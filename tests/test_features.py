import hashlib
import os
import tempfile
import unittest
from core import Ledger
from features import best,search,artifact_digest
class FeatureTests(unittest.TestCase):
    def test_last_metric_and_filter(self):
        l=Ledger(':memory:'); self.addCleanup(l.close)
        for name,value in [('a',0.2),('b',0.4)]:
            l.start(name,{'model':'linear'}); l.metric(name,'loss',0,9); l.metric(name,'loss',1,value); l.finish(name)
        self.assertEqual(best(l,'loss'),('a',0.2)); self.assertEqual(best(l,'loss',False),('b',0.4))
        self.assertEqual(len(search(l,{'model':'linear'})),2); self.assertEqual(search(l,{'model':'tree'}),[])
    def test_digest(self):
        with tempfile.TemporaryDirectory() as d:
            p=os.path.join(d,'model');
            with open(p,'wb') as f: f.write(b'weights')
            self.assertEqual(artifact_digest(p),hashlib.sha256(b'weights').hexdigest())
