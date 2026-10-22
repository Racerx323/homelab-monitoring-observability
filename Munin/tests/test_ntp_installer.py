"""Offline installer rendering and pre-mutation rejection checks."""
import importlib.util
from pathlib import Path
import types
import unittest
from unittest.mock import patch

SPEC=importlib.util.spec_from_file_location('installer',Path(__file__).resolve().parents[1]/'scripts/install_ntp_node.py')
m=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(m)


class InstallerTests(unittest.TestCase):
    def test_dual_stack_config_has_one_literal_port_per_address(self):
        raw=m.node_config('node.example',['192.0.2.51','fd00::51'],['192.0.2.83','fd00::83']).decode()
        self.assertIn('port 192.0.2.51:4949\n',raw);self.assertIn('port [fd00::51]:4949\n',raw)
        self.assertIn('allow ^192\\.0\\.2\\.83$\n',raw);self.assertNotIn('host *',raw)
        for hosts,allows in [(['*'],['192.0.2.1']),([],['192.0.2.1']),(['127.0.0.1'],[])]:
            with self.assertRaises(ValueError):m.node_config('node.example',hosts,allows)

    def test_nonroot_and_bad_host_recovery_submit_no_command(self):
        spec={'operation_id':'fixture','hostname':'expected','boot_id':'expected'}
        obj=m.Installer(spec,'digest')
        with patch.object(m.os,'geteuid',return_value=1000),patch.object(obj,'command') as command:
            with self.assertRaisesRegex(ValueError,'root/schema/profile'):obj.preflight()
            with self.assertRaisesRegex(ValueError,'recovery root/host/boot'):obj.recover()
            command.assert_not_called()
        with patch.object(m.os,'geteuid',return_value=0),patch.object(m.socket,'gethostname',return_value='foreign'),patch.object(obj,'command') as command:
            with self.assertRaisesRegex(ValueError,'recovery root/host/boot'):obj.recover()
            command.assert_not_called()

    def test_operation_identity_and_protected_set(self):
        with self.assertRaises(ValueError):m.Installer({'operation_id':'../outside'},'digest')
        obj=m.Installer({'operation_id':'fixture','schema':1,'profile':'ntp',
            'service_identity':{'ActiveState':'active','SubState':'running','MainPID':'42'},'protected_files':{}},'digest')
        with patch.object(m.os,'geteuid',return_value=0),patch.object(obj,'command') as command:
            with self.assertRaisesRegex(ValueError,'complete protected'):obj.preflight()
            command.assert_not_called()


if __name__=='__main__':unittest.main()
