#!/usr/bin/python3
"""Offline protocol and contact checks; no real network or SMTP operation."""
import importlib.machinery
import importlib.util
import io
import json
import os
from pathlib import Path
import smtplib
import socket
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]


def load(path):
    loader=importlib.machinery.SourceFileLoader(path.stem,str(path))
    spec=importlib.util.spec_from_loader(path.stem,loader)
    module=importlib.util.module_from_spec(spec);loader.exec_module(module)
    return module


t=load(ROOT/'master/plugins/ntp_transport_j2');a=load(ROOT/'scripts/ntp_mailrise.py')


class Protocol:
    def __init__(self,data):self.stream=io.BytesIO(data);self.sent=[]
    def __enter__(self):return self
    def __exit__(self,*args):pass
    def settimeout(self,value):self.timeout=value
    def bind(self,value):self.source=value
    def connect(self,value):self.target=value
    def makefile(self,*args):return self.stream
    def sendall(self,data):self.sent.append(data.decode().strip())


def transcript(value='U'):
    rows=['# munin node at j2-svntp1','cap multigraph',' '.join(sorted(t.PLUGINS))]
    for plugin in sorted(t.PLUGINS):
        rows+=['multigraph '+plugin,'graph_title Example','reading.label Reading','.',
               'multigraph '+plugin,'reading.value '+value,'.']
    return ('\n'.join(rows)+'\n').encode()


class MasterTests(unittest.TestCase):
    def test_all_selected_plugins_both_explicit_source_binds(self):
        for endpoint in t.ENDPOINTS:
            connection=Protocol(transcript())
            self.assertEqual(t.check(endpoint,lambda *args:connection),1)
            self.assertEqual(connection.source,(endpoint[2],0));self.assertEqual(connection.target,(endpoint[1],4949))
            self.assertEqual(len([x for x in connection.sent if x.startswith('fetch ')]),len(t.PLUGINS))

    def test_partial_identity_missing_plugin_invalid_value_and_duplicate_fail(self):
        raw=transcript('1')
        for data in (raw.replace(b'j2-svntp1',b'foreign',1),raw.replace(b'ntp_jobs ',b'',1),
                     raw.replace(b'reading.value 1',b'reading.value garbage',1),
                     raw.replace(b'reading.value 1',b'other.value 1',1),
                     raw.replace(b'reading.value 1',b'reading.value 1\nreading.value 1',1),raw[:-3]):
            with self.assertRaises(ValueError):t.check(t.ENDPOINTS[0],lambda *args:Protocol(data))

    def test_family_failure_independent_and_config_has_no_network(self):
        def check(endpoint):
            if endpoint[0]==socket.AF_INET6:raise TimeoutError('refused')
            return 1
        with patch.object(t,'check',side_effect=check),patch.object(t,'submission_status',return_value='U'):
            self.assertEqual(t.fetch(),'v4.value 1\nv6.value 0\nmail.value U')
        with patch.object(t.socket,'socket',side_effect=AssertionError('network')):
            self.assertIn('v6.critical 1:1',t.config())

    def test_alert_routes_recovery_and_fixed_origin(self):
        for state in ('WARNING','CRITICAL','UNKNOWN','OK'):
            msg=a.message(f'{state}|j2-svntp1|ntp_job_age||retention_age|'.encode())
            self.assertEqual(msg['To'],'notify@mailrise.xyz' if state=='OK' else 'notify.failure@mailrise.xyz')
            self.assertIn(state,msg['Subject'])
        for raw in (b'CRITICAL|foreign|load|||',b'OK|J1-SVMF|load|||',b'OK|j2-svntp1|arbitrary|||',
                    b'OK|j2-svntp1\nBcc: evil|load|||',b'OK|j2-svntp1|load|x;y||',b'x'*16385):
            with self.assertRaises(ValueError):a.message(raw)

    def test_smtp_submission_refusal_no_retry_and_status_roundtrip(self):
        calls=[]
        class SMTP:
            def __init__(self,*args,**kwargs):calls.append((args,kwargs))
            def __enter__(self):return self
            def __exit__(self,*args):pass
            def send_message(self,msg):return {'notify.failure@mailrise.xyz':(550,b'refused')}
        with self.assertRaises(RuntimeError):a.deliver(a.message(b'CRITICAL|j2-svntp1|load|||'),SMTP)
        self.assertEqual(calls,[(('127.0.0.1',8025),{'timeout':10})])
        with tempfile.TemporaryDirectory() as tmp:
            directory=Path(tmp);directory.chmod(0o700);path=directory/'status.json'
            self.assertEqual(t.submission_status(path),'U')
            a.save_status(False,path);self.assertEqual(t.submission_status(path),0)
            a.save_status(True,path);self.assertEqual(t.submission_status(path),1)
            path.chmod(0o644);self.assertEqual(t.submission_status(path),'U')
            with self.assertRaises(ValueError):a.save_status(True,path)

    def test_one_message_pipe_is_explicit(self):
        text=(ROOT/'master/configs/j2-svntp1.conf.example').read_text()
        self.assertIn('contact.ntp_mailrise.max_messages 1',text)
        self.assertNotIn('command ${',text)


if __name__=='__main__':unittest.main()
