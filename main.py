#!/usr/bin/env python3
import sys, platform, time
import config
from subprocess import Popen
from _thread import *
import client

server_command = "import server, sys; server.start_server(sys.argv[1]);"
client_command = "import client, sys; client.start_client(sys.argv[1]);"
stats = {}

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

def get_avg_throughput():
  start_new_thread(start_server,())
  time.sleep(1)
  i = 5
  throughput = 0
  while i > 0:
    throughput += client.client(config)
    time.sleep(1)
    i -= 1
  throughput /= 5;
  config.TCP_PORT += 1
  return throughput

def generate_statistics():
  probabilities = [0.01, 0.05, 0.1, 0.3]
  window_sizes = [1, 10, 100, 500, 1000]
  config.TCP_PORT = 50000
  print('Testing Stop-and-Wait algorithm')
  config.algorithm = 'S&W'
  stats['S&W'] = {}
  for p in probabilities:    
    config.plp = config.pcp = p
    stats['S&W'][p] = get_avg_throughput()

  print('Testing Selective-Repeat algorithm')
  config.algorithm = 'SR'
  stats['SR'] = {}
  for ws in window_sizes:
    config.window_size = ws
    stats['SR'][ws] = {}
    for p in probabilities:    
      config.plp = config.pcp = p
      stats['SR'][ws][p] = get_avg_throughput()

  print('Testing Go-Back-N algorithm')
  config.algorithm = 'GBN'
  stats['GBN'] = {}
  for ws in window_sizes:
    config.window_size = ws
    stats['GBN'][ws] = {}
    for p in probabilities:    
      config.plp = config.pcp = p
      stats['GBN'][ws][p] = get_avg_throughput()

  print(stats['S&W'])
  print(stats['GBN'])
  print(stats['SR'])
  return stats
  
  