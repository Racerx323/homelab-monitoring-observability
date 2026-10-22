#!/usr/bin/python3
"""Offline checks for preserving merges and a read-only native parser probe."""
import importlib.util
import base64
import hashlib
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import Mock

SOURCE = Path(__file__).resolve().parents[1]/'scripts/qualify_master.py'
spec = importlib.util.spec_from_file_location('qualification', SOURCE)
q = importlib.util.module_from_spec(spec)
spec.loader.exec_module(q)


class QualificationTests(unittest.TestCase):
    def test_merge_preserves_identities_and_disables_only_new_contacts(self):
        raw = b'dbdir /var/lib/munin\n[J1-SVMF]\n address 127.0.0.1\n[j2-svpi4mf]\n address 10.1.2.170\n'
        merged = q.commissioning_config(raw)
        self.assertIn(b'[j2-svpi4mf]\n address 10.1.2.170\n', merged)
        self.assertEqual(merged.count(b'[J1-SVMF]'), 1)
        self.assertEqual(merged.count(b'[j2-svntp1]'), 1)
        self.assertIn(b'ntp_transport_j2.contacts none', merged)
        self.assertIn(b'    contacts none', merged)
        self.assertNotIn(b'contact.ntp_mailrise.command', merged)

    def test_reject_duplicate_missing_or_preexisting_authored_sections(self):
        for text in ('[other]\n', '[J1-SVMF]\n[J1-SVMF]\n',
                     '[J1-SVMF]\n[j2-svntp1]\n',
                     'contact.ntp_mailrise.command unexpected\n[J1-SVMF]\n'):
            with self.assertRaises(ValueError):
                q.commissioning_config(text.encode())

    def test_merge_is_one_use_and_preserves_global_include(self):
        raw = b'includedir /etc/munin/munin-conf.d\n[J1-SVMF]\n address 127.0.0.1\n'
        merged = q.commissioning_config(raw)
        self.assertTrue(merged.startswith(b'includedir /etc/munin/munin-conf.d\n'))
        with self.assertRaises(ValueError):
            q.commissioning_config(merged)

    def test_parser_probe_uses_native_memory_parser_without_startup(self):
        self.assertIn('parse_config($fh,0)', q.PARSER)
        self.assertIn('do {local $/; <STDIN>}', q.PARSER)
        for forbidden in ('munin_readconfig', 'logger_open', 'system(', 'qx(', 'limits_startup'):
            self.assertNotIn(forbidden, q.PARSER)

    def test_difference_distinguishes_line_endings_and_omits_contact_secrets(self):
        self.assertTrue(q.configuration_difference(b'[host]\r\n',b'[host]\n')
                        ['text_matches_ignoring_line_endings'])
        result=q.configuration_difference(b'[old]\n',b'[new]\ncontact.secret.command TOKEN\n')
        self.assertFalse(result['text_matches_ignoring_line_endings'])
        self.assertNotIn('TOKEN',str(result))
        self.assertIn('[new]',str(result))

    def test_crlf_merge_preserves_existing_bytes(self):
        raw=b'dbdir /var/lib/munin\r\n[J1-SVMF]\r\n address 127.0.0.1\r\n'
        merged=q.commissioning_config(raw)
        self.assertIn(b' address 127.0.0.1\r\n',merged)
        self.assertIn(b'ntp_transport_j2.contacts none\r\n',merged)
        self.assertEqual(merged.count(b'\n'),merged.count(b'\r\n'))

    def test_direct_rrd_candidate_removes_only_reviewed_dependency(self):
        raw=b'# cache example\r\nrrdcached_socket /var/run/rrdcached.sock\r\n[J1-SVMF]\r\n'
        self.assertEqual(q.without_rrdcached(raw),b'# cache example\r\n[J1-SVMF]\r\n')
        for text in (b'[J1-SVMF]\n',raw+raw,
                     raw.replace(b'/var/run/rrdcached.sock',b'/other/socket')):
            with self.assertRaises(ValueError):q.without_rrdcached(text)

    def test_raw_export_is_hash_pinned_and_drift_precedes_native_command(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);raw=b'rrdcached_socket /var/run/rrdcached.sock\n[J1-SVMF]\n'
            (root/'munin.conf').write_bytes(raw)
            def record(path,content=False):
                data=path.read_bytes();row={'sha256':hashlib.sha256(data).hexdigest()}
                if content:row['base64']=base64.b64encode(data).decode()
                return row
            command=Mock(return_value={'returncode':0})
            helper=types.SimpleNamespace(file_record=record,bounded=command,LIMIT=1048576)
            with self.assertRaisesRegex(ValueError,'baseline drift'):
                q.collect(helper,raw,raw,root,export_sha256='0'*64)
            command.assert_not_called()
            result=q.collect(helper,raw,raw,root,export_sha256=hashlib.sha256(raw).hexdigest())
            self.assertEqual(base64.b64decode(result['production_baseline']['base64']),raw)
            self.assertIn(b'commissioning_direct_rrd',command.call_args.kwargs['payload'])


if __name__ == '__main__':
    unittest.main()
