# mqtt_temp_mongo_web
Uses rabbitmq to take the CPU temp from a number of pis through a client program.  Then a server program listens to the queue, pulls it from the queue puts it into a Mongo DB.  Then another program collects it from Mongo and displays it in graph form via web page.

Client uses the pika modules
Server uses the pike and pymongo modules
Web program uses math, matplotlib, numpy, and tenacity
