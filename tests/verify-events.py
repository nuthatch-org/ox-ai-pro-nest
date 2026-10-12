#!/usr/bin/env python3
"""Compare exposed event records with independently ABI-decoded Polygon logs.
NUTHATCH_RPC and NEST_ENDPOINT come from the environment, never from arguments.
Use --logs with a saved JSON array for an offline reference. Does not run mappings.
"""
import argparse,json,os,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DEPLOYMENT='QmbzwJnre963f9wT9VCJPede69vaniAKWVHzUEsAmBfrHG'
parser=argparse.ArgumentParser();parser.add_argument('--logs',type=Path);parser.add_argument('--from-block',type=int,default=88711689);parser.add_argument('--to-block',type=int,default=88811689);args=parser.parse_args()
def post(url,body):
 return json.load(urllib.request.urlopen(urllib.request.Request(url,data=json.dumps(body).encode(),headers={'Content-Type':'application/json'}),timeout=30))
if args.logs:logs=json.loads(args.logs.read_text())
else:
 r=post(os.environ['NUTHATCH_RPC'],{'jsonrpc':'2.0','id':1,'method':'eth_getLogs','params':[{'address':'0x5f511f9ad5c7b3d68d1f86444a5b7a32459fbb5a','fromBlock':hex(args.from_block),'toBlock':hex(args.to_block)}]})
 assert isinstance(r.get('result'),list),r.get('error');logs=r['result']
assert logs,'The reference returned no logs; that is not a passing comparison.'
abi=json.loads((ROOT/'abis/ox_ai_pro.json').read_text())
registry=json.loads((ROOT/'schema.json').read_text())['tables']
topics={t['topic0']:t['event'].split('(')[0] for t in registry}
abis={x['name']:x for x in abi if x.get('type')=='event'}
expected={k:[] for k in ['subscriptionEvents','rewards','rankUpEvents','campaignWins','monthSnapshotEntities','transfers','withdrawals','deposits']}
def decode(log):
 name=topics.get(log['topics'][0]);
 if name is None:return None,{}
 data=bytes.fromhex(log['data'][2:]);si=0;ti=1;v={}
 for f in abis[name]['inputs']:
  if f['indexed']:word=bytes.fromhex(log['topics'][ti][2:]);ti+=1
  else:word=data[si*32:(si+1)*32];si+=1
  t=f['type'];n=int.from_bytes(word,'big')
  if t.startswith('uint'):v[f['name']]=str(n)
  elif t=='address':v[f['name']]='0x'+word[-20:].hex()
  elif t=='bytes32':v[f['name']]='0x'+word.hex()
  elif t=='bool':v[f['name']]=bool(n)
  elif t=='string':length=int.from_bytes(data[n:n+32],'big');v[f['name']]=data[n+32:n+32+length].decode()
  else:v[f['name']]=None
 return name,v
for log in logs:
 if log.get('removed'):raise AssertionError('Removed logs are not a settled reference')
 name,v=decode(log)
 row={'id':log['transactionHash']+'-'+str(int(log['logIndex'],16)),'timestamp':str(int(log['blockTimestamp'],16)),'block':str(int(log['blockNumber'],16)),'txHash':log['transactionHash']}
 relation=lambda x:{'id':v[x]}
 if name=='Subscribed':
  row.update(member=relation('userId'),amount=v['usdValue'],currency=int(v['currency']),firstSub=v['firstSub'],sponsorId=v['sponsorId']);root='subscriptionEvents'
 elif name=='RewardBooked':
  row.pop('block');row.update(upline=relation('uplineId'),fromUserId=v['fromUserId'],pb=v['pb'],pc=v['pc']);root='rewards'
 elif name=='RankUp':row.update(member=relation('userId'),newRank=int(v['newRank']));root='rankUpEvents'
 elif name=='CampaignReward':row.pop('block');row.update(member=relation('userId'),amount=v['amount']);root='campaignWins'
 elif name=='MonthSnapshot':
  row={'id':v['monthId'],'timestamp':row['timestamp'],**v};root='monthSnapshotEntities'
 elif name in ['PBTransferred','PBSent']:
  send=name=='PBSent';row.update(kind='send' if send else 'park',fromMember=relation('fromUserId'),fromUserId=v['fromUserId'],toEmailHash=None if send else v['toEmailHash'],toUserId=v['toUserId'] if send else None,toMember=relation('toUserId') if send else None,amount=v['amount']);root='transfers'
 elif name in ['WithdrawPB','WithdrawPBAs','WithdrawPC']:
  pc=name=='WithdrawPC';row.update(member=relation('userId'),userId=v['userId'],asset='PC' if pc else 'PB',kind={'WithdrawPB':'USDT','WithdrawPBAs':'TOKEN','WithdrawPC':'PC'}[name],to=v['to'],amount=v['usd'],usdtOut=v['tokenAmountOut'] if name=='WithdrawPB' else None,tokenOut=None if pc else v['tokenOut']);root='withdrawals'
 elif name=='UsdtDeposited':row.update(v);root='deposits'
 else:continue
 expected[root].append(row)
endpoint=os.environ.get('NEST_ENDPOINT','http://127.0.0.1:8288/subgraphs/id/'+DEPLOYMENT)
fields={
 'subscriptionEvents':'id member { id } amount currency firstSub sponsorId timestamp block txHash',
 'rewards':'id upline { id } fromUserId pb pc timestamp txHash',
 'rankUpEvents':'id member { id } newRank timestamp block txHash',
 'campaignWins':'id member { id } amount timestamp txHash',
 'monthSnapshotEntities':'id monthId rddDistributed rddCount ldDistributed ldCount timestamp',
 'transfers':'id kind fromMember { id } fromUserId toEmailHash toUserId toMember { id } amount timestamp block txHash',
 'withdrawals':'id member { id } userId asset kind to amount usdtOut tokenOut timestamp block txHash',
 'deposits':'id from amount message timestamp block txHash',
}
compared=0
for root,rows in expected.items():
 for start in range(0,len(rows),100):
  chunk=rows[start:start+100];ids=[r['id'] for r in chunk]
  q='{ '+root+'(first: 100, where: {id_in: '+json.dumps(ids)+'}) { '+fields[root]+' } }'
  answer=post(endpoint,{'query':q});assert not answer.get('errors'),answer
  actual={r['id']:r for r in answer['data'][root]};want={r['id']:r for r in chunk}
  assert actual==want,(root,'missing',set(want)-set(actual),'unexpected',set(actual)-set(want),next(((k,want[k],actual.get(k)) for k in want if want[k]!=actual.get(k)),None))
  compared+=len(chunk)
 print(root,len(rows),'compared')
assert compared>0
refused=post(endpoint,{'query':'{ members(first: 1) { id totalPbEarned teamVolume } }'})
assert refused.get('errors') and not refused.get('data'),refused
for q in ['{ globals(first: 1) { id totalMembers } }','{ directorRewards(first: 1) { id amount } }','{ memberMonthVolumes(first: 1) { id volume } }']:
 r=post(endpoint,{'query':q});assert r.get('errors') and not r.get('data'),r
print('PASS',compared,'records; all accounting queries refused')
