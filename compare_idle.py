#!/usr/bin/python
import sys
import string
import re
import os

user = [-1] * 256
nice = [-1] * 256
system = [-1] * 256
idle = [-1] * 256
cpu_online = [-1] * 256
siblings = {}

def read_stat(stat_path):
        fh = open(stat_path)
        for line in fh.readlines():
          values = line.split(' ')
          cpu = re.search('[-+]?\d+', line).group(0)
          user.insert(int(cpu), long(values[1]))
          nice.insert(int(cpu), long(values[2]))
          system.insert(int(cpu), long(values[3]))
          idle.insert(int(cpu), long(values[4]))
          cpu_online.insert(int(cpu), 1)

def read_topo(topo_path):
        fh = open(topo_path)
        for line in fh.readlines():
          values = line.split(':')
          info = values[1]
          pair = info.split(',')
          cpu = pair[0]
          sib = pair[1]
          siblings[int(cpu)] = int(sib)

def verify_cpu():
        match = 1
        for cpu in siblings:
          sib = siblings.get(cpu)
          if cpu_online[cpu] != 1:
              continue
          if cpu_online[sib] != 1:
              continue
          busy = user[int(cpu)] + nice[int(cpu)] + system[int(cpu)]
          if(busy > idle[int(cpu)]):
            is_cpu_busy = 1
          else:
            is_cpu_busy = 0
          busy = user[int(sib)] + nice[int(sib)] + system[int(sib)]
          if(busy > idle[int(sib)]):
            is_sib_busy = 1
          else:
            is_sib_busy = 0
          if (is_cpu_busy != is_sib_busy):
              continue
          else:
            print("cpu(%d)(%d) not match with sibling(%d)(%d)!" % (cpu,is_cpu_busy,sib,is_sib_busy))
            match = 0
        if (match == 1):
            print("CPUs are busy while their siblings are idle!")

def printHelp():
        print('')
        print('  -h help')
        print('  -stat /proc/stat file')
        print('  -topo your topology file')
        print('')
        return True

# ----------------- MAIN --------------------
# exec start (skipped if script is loaded as library)
if __name__ == '__main__':
    args = iter(sys.argv[1:])
    for arg in args:
      if(arg == '-h'):
        printHelp()
      elif(arg == '-stat'):
        try:
          val = args.next()
          read_stat(val)
        except:
          print('Read /proc/stat file failed')
      elif(arg == '-topo'):
        try:
          val = args.next()
          read_topo(val)
        except:
          print('Read topology file failed')
      else:
          print('Invalid argument: '+arg)
    verify_cpu()
