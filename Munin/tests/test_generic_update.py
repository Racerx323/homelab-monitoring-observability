#!/usr/bin/python3
"""Offline archive, controller and source-bound acceptance boundaries."""
import importlib.util
import io
import json
import os
from pathlib import Path
import tarfile
import tempfile
import time
import types
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT/'scripts'/name)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


d = load('deploy_generic.py')
p = load('probe_generic.py')
q = load('qualify_generic.py')


class Protocol:
    def __init__(self, raw):
        self.stream = io.BytesIO(raw)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def settimeout(self, value):
        pass

    def bind(self, source):
        self.source = source

    def connect(self, target):
        self.target = target

    def makefile(self, *args):
        return self.stream

    def sendall(self, raw):
        pass


def transcript(cold=False, health='1', names=('diskstats', 'ntp_health')):
    rows = ['# munin node at j2-svntp1', 'cap multigraph', ' '.join(names)]
    for name in sorted(names):
        fields = ['query_ok', 'synced', 'pps_selected'] if name == 'ntp_health' else ['reading']
        rows += ['graph_title Example']+[f+'.label '+f for f in fields]+['.']
        if name != 'diskstats' or not cold:
            rows += [f+'.value '+(health if name == 'ntp_health' else '1') for f in fields]
        rows += ['.']
    return ('\n'.join(rows)+'\n').encode()


class UpdateTests(unittest.TestCase):
    def test_timing_acceptance_requires_corrected_healthy_fields_and_seconds_plot(self):
        path=ROOT/'node/plugins/ntp/ntp_metrics.py'
        spec=importlib.util.spec_from_file_location('timing',path)
        metrics=importlib.util.module_from_spec(spec);spec.loader.exec_module(metrics)
        config='\n'.join(metrics.config('health'))+'\n'
        values='\n'.join(metrics.values('ntp_health',dict.fromkeys(metrics.TIME_FIELDS[:6]+metrics.TIMING_HEALTH_FIELDS,1))
                         +metrics.values('ntp_timing',dict.fromkeys(metrics.TIME_FIELDS[6:],0)))+'\n'
        raw=('# munin node at j2-svntp1\ncap multigraph\nntp_health\n'+config+'.\n'+values+'.\n').encode()
        endpoint=(2,'10.1.0.51','10.1.3.83')
        row=p.probe(endpoint,['ntp_health'],q.fields,connect=lambda *a:Protocol(raw),timing=True)
        self.assertTrue(row['plugins']['ntp_health']['timing_health_corrected'])
        for bad in (raw.replace(b'selected_offset_ok.value 1',b'selected_offset_ok.value 0'),
                    raw.replace(b'selected_jitter_ok.critical 1:1',b'selected_jitter_ok.critical 0:1'),
                    raw.replace(b'graph_vlabel seconds',b'graph_vlabel milliseconds')):
            with self.assertRaises(ValueError):
                p.probe(endpoint,['ntp_health'],q.fields,connect=lambda *a:Protocol(bad),timing=True)

    def test_bound_sources_full_health_and_cold_exception(self):
        endpoint = (2, '10.1.0.51', '10.1.3.83')
        names = ['diskstats', 'ntp_health']
        for seed in (False, True):
            stream = Protocol(transcript(cold=seed))
            row = p.probe(endpoint, names, q.fields, seed, lambda *args: stream)
            self.assertTrue(row['complete'])
            self.assertEqual(stream.source, ('10.1.3.83', 0))
            self.assertEqual(stream.target, ('10.1.0.51', 4949))
        with self.assertRaises(ValueError):
            p.probe(endpoint, names, q.fields, False, lambda *args: Protocol(transcript(cold=True)))
        with self.assertRaises(ValueError):
            p.probe(endpoint, names, q.fields, True, lambda *args: Protocol(transcript(health='0')))

    def test_partial_duplicate_unknown_and_unterminated_frames_fail(self):
        raw = transcript()
        variants = [raw.replace(b'diskstats ntp_health', b'diskstats', 1),
                    raw.replace(b'diskstats ntp_health', b'diskstats diskstats ntp_health', 1),
                    raw.replace(b'reading.value 1', b'reading.value U', 1), raw[:-3]]
        for value in variants:
            with self.assertRaises(ValueError):
                p.probe((2, 'target', 'source'), ['diskstats', 'ntp_health'], q.fields,
                        False, lambda *args: Protocol(value))

    def test_real_deadline_is_checked_after_final_frame(self):
        with patch.object(p.time, 'monotonic', side_effect=[0]+[1]*17+[26]):
            # The explicit deadline rejection is covered without a real socket.
            with self.assertRaises(TimeoutError):
                p.probe((2, 'target', 'source'), ['diskstats', 'ntp_health'], q.fields,
                        False, lambda *args: Protocol(transcript()))

    def test_unapproved_archive_never_imports_adjacent_code(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            path.chmod(0o700)
            archive = path/'deployment.tar'
            archive.write_bytes(b'invalid')
            archive.chmod(0o600)
            (path/'data-utils.py').write_text('raise AssertionError("unverified code loaded")')
            with self.assertRaisesRegex(ValueError, 'hash/size'):
                d.execute(types.SimpleNamespace(directory=path, sha256='0'*64, action='execute'))
            self.assertFalse((path/'execution.json').exists())

    def test_closed_archive_hash_review_and_expiry(self):
        now = int(time.time())
        spec = {'operation_id': 'munin-generic-compatible-20261021-v99', 'prepared_epoch': now,
                'expires_epoch': now+86400, 'recovery_seconds': 20, 'endpoint': 'test',
                'user': 'test', 'host_key_alias': 'test', 'qualification_sha256': d.sha(b'{}'),
                'worker': {'operation_id': 'munin-generic-compatible-20261021-v99', 'role': 'compatible',
                           'target': '/test', 'mode': 0o755, 'fixture': True, 'candidate': 'eA=='}}
        files = {n: b'' for n in d.MEMBERS-{'manifest.json'}}
        files.update({'compatible.py': b'x', 'qualification.json': b'{}', 'spec.json': d.encoded(spec),
                      'review.md': d.review(spec).encode()})
        def archive(extra=False):
            files['manifest.json'] = d.encoded({n: d.sha(v) for n, v in files.items() if n != 'manifest.json'})
            out = io.BytesIO()
            with tarfile.open(fileobj=out, mode='w') as stream:
                for n, raw in list(files.items())+([('extra', b'')] if extra else []):
                    row = tarfile.TarInfo(n)
                    row.size = len(raw)
                    stream.addfile(row, io.BytesIO(raw))
            return out.getvalue()
        raw = archive()
        self.assertEqual(d.unpack(raw, d.sha(raw))[0], spec)
        for altered, digest in ((raw, '0'*64), (archive(True), None)):
            with self.assertRaises(ValueError):
                d.unpack(altered, digest or d.sha(altered))
        files['review.md'] += b'changed'
        raw = archive()
        with self.assertRaises(ValueError):
            d.unpack(raw, d.sha(raw))

    def test_shared_transaction_keeps_real_lock_and_timer_implementation(self):
        files = {'transaction.py': d.SOURCES['transaction.py'].read_bytes()}
        tx = d.transaction(files)
        self.assertEqual(tx.STAGES, d.STAGES)
        self.assertIs(tx.unpack, d.unpack)
        self.assertIn('/usr/bin/systemd-run', tx.root_launch.__code__.co_consts)

    def test_companion_probe_changes_identity_before_execution(self):
        files = {name: d.SOURCES[name].read_bytes() for name in ('helper.py', 'observer.py', 'base.py', 'fields.py', 'probe.py')}
        program = d.prerequisite_program(files, {}, None, True, ['cpu'], False)
        self.assertIn(b'/usr/sbin/runuser', program)
        self.assertIn(b'"munin"', program)
        self.assertIn(b'after=o.continuity(spec)', program)
        self.assertNotIn(b'systemctl restart', program)

    def test_unreviewed_node_dropin_fails_before_restart(self):
        base, worker = load('install_ntp_node.py'), load('update_generic.py')
        cls = worker.make_worker(base, None)
        obj = cls({'operation_id': 'test', 'role': 'node', 'target': '/test', 'candidate': '',
                   'units': {}, 'protected': {}, 'node_unit_layout': {'FragmentPath': '/unit', 'DropInPaths': '/guard'}}, 'hash')
        with patch.object(obj, 'identity'), patch.object(obj, 'ctl', return_value='FragmentPath=/unit\nDropInPaths=/foreign\n') as ctl:
            with self.assertRaisesRegex(ValueError, 'drop-ins'):
                obj.continuity()
        self.assertEqual(ctl.call_args.args, ('show', 'munin-node.service', '--property=FragmentPath,DropInPaths'))


if __name__ == '__main__':
    unittest.main()
