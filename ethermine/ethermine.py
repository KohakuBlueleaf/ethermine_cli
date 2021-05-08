from requests import get
from json import loads, dump, dumps
from time import time,sleep
from os import system
import csv

from .utils import *


API = [
  'https://api.ethermine.org/miner/{}/dashboard',
  'https://api.ethermine.org/miner/{}/dashboard/payouts',
  'https://www.bitoex.com/api/v0/rate/{}',
  'https://api.ethermine.org/miner/{}/settings',
  'https://api.ethermine.org/miner/{}/worker/{}/history'
]
PAYTIME = [605100,1209900]
TEMPLATE = ['''┌────────────────┬─────────────┐
│現在算力(60m)   │ {:<7} MH/s│
├────────────────┼─────────────┤
│平均算力(24h)   │ {:<7} MH/s│
├────────────────┼─────────────┤
│礦機回報算力    │ {:<7} MH/s│
├────────────────┼─────────────┤
├────────────────┼─────────────┤
│預測日收益      │ {:<7} ETH │
│                │ {:<7} NTD │
├────────────────┼─────────────┤
│預測下次出金量  │ {:<7} ETH │
│                │ {:<7} NTD │
├────────────────┼─────────────┤
│距離下次出金    │ {:<7} hr  │
├────────────────┼─────────────┤
├────────────────┼─────────────┤
│BitoEX以太幣賣價│ {:<7} NTD │
└────────────────┴─────────────┘''',
'''┌─────────┬────────────────────┐
│礦機名稱 │ {:<19}│
├─────────┴──────┬─────────────┤
│現在算力(10m)   │ {:<7} MH/s│
├────────────────┼─────────────┤
│礦機回報算力    │ {:<7} MH/s│
├────────────────┼─────────────┤
│有效share(10m)  │ {:<11} │
└────────────────┴─────────────┘'''
]


def get_miner_stat(id):
  data = loads(get(API[0].format(id)).content)['data']
  pay = loads(get(API[1].format(id)).content)['data']
  setting = loads(get(API[3].format(id)).content)['data']

  hash2pay = pay['estimates']['coinsPerMin']/pay['estimates']['averageHashrate']
  all_hashrate = [i['currentHashrate'] for i in data['statistics']]

  avg_1h = sum(all_hashrate[-6:])/6
  avg_24h = sum(all_hashrate)/144
  report = data['currentStatistics']['reportedHashrate']

  unpaid = data['currentStatistics']['unpaid']
  threshold = setting['minPayout']
  if pay['payouts']:
    last_paid = pay['payouts'][0]['paidOn']
    
    next_paid_time = last_paid+PAYTIME[0]
    duration = next_paid_time-time()
    next_payout = duration/60*hash2pay*avg_24h+unpaid/1e18
    if next_payout<0.05:
      next_paid_time = last_paid+PAYTIME[1]
      duration = next_paid_time-time()
      next_payout = duration/60*hash2pay*avg_24h+unpaid/1e18
      if next_payout<0.01:
        duration = (threshold-unpaid)/1e18/(60*hash2pay*avg_24h)
        next_payout = threshold
  else:
    duration = (threshold-unpaid)/1e18/(60*hash2pay*avg_24h)
    next_payout = threshold

  daily_profit = 1440*hash2pay*avg_24h

  return report, avg_1h, avg_24h, daily_profit, next_payout, duration, data['workers']

def get_eth_stat():
  return int(loads(get(API[2].format(int(time()))).content)['ETH'][1].replace(',',''))

def get_workers_his(id, workers):
  his = {}
  for i in workers:
    data = loads(get(API[4].format(id, i)).content)['data']
    his[i] = {i['time']:i['validShares'] for i in data}
  
  return his

def get_stat(id, refresh=False, worker=False, log=False, path=None):
  re, a6, a24, dp, np, du, wr = get_miner_stat(id)
  price = get_eth_stat()
  workers = get_workers_his(id, (i['worker'] for i in wr))

  re, a6, a24 = round(re/1e6, 2),round(a6/1e6, 2),round(a24/1e6, 2)
  dp, np = round(dp,4), round(np, 4)
  
  profit = round(np*price)

  if refresh:
    system('cls')

  stat = TEMPLATE[0].format(
    a6,a24,re,
    dp, round(dp*price),
    np, round(np*price),
    s2h(du),
    price
  )
  if log:
    try:
      with open(path+'/log.json', 'r') as f:
        data = loads(f.read())
    except:
      data = {'workers':{i['worker']:0 for i in wr}}
    
    for name, his in workers.items():
      for time, shares in his.items():
        time_str = f'{t2d(time)}'
        now = eval(str(data.get(time_str, data['workers'])))
        now[name] = shares
        data[time_str] = now
    
    with open(path+'/log.json', 'w') as f:
      dump(data, f, indent=2)

  if worker:
    wrs = []
    for i in wr:
      wrs.append(TEMPLATE[1].format(
        i['worker'],
        round(i['currentHashrate']/1e6,2),
        round(i['reportedHashrate']/1e6,2),
        i['validShares']
      ))
    print_block(stat,*wrs[:6])
    if len(wrs)>6:
      temp = []
      for i in range(6,len(wrs)):
        temp.append(wrs[i])
        if len(temp)==4:
          print_block(*temp)
          temp = []
      print_block(*temp)
  else:
    print(stat)

def json2csv(file, output):
  with open(file, 'r') as f:
    data = loads(f.read())
  table = dict2table(data)
  with open(output, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(table)


if __name__=='__main__':
  while True:
    get_stat('0xb23f58fe9aa3165059116f01a50ba0d9fff6a189', True)
    sleep(60)