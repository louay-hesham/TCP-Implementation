#!/usr/bin/env python3
import sys, platform, time
import config
from subprocess import Popen
from _thread import *
import client

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

# def start_thread(func):
#   return pool.apply_async(func,(config))

def generate_statistics():
  start_new_thread(start_server,())
  time.sleep(2)
  c = client.client(config)
  for t in [s, c]:
    print(t)
  print('done')
  
