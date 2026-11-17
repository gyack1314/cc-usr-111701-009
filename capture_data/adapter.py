"""保存 Inline XBRL XHTML 的事实引用。"""
from xml.etree import ElementTree as ET
IX='{http://www.xbrl.org/2013/inlineXBRL}'
XBRLI='{http://www.xbrl.org/2003/instance}'
def decode(raw,manifest):
    root=ET.fromstring(raw)
    records=[{'kind':'filing','id':manifest['collection'],'version':'received','refs':[],
              'payload':{'source_url':manifest['source_url'],'documents':['annual.html','notes.html']}}]
    for context in root.iter(XBRLI+'context'):
        identifier=context.find('.//'+XBRLI+'identifier')
        period=context.find(XBRLI+'period')
        records.append({'kind':'context','id':context.attrib['id'],'version':manifest['collection'],
                        'refs':[manifest['collection']],
                        'payload':{'entity':identifier.text if identifier is not None else None,
                                   'period':[x.text for x in period] if period is not None else []}})
    for unit in root.iter(XBRLI+'unit'):
        measure=unit.find(XBRLI+'measure')
        records.append({'kind':'unit','id':unit.attrib['id'],'version':manifest['collection'],
                        'refs':[manifest['collection']],
                        'payload':{'measure':measure.text if measure is not None else None}})
    for fact in root.iter(IX+'nonFraction'):
        records.append({'kind':'fact','id':fact.attrib['id'],'version':manifest['collection'],
                        'refs':[fact.attrib['contextRef'],fact.attrib['unitRef']],
                        'payload':{'name':fact.attrib['name'],'value':fact.text,
                                   'scale':fact.attrib.get('scale'),
                                   'continuation':fact.attrib.get('continuedAt')}})
    return {'protocol':manifest['protocol'],'collection':manifest['collection'],'records':records}
