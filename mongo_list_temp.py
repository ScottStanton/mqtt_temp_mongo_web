#!/usr/bin/python3
#
# This software is covered by The Unlicense license
#

import os, pymongo, sys


def print_mongo():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["cpu_temperature"]
    mycol = mydb["temps"]

    #print(myclient.list_database_names())
    for x in mycol.find():
        print(x) 
    myclient.close()



def main():
    print_mongo()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
