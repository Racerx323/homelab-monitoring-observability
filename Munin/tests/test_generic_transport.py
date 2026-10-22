#!/usr/bin/python3
"""Offline exact-set transition and CDEF contracts for undeployed candidates."""
import importlib.machinery
import importlib.util
import io
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    path = ROOT/'master/plugins'/name
    loader = importlib.machinery.SourceFileLoader(name, str(path))
    spec = importlib.util.spec_from_loader(name, loader)
    obj = importlib.util.module_from_spec(spec)
    loader.exec_module(obj)
    return obj


base = load('ntp_transport_j2')
compatible = load('ntp_transport_j2.compatible.candidate')
expanded = load('ntp_transport_j2.expanded.candidate')
selection = set(json.loads((ROOT/'node/profiles/ntp/generic-parity.candidate.json').read_text())['requires_coordinated_master_expected_set'])
original = set(json.loads((ROOT/'node/profiles/ntp/generic-expansion.candidate-manifest.json').read_text())['old_plugins'])


class Protocol:
    def __init__(self, raw):
        self.stream = io.BytesIO(raw)
        self.sent = []

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def bind(self, source):
        self.source = source

    def connect(self, target):
        self.target = target

    def settimeout(self, timeout):
        self.timeout = timeout

    def makefile(self, *args):
        return self.stream

    def sendall(self, raw):
        self.sent.append(raw)


def transcript(names, value='1'):
    rows = ['# munin node at j2-svntp1', 'cap multigraph', ' '.join(sorted(names))]
    for name in sorted(names):
        rows += ['multigraph '+name, 'graph_title test', 'raw.label Raw', 'raw.cdef raw,8,*',
                 'derived.label Derived', 'derived.cdef raw,2,*', '.',
                 'multigraph '+name, 'raw.value '+value, '.']
    return ('\n'.join(rows)+'\n').encode()


class GenericTransportTests(unittest.TestCase):
    def test_compatible_accepts_only_exact_old_or_expanded_sets(self):
        self.assertEqual(set(compatible.PLUGIN_SETS), {frozenset(original), frozenset(selection)})
        for names in (original, selection):
            for endpoint in compatible.ENDPOINTS:
                stream = Protocol(transcript(names))
                self.assertEqual(compatible.check(endpoint, lambda *args: stream), 1)
                self.assertEqual(stream.source, (endpoint[2], 0))
                self.assertEqual(stream.target, (endpoint[1], 4949))
                self.assertEqual(sum(x.startswith(b'fetch ') for x in stream.sent), len(names))

    def test_no_partial_or_arbitrary_superset(self):
        for names in (selection-{'ntp_health'}, selection-{'acpi'}, selection|{'foreign'}, original|{'acpi'}):
            with self.assertRaises(ValueError):
                compatible.check(compatible.ENDPOINTS[0], lambda *args: Protocol(transcript(names)))

    def test_finalized_candidate_rejects_old_set(self):
        self.assertEqual(expanded.PLUGIN_SETS, (frozenset(selection),))
        self.assertEqual(expanded.check(expanded.ENDPOINTS[0], lambda *args: Protocol(transcript(selection))), 1)
        with self.assertRaises(ValueError):
            expanded.check(expanded.ENDPOINTS[0], lambda *args: Protocol(transcript(original)))

    def test_raw_self_cdef_is_required_computed_only_field_is_not(self):
        raw = transcript(selection)
        for bad in (raw.replace(b'raw.value 1', b'other.value 1', 1),
                    raw.replace(b'raw.value 1', b'raw.value 1\nraw.value 1', 1),
                    raw.replace(b'raw.value 1', b'raw.value garbage', 1)):
            with self.assertRaises(ValueError):
                expanded.check(expanded.ENDPOINTS[0], lambda *args: Protocol(bad))

    def test_unknown_is_transport_data_not_health_or_submission_success(self):
        self.assertEqual(expanded.check(expanded.ENDPOINTS[0], lambda *args: Protocol(transcript(selection, 'U'))), 1)
        self.assertIn('v6.critical 1:1', expanded.config())
        self.assertEqual(expanded.ENDPOINTS, base.ENDPOINTS)


if __name__ == '__main__':
    unittest.main()
