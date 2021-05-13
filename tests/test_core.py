import sqlite3
import unittest
from core import Ledger
class CoreTests(unittest.TestCase):
    def setUp(self): self.l=Ledger(':memory:'); self.addCleanup(self.l.close)
    def test_lifecycle(self):
        self.l.start('a',{'rate':0.1}); self.l.metric('a','loss',0,0.5); self.l.finish('a')
        self.assertEqual(self.l.runs()[0]['status'],'finished')
    def test_duplicate_step(self):
        self.l.start('a',{}); self.l.metric('a','x',0,1)
        with self.assertRaises(sqlite3.IntegrityError): self.l.metric('a','x',0,2)
    def test_terminal_is_closed(self):
        self.l.start('a',{}); self.l.finish('a','failed')
        with self.assertRaises(ValueError): self.l.metric('a','x',0,1)
