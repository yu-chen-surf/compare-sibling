#!/usr/bin/python
import sys
import string
import re
import os

def read_cstat(stat_path):
        poll_time=0
        other_time=0
        cur_time=0
        fh = open(stat_path)
        for line in fh.readlines():
          time_tmp = re.search('time', line)
          if time_tmp is None:
            continue
          time=time_tmp.group(0)
          values = line.split('.')

          time = values[2].split(' ')
          cur_time = int(time[1])

          poll = re.search('POLL', line)
          if poll:
              poll_time=poll_time+int(cur_time)
          else:
              other_time=other_time+int(cur_time)
        print('POLL: %d' %poll_time)
        print('CSTATES: %d' %other_time)

def printHelp():
        print('')
        print('  -h help')
        print('  -f file')
        print('')
        return True

# ----------------- MAIN --------------------
# exec start (skipped if script is loaded as library)
if __name__ == '__main__':
    args = iter(sys.argv[1:])
    for arg in args:
      if(arg == '-h'):
        printHelp()
      elif(arg == '-f'):
        try:
          val = args.next()
          read_cstat(val)
        except:
          print('Read file failed')
      else:
          print('Invalid argument: '+arg)
