#!/usr/bin/env python3
"""Run as root on Helsinki. Add this deployment's GraphQL-only public route."""
from pathlib import Path
import datetime,json,subprocess,urllib.request
DEP='QmbzwJnre963f9wT9VCJPede69vaniAKWVHzUEsAmBfrHG'
UPSTREAM='100.83.44.63:8312'
body=json.dumps({'query':'{ _meta { block { number timestamp } } subscriptionEvents(first: 1) { id } }'}).encode()
r=json.load(urllib.request.urlopen(urllib.request.Request('http://'+UPSTREAM+'/subgraphs/id/'+DEP,data=body,headers={'Content-Type':'application/json'}),timeout=30))
assert not r.get('errors') and r['data']['subscriptionEvents'],r
assert datetime.datetime.now(datetime.timezone.utc).timestamp()-r['data']['_meta']['block']['timestamp']<120,'upstream data is stale'
p=Path('/etc/caddy/Caddyfile');old=p.read_text()
marker='\t# openloom-bsc, graph-support#53'
assert 'subgraphs.nuthatch-indexer.com {' in old and marker in old
assert '\thandle /subgraphs/id/'+DEP not in old,'route already exists'
backup=p.with_name('Caddyfile.bak-ox-ai-pro-'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
backup.write_text(old)
route=f'''\t# OX AI PRO limited event-history stopgap, graph-support#57.
\thandle /subgraphs/id/{DEP} {{
\t\theader Access-Control-Allow-Origin "*"
\t\treverse_proxy {UPSTREAM}
\t}}
'''
try:
 p.write_text(old.replace(marker,route+marker,1))
 subprocess.run(['caddy','validate','--config',str(p),'--adapter','caddyfile'],check=True,capture_output=True)
 subprocess.run(['systemctl','reload','caddy'],check=True)
 url='https://subgraphs.nuthatch-indexer.com/subgraphs/id/'+DEP
 out=json.load(urllib.request.urlopen(urllib.request.Request(url,data=body,headers={'Content-Type':'application/json'}),timeout=30))
 assert not out.get('errors') and out['data']['subscriptionEvents'],out
 print('live:',url,'block',out['data']['_meta']['block']['number'],'backup:',backup)
except BaseException:
 p.write_text(old);subprocess.run(['systemctl','reload','caddy'],check=False);raise
