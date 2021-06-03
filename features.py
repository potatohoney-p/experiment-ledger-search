import hashlib
def artifact_digest(path):
    digest=hashlib.sha256()
    with open(path,'rb') as stream:
        while True:
            block=stream.read(65536)
            if not block: break
            digest.update(block)
    return digest.hexdigest()
def search(ledger,required):
    return [r for r in ledger.runs() if all(r['params'].get(k)==v for k,v in required.items())]
def best(ledger,name,minimize=True):
    candidates=[]
    for run in ledger.runs():
        if run['status']!='finished': continue
        row=ledger.db.execute('SELECT value FROM metrics WHERE run=? AND name=? ORDER BY step DESC LIMIT 1',(run['id'],name)).fetchone()
        if row: candidates.append((run['id'],row[0]))
    return min(candidates,key=lambda p:(p[1] if minimize else -p[1],p[0])) if candidates else None
