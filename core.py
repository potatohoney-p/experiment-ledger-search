import json
import math
import sqlite3
class Ledger:
    def __init__(self,path):
        self.db=sqlite3.connect(path)
        self.db.executescript('CREATE TABLE IF NOT EXISTS runs (id TEXT PRIMARY KEY, params TEXT, status TEXT); CREATE TABLE IF NOT EXISTS metrics (run TEXT, name TEXT, step INTEGER, value REAL, PRIMARY KEY(run,name,step));')
    def close(self): self.db.close()
    def start(self,run,params):
        if not isinstance(run,str) or not run: raise ValueError('Run id required')
        payload=json.dumps(params,sort_keys=True,allow_nan=False)
        with self.db: self.db.execute('INSERT INTO runs VALUES (?,?,?)',(run,payload,'running'))
    def metric(self,run,name,step,value):
        row=self.db.execute('SELECT status FROM runs WHERE id=?',(run,)).fetchone()
        if row is None or row[0]!='running': raise ValueError('Run is not active')
        if not name or not isinstance(step,int) or step<0 or not math.isfinite(value): raise ValueError('Invalid metric')
        with self.db: self.db.execute('INSERT INTO metrics VALUES (?,?,?,?)',(run,name,step,value))
    def finish(self,run,status='finished'):
        if status not in ('finished','failed'): raise ValueError('Invalid terminal status')
        with self.db:
            cursor=self.db.execute('UPDATE runs SET status=? WHERE id=? AND status=?',(status,run,'running'))
            if cursor.rowcount!=1: raise ValueError('Run is not active')
    def runs(self):
        return [{'id':i,'params':json.loads(p),'status':s} for i,p,s in self.db.execute('SELECT * FROM runs ORDER BY id')]
