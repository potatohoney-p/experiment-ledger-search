import json
from core import Ledger
from features import best,search
with open('examples/input.json') as stream: rows=json.load(stream)
ledger=Ledger(':memory:')
try:
    for row in rows:
        ledger.start(row['id'],row['params'])
        for step,value in enumerate(row['loss']): ledger.metric(row['id'],'loss',step,value)
        ledger.finish(row['id'])
    print(json.dumps({'best':best(ledger,'loss'),'runs':search(ledger,{'model':'linear'})},sort_keys=True))
finally: ledger.close()
