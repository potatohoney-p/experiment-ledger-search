import unittest
from core import Ledger
from features import best
class EdgeTests(unittest.TestCase):
    def test_no_finished_candidate(self):
        l=Ledger(':memory:'); self.addCleanup(l.close); l.start('a',{}); l.metric('a','loss',0,1)
        self.assertIsNone(best(l,'loss'))
    def test_nonfinite(self):
        l=Ledger(':memory:'); self.addCleanup(l.close); l.start('a',{})
        with self.assertRaises(ValueError): l.metric('a','loss',0,float('nan'))
    def test_missing_run(self):
        l=Ledger(':memory:'); self.addCleanup(l.close)
        with self.assertRaises(ValueError): l.finish('missing')
