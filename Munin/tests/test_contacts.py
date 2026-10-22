#!/usr/bin/python3
"""Closed scope, exact payload and review binding checks; no network or SMTP."""
import base64
import copy
from email.message import EmailMessage
from email import policy
import importlib.util
import json
import os
import re
from pathlib import Path
import socket
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


d = load(ROOT/'scripts/review_ntp_contacts.py')
c = load(ROOT/'scripts/install_ntp_contacts.py')


def inactive_baseline():
    """Keep installer tests valid after the canonical production mirror is active."""
    raw = (ROOT/'master/configs/munin.conf').read_bytes()
    if b'contact.ntp_mailrise.command ' not in raw:
        return raw
    raw = re.sub(rb'(?m)^contacts none\n(?=contact\.ntp_mailrise\.command )', b'', raw)
    raw = re.sub(rb'(?m)^contact\.ntp_mailrise\.(?:command|text|max_messages) [^\n]*\n', b'', raw)
    raw = re.sub(rb'(?m)^([ \t]*ntp_transport_j2\.contacts) ntp_mailrise$', rb'\1 none', raw)
    graphs = b'|'.join(re.escape(name.encode()) for name in sorted(c.GRAPHS))
    return re.sub(rb'(?m)^[ \t]*(?:'+graphs+rb')\.contacts ntp_mailrise\n', b'', raw)


def message(label):
    helper = load(ROOT/'scripts/ntp_mailrise.py')
    msg = helper.message((b'CRITICAL|j2-svntp1|ntp_health||selected_offset_ok selected_jitter_ok|'
                          if label == 'problem' else b'OK|j2-svntp1|ntp_health|||'))
    msg.replace_header('Subject', '[DELIVERY TEST] ' + str(msg['Subject']))
    msg.set_content('Controlled delivery test. No production fault was induced.\n\n' + msg.get_content())
    msg['Date'] = 'Thu, 22 Oct 2026 12:00:00 -0500'
    msg['Message-ID'] = '<qualification-' + label + '@local.theama.co>'
    return msg.as_bytes(policy=policy.SMTP)


def fixture(output, kind='activation', units=None, protected=None, fault=None, prerequisite=None, proof=None):
    os.umask(0o077)
    files = {n: p.read_bytes() for n, p in d.SOURCES.items()}
    before = inactive_baseline()
    candidate = c.render(before)
    now = time.time()
    op = 'munin-contacts-' + ('activate' if kind == 'activation' else kind) + '-20261022-v1'
    files.update({'production-before.conf': before, 'repository-before.conf': before,
        'candidate.conf': candidate, 'message.eml': b'', 'preview.txt': b'', 'ca.pem': b'', 'known_hosts': b'',
        'qualification.json': b'{}', 'candidate.diff': b'qualified fixture candidate', 'metadata-evidence.json': b'{}'})
    spec = {'schema': 1, 'kind': kind, 'operation_id': op, 'prepared_epoch': now,
        'expires_epoch': now+3600, 'recovery_seconds': 4, 'repository_target': '/evidence/mirror.conf',
        'worker': {'operation_id': op, 'hostname': socket.gethostname(),
            'boot_id': Path('/proc/sys/kernel/random/boot_id').read_text().strip(),
            'fixture': True, 'before_sha256': d.sha(before), 'candidate_sha256': d.sha(candidate),
            'units': units or {}, 'protected_files': protected or {},
            'artifacts': {k: base64.b64encode(files[n]).decode() for k, n in
                (('config', 'candidate.conf'), ('repository', 'repository-before.conf'), ('helper', 'mailrise.py'), ('gate', 'gate.py'))}}}
    if fault:
        spec['worker']['test_fault'] = fault
    if proof is not None:
        spec['worker']['predecessor_proof'] = proof
    if kind != 'activation':
        raw = message(kind)
        preview = raw.decode().replace('\r\n', '\n') + '\nAttachments: none\n'
        files.update({'message.eml': raw, 'preview.txt': preview.encode()})
        spec.update(message_label=kind, message_sha256=d.sha(raw), preview=preview,
                    activation_prerequisite=prerequisite)
        if kind == 'recovery':
            spec['problem_prerequisite'] = {'directory': '/evidence/problem', 'archive_sha256': 'a'*64,
                                             'message_sha256': d.sha(message('problem'))}
    digest = d.write_archive(output, spec, files)
    return spec, files, digest


class Contacts(unittest.TestCase):
    def test_proof_exception_bound_to_completed_diagnostic(self):
        digest = 'a'*64
        original = 'b'*64
        files = {'/etc/munin/munin.conf': original, '/protected': 'c'*64}
        worker = {'hostname': 'J1-SVMF', 'boot_id': 'boot', 'units': {},
                  'before_sha256': original, 'protected_files': {'/protected': 'c'*64}}
        spec = {'purpose': 'contact-metadata', 'kind': 'master',
                'operation_id': 'munin-contact-config-metadata-20261022-v1',
                'hostname': 'J1-SVMF', 'endpoint': '10.1.3.83', 'boot_id': 'boot', 'units': {}, 'files': files}
        m = {'uid': 0, 'gid': 0, 'mode': 0o644, 'nlink': 2, 'sha256': original,
             'device': 1, 'inode': 42, 'size': 100, 'mtime': 123.5}
        matches = {'uid': True, 'gid': True, 'mode': True, 'nlink': False, 'sha256': True}
        capture = {'spec_sha256': d.sha(d.encoded(spec)), 'operation_id': spec['operation_id'],
                   'target_mutation': False, 'capture_complete': True,
                   'before': {'units': {}, 'file_hashes': files}, 'after': {'units': {}, 'file_hashes': files},
                   'observations': {'main': {'path': '/etc/munin/munin.conf', 'metadata': m, 'matches': matches},
                       'predecessor_proof': {'path': d.PROOF, 'metadata': dict(m), 'matches': dict(matches)},
                       'same_inode_as_predecessor_proof': True,
                       'presence': {str(p): {'missing': True} for p in (c.HELPER, c.GATE, c.CONTROL, c.STATUS)}}}
        evidence = {'spec': spec, 'capture': capture, 'archive_sha256': digest,
                    'result': {'returncode': 0, 'capture_complete': True, 'bundle_sha256': digest},
                    'receipt': {'sha256': digest}, 'outcome': {'archive_sha256': digest,
                        'diagnosis_accepted': True, 'target_mutation': False}}
        expected = {k: m[k] for k in ('device', 'inode', 'size', 'mtime', 'sha256')}
        self.assertEqual(d.proof_from_evidence(evidence, worker), expected)
        mutations = [lambda e: e['capture']['observations']['predecessor_proof'].update(path='/foreign'),
                     lambda e: e['capture']['observations']['predecessor_proof']['metadata'].update(inode=99),
                     lambda e: e['capture']['observations']['main']['metadata'].update(nlink=3),
                     lambda e: e['receipt'].update(sha256='f'*64),
                     lambda e: e['capture'].update(capture_complete=False),
                     lambda e: e['capture']['after'].update(units={'foreign': {}}),
                     lambda e: e['outcome'].update(diagnosis_accepted=False),
                     lambda e: e['capture']['observations']['presence'][str(c.GATE)].update(missing=False)]
        for mutate in mutations:
            changed = copy.deepcopy(evidence)
            mutate(changed)
            with self.assertRaises(ValueError):
                d.proof_from_evidence(changed, worker)

    def test_preserving_nine_graph_scope_and_default_none(self):
        before = inactive_baseline()
        candidate = c.directives(c.render(before))
        self.assertEqual(candidate['global']['contacts'], 'none')
        self.assertEqual(candidate['j2-svntp1']['contacts'], 'none')
        selected = {(h, k[:-9]) for h, v in candidate.items() for k, x in v.items()
                    if k.endswith('.contacts') and x == 'ntp_mailrise'}
        self.assertEqual(selected, {('j2-svntp1', g) for g in c.GRAPHS} | {('J1-SVMF', 'ntp_transport_j2')})
        self.assertIn(str(c.GATE), candidate['global']['contact.ntp_mailrise.command'])
        self.assertEqual(candidate['global']['contact.ntp_mailrise.max_messages'], '1')

    def test_duplicate_existing_contact_and_foreign_baseline_rejected(self):
        before = inactive_baseline()
        for bad in (before + b'\n[j2-svntp1]\n', b'contacts none\n'+before,
                    b'contact.foreign.command mail\n'+before,
                    before.replace(b'contacts none', b'contacts foreign', 1)):
            with self.subTest(bad=bad[-40:]), self.assertRaises(ValueError):
                c.render(bad)

    def test_exact_message_routes_and_reject_mutation(self):
        for label, recipient in (('problem', 'notify.failure@mailrise.xyz'), ('recovery', 'notify@mailrise.xyz')):
            raw = message(label)
            self.assertEqual(c.validate_message(raw, label), recipient)
            for bad in (raw.replace(b'\r\n', b'\n'), raw.replace(b'From:', b'Bcc: evil@example.com\r\nFrom:', 1),
                        raw.replace(b'notify', b'foreign', 1), raw.replace(b'[DELIVERY TEST] ', b'', 1)):
                with self.assertRaises(ValueError):
                    c.validate_message(bad, label)

    def test_archive_bound_to_all_bytes_and_role(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec, files, digest = fixture(Path(tmp)/'bundle')
            raw = (Path(tmp)/'bundle/deployment.tar').read_bytes()
            self.assertEqual(d.unpack(raw, digest)[0], spec)
            with self.assertRaises(ValueError):
                d.unpack(raw+b'x', digest)
            spec['operation_id'] = 'munin-contacts-problem-20261022-v1'
            spec['worker']['operation_id'] = spec['operation_id']
            with self.assertRaises(ValueError):
                d.write_archive(Path(tmp)/'foreign-role', spec, files)
            self.assertFalse((Path(tmp)/'foreign-role').exists())

    def test_recovery_requires_operator_confirmation(self):
        spec = {'kind': 'recovery', 'problem_prerequisite': {'archive_sha256': 'a'*64, 'message_sha256': 'b'*64}}
        for context in ({}, {'problem_confirmation': {'delivered': True}}):
            with self.assertRaises(ValueError):
                d.confirmation(spec, context)
        ack = {'archive_sha256': 'a'*64, 'message_sha256': 'b'*64, 'delivered': True,
               'source': 'operator', 'acknowledgement': 'Aaron confirmed receipt', 'execution_receipt_sha256': 'c'*64}
        d.confirmation(spec, {'problem_confirmation': ack})
        ack['source'] = 'inferred'
        with self.assertRaises(ValueError):
            d.confirmation(spec, {'problem_confirmation': ack})


if __name__ == '__main__':
    unittest.main()
