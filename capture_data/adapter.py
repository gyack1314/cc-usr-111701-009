import json
def decode(raw, manifest):
    doc=json.loads(raw.decode('utf-8'));filing=doc['filing_id']
    records=[{'kind':'filing','id':filing,'version':'received','refs':[],
              'payload':{'documents':doc['documents'],'source_url':manifest['source_url']}}]
    for context in doc['contexts']:
        records.append({'kind':'context','id':context['id'],'version':filing,'refs':[filing],
                        'payload':context})
    for unit in doc['units']:
        records.append({'kind':'unit','id':unit['id'],'version':filing,'refs':[filing],
                        'payload':unit})
    for fact in doc['facts']:
        records.append({'kind':'fact','id':fact['id'],'version':filing,
                        'refs':[fact['contextRef'],fact['unitRef']], 'payload':fact})
    return {'protocol':manifest['protocol'],'collection':manifest['collection'],'records':records}
