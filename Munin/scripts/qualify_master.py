#!/usr/bin/python3
"""Read-only native master configuration/parser and activation-path qualification."""
import base64
import difflib
import hashlib
import itertools
import json
from pathlib import Path
import re
import stat


def commissioning_config(raw):
    """Preserve existing bytes/identities; keep new contacts explicitly inactive."""
    text = raw.decode('utf-8')
    sections = re.findall(r'^\s*\[([^]\n]+)\]\s*$', text, re.M)
    if len(sections) != len(set(sections)) or sections.count('J1-SVMF') != 1:
        raise ValueError('unique existing master section required')
    if 'j2-svntp1' in sections or re.search(r'^\s*contact\.ntp_mailrise\.', text, re.M):
        raise ValueError('candidate already present; inspect before merging')
    newline = '\r\n' if text.count('\r\n') > text.count('\n')/2 else '\n'
    pattern = r'(^[ \t]*\[J1-SVMF\][ \t]*(\r?\n|$))'
    def insert(match):
        ending = match[2] or newline
        return (match[1]+('' if match[2] else newline)
                +'    ntp_transport_j2.contacts none'+ending
                +'    ntp_transport_j2.unknown_limit 0'+ending)
    text, count = re.subn(pattern, insert, text, count=1, flags=re.M)
    if count != 1:
        raise ValueError('master header not safely mergeable')
    if not text.endswith('\n'):
        text += newline
    return (text+newline+newline.join(('[j2-svntp1]',
            '    address 10.1.0.51','    port 4949','    use_node_name yes',
            '    contacts none','    unknown_limit 0',''))).encode()


def configuration_difference(repository, live):
    """Expose known non-secret directives only; preserve hash-level distinction."""
    allowed = {'address','use_node_name','port','dbdir','htmldir','logdir','rundir',
               'tmpldir','staticdir','cgitmpdir','includedir','graph_period',
               'graph_strategy','html_strategy','munin_cgi_graph_jobs','max_processes',
               'max_size_x','max_size_y','rrdcached_socket',
               'timeout_fetch_all_nodes','timeout_fetch_one_node'}
    def display(line):
        text = line.strip()
        if not text or text.startswith('#'):
            return '[blank/comment omitted]'
        if re.fullmatch(r'\[[A-Za-z0-9_.;-]+\]', text):
            return text
        parts = text.split(None,1)
        if (len(parts)==2 and parts[0] in allowed
                and re.fullmatch(r'[A-Za-z0-9_./:\[\] -]+',parts[1])):
            return text
        return '[directive omitted]'
    a=repository.decode().splitlines(); b=live.decode().splitlines()
    differences=[]
    for tag,i,j,k,l in difflib.SequenceMatcher(a=a,b=b,autojunk=False).get_opcodes():
        if tag!='equal':
            differences.append({'repository_line':i+1,'production_line':k+1,
                                'repository':[display(v) for v in a[i:j]],
                                'production':[display(v) for v in b[k:l]]})
    return {'text_matches_ignoring_line_endings':a==b,
            'repository_crlf':repository.count(b'\r\n'),'production_crlf':live.count(b'\r\n'),
            'differences':differences}


def without_rrdcached(raw):
    """Candidate only: direct RRD access; preserve every unrelated baseline byte."""
    pattern=rb'(?m)^[ \t]*rrdcached_socket[ \t]+/var/run/rrdcached\.sock[ \t]*(?:\r?\n|$)'
    if len(re.findall(rb'(?m)^[ \t]*rrdcached_socket\b',raw))!=1:
        raise ValueError('one reviewed cache directive required')
    candidate,count=re.subn(pattern,b'',raw)
    if count!=1:
        raise ValueError('unreviewed cache endpoint; no candidate')
    return candidate


# Config::parse_config only parses the supplied in-memory streams. It does not
# run update/limits, initialize contact pipes, expand includes or open log files.
PARSER = r'''
use strict; use warnings; use JSON::PP; use Munin::Master::Config;
my $input=do {local $/; <STDIN>}; my $data=decode_json($input); my %result;
for my $name (sort keys %$data) {
    my $cfg=bless({config_file=>"sealed-$name",groups=>{}},'Munin::Master::Config');
    my @errors;
    for my $text (@{$data->{$name}}) {
        open my $fh,'<',\$text or die 'memory stream';
        eval {$cfg->parse_config($fh,0)};
        push @errors, "$@" if $@;
        close $fh;
    }
    $result{$name}={parsed=>@errors?JSON::PP::false:JSON::PP::true,errors=>\@errors};
}
print encode_json(\%result);
'''


def collect(helper, repository_raw, candidate_raw, root=Path('/etc/munin'), export_sha256=None):
    records = []
    paths = [root/'munin.conf']
    include = root/'munin-conf.d'
    if include.is_symlink():
        raise ValueError('indirect includedir')
    if include.exists():
        if not include.is_dir():
            raise ValueError('includedir must be a directory')
        children = sorted(itertools.islice(include.iterdir(),65))
        if len(children) > 64:
            raise ValueError('include count bound')
        # Native include expansion/filter semantics must be read before any
        # mutation. Do not pretend parsing all files proves effective inheritance.
        paths += [p for p in children if not p.name.startswith('.')]
    contents = []
    for path in paths:
        if path.is_symlink() or any(p.is_symlink() for p in path.parents):
            raise ValueError('indirect configuration')
        row = helper.file_record(path, content=True)
        if 'base64' not in row or row.get('changed_during_read'):
            raise ValueError('stable regular configuration required')
        raw = base64.b64decode(row.pop('base64'), validate=True)
        if len(raw) > 65536:
            raise ValueError('configuration bound')
        contents.append(raw.decode('utf-8'))
        records.append({'path': str(path), 'record': row})
    raw = contents[0].encode()
    if export_sha256 is not None and hashlib.sha256(raw).hexdigest() != export_sha256:
        raise ValueError('production baseline drift; no raw export or repair')
    merged = commissioning_config(raw)
    streams = {'live_files': contents, 'commissioning': [merged.decode()]+contents[1:],
                          'repository': [repository_raw.decode()],
                          'contact_example_in_memory_only': [candidate_raw.decode()]}
    if export_sha256 is not None:
        streams['commissioning_direct_rrd']=[commissioning_config(without_rrdcached(raw)).decode()]+contents[1:]
    payload = json.dumps(streams).encode()
    command = ['/usr/sbin/runuser', '-u', 'munin', '--', '/usr/bin/perl', '-e', PARSER]
    parsed = helper.bounded(command, timeout=25, limit=helper.LIMIT, payload=payload,
                            env={'PATH':'/usr/sbin:/usr/bin:/sbin:/bin','LC_ALL':'C'})
    before = records
    after = [{'path':str(p),'record':helper.file_record(p)} for p in paths]
    if before != after:
        raise ValueError('configuration changed during qualification')
    socket = Path('/run/rrdcached.sock')
    try:
        info = socket.lstat()
        cache = {'socket':stat.S_ISSOCK(info.st_mode),'mode':stat.S_IMODE(info.st_mode),
                 'uid':info.st_uid,'gid':info.st_gid}
    except FileNotFoundError:
        cache = {'missing':True}
    result = {'files':records,'repository_matches_live':raw == repository_raw,
            'configuration_difference':configuration_difference(repository_raw,raw),
            'repository_sha256':hashlib.sha256(repository_raw).hexdigest(),
            'commissioning_sha256':hashlib.sha256(merged).hexdigest(),
            'native_parser':parsed,'rrdcached_socket':cache,
            'include_expansion_and_effective_inheritance_accepted':False,
            'activation_or_restoration_executed':False,'messages_sent':False}
    if export_sha256 is not None:
        result['production_baseline'] = {'sha256':export_sha256,
            'base64':base64.b64encode(raw).decode(), 'path':'/etc/munin/munin.conf'}
        result['direct_rrd_candidate_sha256']=hashlib.sha256(
            commissioning_config(without_rrdcached(raw))).hexdigest()
    return result
