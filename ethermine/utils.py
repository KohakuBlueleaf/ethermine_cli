from datetime import datetime

def print_block(*args):
  args = [i.split('\n') for i in args]
  max_len = max(len(i) for i in args)

  new = []
  before = []
  before_len = max_len
  for block in args:
    now_len = len(block)
    if before_len+now_len<max_len:
      before.append(block)
      before_len += now_len
    else:
      space_line = ((max_len-before_len)//max(1,(len(before)-1)))
      new.append([j for i in before for j in i+['']*space_line])
      before = [block]
      before_len = now_len
  space_line = ((max_len-before_len)//max(1,(len(before)-1)))
  new.append([j for i in before for j in i+['']*space_line])
  new = new[1:]

  separator = ' '.join('{}' for _ in new)

  output = ''
  for i in range(max_len):
    output += separator.format(*[j[i] for j in new])
    output += '\n'
  
  print(output, end='')

def s2h(s):
  return round(s/3600,1)

def t2d(timestamp):
  return str(datetime.fromtimestamp(timestamp))

def dict2table(data):
  workers = [i for i in data['workers'].keys()]

  table = [['時間']]
  table[0] += workers

  for t, d in data.items():
    if t=='workers':
      continue
    table.append([t]+[d[name] for name in workers])
  
  return table