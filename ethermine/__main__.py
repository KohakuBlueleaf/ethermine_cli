import os,sys
import shutil

from argparse import ArgumentParser, RawTextHelpFormatter
from textwrap import dedent
from .ethermine import *
from json import dump


parser = ArgumentParser(formatter_class=RawTextHelpFormatter)
parser.add_argument(
  'command',
  help=dedent('''\
             stat: monitor the stat of a miner(need -I to be set)
             convert: convert log.json to log.csv(need -F to be set)'''),
  type=str, default='stat'
)
parser.add_argument(
  '-I', '--id',
  help='your ETH address',
  type=str, default=''
)
parser.add_argument(
  '-W','--worker',
  help='print workers\' data.',
  action='store_true', default=False
)
parser.add_argument(
  '-L','--log',
  help='save the log of every worker(valid shares).',
  action='store_true', default=False
)
parser.add_argument(
  '-P','--path',
  help='the path of log',
  type=str, default=os.getcwd()
)
parser.add_argument(
  '-T','--time',
  help='time between refresh data. (second)',
  type=int, default=60
)
parser.add_argument(
  '-F','--file',
  help='log to convert(log.json->csv)',
  type=str, default=''
)
parser.add_argument(
  '-O','--out',
  help='convert output file',
  type=str, default=''
)

def stat(args):
  if args.id == '':
    raise ValueError('id is not set')
  path = args.path.strip('/')
  while True:
    get_stat(args.id, True, args.worker, args.log, path)
    sleep(args.time)

def convert(args):
  file = args.file
  output = args.out
  if not output:
    output = file.replace('.json','.csv')
  json2csv(file, output)

def main():
  args = parser.parse_args()
  if args.command:
    try:
      globals()[args.command](args)
    except KeyboardInterrupt:
      return 
  

if __name__=='__main__':
  main()