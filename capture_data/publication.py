"""事实字段接收与申报文档闭包分开。"""
def assess(rows):
    filings=[r for r in rows if r['kind']=='filing']
    facts=[r for r in rows if r['kind']=='fact']
    absent=[x for r in filings for x in r['payload']['documents'] if not r['payload'].get('verified_documents',{}).get(x)]
    continuation=[r['id'] for r in facts if r['payload'].get('continuation') and not r['payload'].get('continuation_resolved')]
    return {'publishable':not absent and not continuation,
            'reasons':['申报文档未核验:'+x for x in absent]+['事实续片未接收:'+x for x in continuation],
            'candidate_facts':len(facts)}
