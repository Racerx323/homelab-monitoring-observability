"""Offline parser, privilege-contract, metadata and missing-evidence tests."""
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location('metrics',ROOT/'node/plugins/ntp/ntp_metrics.py')
m=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(m)
SAMPLE='leap=00, stratum=1, offset=-0.125, sys_jitter=0.015\n     remote refid st t when poll reach delay offset jitter\no127.127.22.0 .PPS. 0 l 4 16 377 0.000 -0.125 0.015\n'


class MetricsTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)

    def test_ntp_units_selection_and_missing_data(self):
        d=m.parse_ntpq(SAMPLE);self.assertEqual(d['reach'],255);self.assertEqual(d['selected_offset'],-.000125)
        self.assertAlmostEqual(d['selected_jitter'],.000015);self.assertEqual(d['pps_selected'],1);self.assertEqual(d['synced'],1)
        for raw in ('',SAMPLE.replace('offset=-0.125','offset=nan'),SAMPLE+SAMPLE,SAMPLE.replace(' 377 ',' 888 ')):
            with self.assertRaises(ValueError):m.parse_ntpq(raw)
        self.assertEqual(m.parse_ntpq(SAMPLE.replace('leap=00','leap=11'))['synced'],0)

    def test_query_is_numeric_local_fixed_command_and_bounded(self):
        p=types.SimpleNamespace(returncode=0,stdout=SAMPLE)
        with patch.object(m.subprocess,'run',return_value=p) as run:
            self.assertEqual(m.time_metrics()['query_ok'],1)
            args=run.call_args;self.assertEqual(args.args[0][-1],'127.0.0.1');self.assertIn('-n',args.args[0])
            self.assertEqual(args.kwargs['timeout'],8)
        with patch.object(m.subprocess,'run',side_effect=OSError):
            d=m.time_metrics();self.assertEqual(d['query_ok'],0);self.assertEqual(d['stratum'],'U')

    def test_observed_shm2_pps_system_peer_and_negative_identities(self):
        raw=(ROOT/'tests/fixtures/ntpq-shm2-selected.txt').read_text()
        self.assertEqual(m.parse_ntpq(raw)['pps_selected'],1)
        self.assertEqual(m.parse_ntpq(raw.replace('*SHM(2)','*127.127.28.2'))['pps_selected'],1)
        for changed in (raw.replace('*SHM(2)','*SHM(0)'),raw.replace('.PPS.','.NMEA.'),
                        raw.replace('*SHM(2)','*192.0.2.1'),raw.replace('*SHM(2)','oSHM(0)'),raw.replace('0 l','1 u')):
            self.assertEqual(m.parse_ntpq(changed)['pps_selected'],0)
        with self.assertRaises(ValueError):m.parse_ntpq(raw+raw.splitlines()[-1]+'\n')

    def test_storage_uses_available_bytes_and_available_inodes(self):
        fs=types.SimpleNamespace(f_bavail=10,f_frsize=4096,f_files=100,f_favail=5,f_ffree=90)
        d=m.storage_metrics(statvfs=lambda p:fs)
        self.assertEqual(d['root_bytes'],40960);self.assertEqual(d['root_inodes'],5)
        with patch.object(m,'storage_metrics',return_value=d):self.assertIn('root_bytes.value 40960',m.fetch('storage'))
        self.assertIn('root_bytes.critical 10737418240:',m.config('storage'))
        self.assertIn('root_inodes.critical 5:',m.config('storage'))
        self.assertEqual(m.storage_metrics(statvfs=lambda p: (_ for _ in ()).throw(OSError()))['root_ok'],0)

    def test_stats_never_reads_records_and_deduplicates_hardlinks(self):
        p=self.root/'loopstats';p.write_text('SECRET RECORD');os.utime(p,(100,100))
        os.link(p,self.root/'loopstats.20261020')
        with patch.object(Path,'read_bytes',side_effect=AssertionError('raw read forbidden')):
            d=m.statistics_metrics(self.root,now=120)
        self.assertEqual(d['bytes']['loopstats'],len('SECRET RECORD'));self.assertEqual(d['age']['loopstats'],20)
        self.assertNotIn('SECRET',json.dumps(d));self.assertEqual(d['age']['protostats'],'U')
        self.assertNotIn('protostats.critical 0:3600',m.config('statistics'))
        (self.root/'peerstats').symlink_to(p)
        self.assertEqual(m.statistics_metrics(self.root,now=120)['ok'],0)

    def test_rollover_new_inode_and_future_timestamp(self):
        p=self.root/'clockstats.20261019';p.write_text('old');os.utime(p,(50,50))
        q=self.root/'clockstats';q.write_text('new');os.utime(q,(100,100))
        d=m.statistics_metrics(self.root,120);self.assertEqual(d['bytes']['clockstats'],6);self.assertEqual(d['age']['clockstats'],20)
        os.utime(q,(1000,1000));self.assertEqual(m.statistics_metrics(self.root,120)['ok'],0)

    def test_missing_invalid_and_forged_heartbeat_is_visible(self):
        path=self.root/'heartbeat';paths={'retention':path}
        self.assertEqual(m.job_metrics(paths,now=200)['retention_evidence'],0)
        path.write_text(json.dumps({'schema':1,'job':'retention','status':'success','completed_epoch':100}));path.chmod(0o600)
        real=os.fstat
        def root_owned(fd):
            info=real(fd);return types.SimpleNamespace(st_mode=info.st_mode,st_uid=0,st_size=info.st_size)
        with patch.object(m.os,'fstat',side_effect=root_owned):
            self.assertEqual(m.job_metrics(paths,200),{'retention_evidence':1,'retention_age':100})
        path.chmod(0o644);self.assertEqual(m.job_metrics(paths,200)['retention_evidence'],0)

    def test_profile_exact_selection_and_privilege(self):
        d=json.loads((ROOT/'node/profiles/ntp/profile.json').read_text())
        settings=(ROOT/d['settings']).read_text()
        self.assertEqual(d['root_plugins'],['ntp_statistics','ntp_jobs'])
        for name in d['custom_plugins']:
            self.assertTrue((ROOT/'node/plugins/ntp'/name).is_file());self.assertIn('['+name+']',settings)
        self.assertFalse(d['heartbeat_producers_deployed'])
        for kind in ('health','storage','statistics','jobs'):
            self.assertTrue(m.config(kind));self.assertTrue(all('\n' not in line for line in m.config(kind)))
        with self.assertRaises(SystemExit):m.main('storage',['/etc/shadow'])


if __name__=='__main__':unittest.main()
