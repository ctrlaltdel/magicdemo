#!/usr/bin/env python3

import os
import sys
import pty
import tty
import termios
import logging
from subprocess import Popen, PIPE, check_output

#logging.basicConfig(level=logging.DEBUG)

old = termios.tcgetattr(sys.stdin)
tty.setcbreak(sys.stdin)

try:
  master, slave = pty.openpty()
  shell = Popen(['/bin/bash', '-l', '-i'],
    stdin=slave,
    preexec_fn=os.setsid,
    env={
      'HOME': os.environ['HOME'],
      'TERM': os.environ['TERM'],
    }
  )
  pin = os.fdopen(master, 'w')

  #pin.write("alias cat='pygmentize'\n")
  #pin.write("alias diff='diff --color'\n")
  pin.write("clear\n")

  with open(sys.argv[1]) as f:
    while True:
      cmd = f.readline().strip()
      logging.debug("cmd: {}".format(repr(cmd)))
      i = 0

      # Skip shebang
      if cmd.startswith('#!'):
        continue

      # Skip comments
      if cmd.startswith('#'):
        continue

      if cmd == '':
        break

      # Wait for key presses
      while True:
        key = sys.stdin.read(1)

        if key == '\t':
          pin.write(cmd[i:])
          i = len(cmd)
        elif key == '\n' and i == len(cmd):
          pin.write('\n')
          break
        elif i < len(cmd):
          pin.write(cmd[i])
          i = i + 1

        pin.flush()

  # Wait for any key press before exiting
  key = sys.stdin.read(1)
  shell.kill()

except KeyboardInterrupt:
  shell.kill()

finally:
  termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old)
  print()
