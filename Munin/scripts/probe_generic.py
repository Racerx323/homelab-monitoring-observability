#!/usr/bin/python3
"""Source-bound native node acceptance, including explicitly cold seed samples."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import socket
import time


def probe(endpoint, names, validate_fields, seed=False, connect=socket.socket):
    family, target, source = endpoint
    started = time.monotonic()
    deadline = started+25
    records = {}
    with connect(family, socket.SOCK_STREAM) as connection:
        connection.settimeout(3)
        connection.bind((source, 0))
        connection.connect((target, 4949))
        with connection.makefile('rb') as stream:
            def line():
                remaining = deadline-time.monotonic()
                if remaining <= 0:
                    raise TimeoutError('25-second protocol deadline')
                connection.settimeout(min(10, remaining))
                raw = stream.readline(8193)
                if not raw or len(raw) > 8192 or not raw.endswith(b'\n'):
                    raise ValueError('bounded native protocol line required')
                return raw.decode('ascii').strip()

            def send(value):
                connection.sendall(value.encode()+b'\n')

            def frame():
                rows, size = [], 0
                for _ in range(4096):
                    text = line()
                    if text == '.':
                        return '\n'.join(rows)+'\n' if rows else ''
                    size += len(text)
                    if size > 262144 or text.startswith('# Unknown'):
                        raise ValueError('invalid native frame')
                    rows.append(text)
                raise ValueError('unterminated native frame')

            if line() != '# munin node at j2-svntp1':
                raise ValueError('node identity mismatch')
            send('cap multigraph')
            if 'multigraph' not in line().split():
                raise ValueError('multigraph capability missing')
            send('list j2-svntp1')
            reported = line().split()
            if len(reported) != len(set(reported)) or set(reported) != set(names):
                raise ValueError('exact node selection mismatch')
            for name in sorted(names):
                send('config '+name)
                config = frame()
                send('fetch '+name)
                fetch = frame()
                record = {'config_sha256': hashlib.sha256(config.encode()).hexdigest(),
                          'fetch_sha256': hashlib.sha256(fetch.encode()).hexdigest()}
                if seed and name == 'diskstats' and not fetch.strip():
                    if 'graph_title ' not in config:
                        raise ValueError('cold diskstats configuration absent')
                    record['cold_seed_no_sample'] = True
                else:
                    record.update(validate_fields(config, fetch))
                    unknown = record['unknown_fields']
                    allowed = {('ntp_job_age', 'retention_age'), ('ntp_job_age', 'reporting_age')}
                    if any(tuple(field) not in allowed or name != 'ntp_jobs' for field in unknown):
                        raise ValueError('unaccepted unknown field: '+name)
                if name == 'ntp_health':
                    if any(field+'.value 1' not in fetch.splitlines() for field in ('query_ok', 'synced', 'pps_selected')):
                        raise ValueError('NTP health lost')
                records[name] = record
            send('quit')
    if time.monotonic() > deadline:
        raise TimeoutError('25-second full protocol budget exceeded')
    return {'source': source, 'target': target, 'seconds': time.monotonic()-started,
            'seed_only': seed, 'plugins': records, 'complete': True}


def both(endpoints, names, validate_fields, seed=False):
    def run(endpoint):
        try:
            return probe(endpoint, names, validate_fields, seed)
        except Exception as error:
            return {'source': endpoint[2], 'target': endpoint[1], 'complete': False, 'error': str(error)}
    with ThreadPoolExecutor(max_workers=2) as pool:
        rows = list(pool.map(run, endpoints))
    return {'complete': all(r['complete'] for r in rows), 'seed_only': seed, 'families': rows}
