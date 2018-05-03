#!/usr/bin/env python3
import sys
import platform
from subprocess import Popen
import config

server_command = "import server, sys; server.start_server(sys.argv[1]);"
client_command = "import client, sys; client.start_client(sys.argv[1]);"

def start_new_process(command_str):
  msg = config.to_str()
  new_window_command = "x-terminal-emulator -e".split()
  echo = [sys.executable, "-c", command_str]
  process = Popen(new_window_command + echo + [msg])
  return process

def start_server():
  return start_new_process(server_command)

def start_client():
  return start_new_process(client_command)
  
