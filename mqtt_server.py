#!/usr/bin/python3
import os, pika, pymongo, sys


def insert_mongo(takentime, hostname, temp):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["cpu_temperature"]
    mycol = mydb["temps"]

    mydict = { "time": takentime, "hostname": hostname, "temp": temp }
    #print(mydict)

    x = mycol.insert_one(mydict)
    #print(myclient.list_database_names())
    #for x in mycol.find():
    #    print(x) 
    myclient.close()

def callback(body):
    values = str(body).strip('b').strip("'").split(',')
    #print(body)
    print(values) 
    insert_mongo(values[0], values[1], values[2])


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='cpu_temperature')

    while True:
        method_frame, header_frame, body = channel.basic_get(queue = 'cpu_temperature')
        if method_frame is None:
            break
        else:
            callback(body) 

    channel.queue_delete(queue = 'cpu_temperature')
    connection.close()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
