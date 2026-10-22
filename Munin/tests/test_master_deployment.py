#!/usr/bin/python3
"""Offline guard, archive and reconciliation policy checks; native cases are separate."""
import ast
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]


def load(path):
    spec=importlib.util.spec_from_file_location(path.stem,path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod


r=load(ROOT/'scripts/deploy_ntp_master.py')
s=load(ROOT/'scripts/sync_master_baseline.py')


class MasterDeploymentTests(unittest.TestCase):
    def test_bad_archive_rejected_before_any_module_or_contact(self):
        with patch.object(r,'module',side_effect=AssertionError('executable load')):
            with self.assertRaisesRegex(ValueError,'archive hash'):
                r.unpack(b'changed','0'*64)

    def test_actual_stdin_bootstrap_reaches_root_guard_before_any_host_command(self):
        files={'runner.py':(ROOT/'scripts/deploy_ntp_master.py').read_bytes()}
        program=r.payload(files,b'not-an-archive','0'*64,'apply','munin-master-test')
        with patch.object(r.os,'geteuid',return_value=1000),patch.object(r.subprocess,'run',side_effect=AssertionError('host command')):
            with self.assertRaisesRegex(ValueError,'root launcher required'):
                exec(compile(program,'<actual-master-stdin>','exec'),{})

    def test_reconciliation_does_not_overwrite_a_changed_repository_baseline(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'munin.conf';path.write_bytes(b'operator edit')
            with self.assertRaisesRegex(ValueError,'approved baseline'):
                s.synchronize(b'candidate',path,write=True,expected_before=b'old baseline')
            self.assertEqual(path.read_bytes(),b'operator edit')

    def test_sources_are_durable_and_actual_runtime_worker_has_no_job_or_mail_execution(self):
        for path in r.SOURCES.values():self.assertTrue(path.is_file(),str(path))
        source=(ROOT/'scripts/install_ntp_master.py').read_text()
        tree=ast.parse(source)
        calls=[n for n in ast.walk(tree) if isinstance(n,ast.Call)]
        for n in calls:
            text=ast.get_source_segment(source,n) or ''
            if isinstance(n.func,ast.Attribute) and n.func.attr in ('command','ctl'):
                self.assertNotIn('munin-update',text)
                self.assertNotIn('munin-limits',text)
                self.assertNotIn('sendmail',text)
                self.assertNotIn("'apache2.service'",text)
        self.assertIn('signal.pidfd_send_signal',source)
        self.assertNotIn('SIGKILL',source)

    def test_review_preserves_contacts_and_separates_later_acceptance(self):
        text=r.review({'operation_id':'munin-master-test','expires_epoch':1792696285})
        for expected in ('contacts none','No contact definitions','three later approved',
                         'root-private','600','not overwritten','SIGKILL'):
            self.assertIn(expected,text)


if __name__=='__main__':unittest.main()
