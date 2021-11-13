#!/usr/bin/python3
#
# This software is covered by The Unlicense license
#

import argparse
import json
import pika
import platform
import sys
import time
from datetime import date
from gpiozero import CPUTemperature

parser = argparse.ArgumentParser()

# Requires a json file for authentication paramters
# debug is optional

parser.add_argument('-j','--json', required=True,
       metavar='json_file', help="JSON file containing the mqtt information.")
parser.add_argument('-d','--debug', action='store_true', help="Show debugging messages on the command line")

args = parser.parse_args()
#print(args)

hostname = platform.node()

def debug_print(msg):
    if args.debug:
        print(f'DEBUG: {msg}')
#End debug_print

def current_time():
    now = time.localtime()
    now_hour = str(time.strftime("%H", now))
    now_min = str(time.strftime("%M", now))
    now_sec = str(time.strftime("%S", now))
    nowdate = date.today()
    return f'{nowdate} {now_hour}:{now_min}'
#End current_time()

def load_json(filename):
   with open(filename) as f:
       data = json.load(f)
       f.close()
   
   if 'user' in data.keys():
       debug_print('user = ' + data['user'])
   if 'passwd' in data.keys():
       debug_print('passwd = ' + data['passwd'])
   if 'ip' in data.keys():
       debug_print('ip = ' + data['ip'])
   return(data)
#End load_json

def send_mqtt(user,passwd,ip,port,mqtt_queue,message):
   credentials = pika.PlainCredentials(user, passwd)
   parameters = pika.ConnectionParameters(ip,port,'/',credentials)

   connection = pika.BlockingConnection(parameters)
   channel = connection.channel()
   channel.queue_declare(queue=mqtt_queue)

   channel.basic_publish(exchange='',routing_key=mqtt_queue,body=message)

   connection.close()
#End send_mqtt

def cpu_temp():
   cpuc = CPUTemperature()
   cpuf = (int(cpuc.temperature) * (9/5) +32)
   cpufs = str(f'{cpuf:.1f}')
   debug_print(cpufs)
   return(cpufs)
#End cpu_temp


if __name__ == '__main__':
   mqtt_data = load_json(args.json)
   ftemp = cpu_temp()
   now = current_time()
   body = f'{now},{hostname},{ftemp}'

   send_mqtt(mqtt_data['user'],mqtt_data['passwd'],mqtt_data['ip'],5672,'cpu_temperature',body)



