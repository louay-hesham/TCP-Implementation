#!/usr/bin/env python3
import sys
import platform
from subprocess import Popen
import config

def randomFunction():
  return "import server, sys; server.start_server(sys.argv[1]);"

msg = config.to_str()
new_window_command = "x-terminal-emulator -e".split()
echo = [sys.executable, "-c",randomFunction()]
process = Popen(new_window_command + echo + [msg])
process.wait()
