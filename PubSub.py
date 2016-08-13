__author__ = '__naresh__'

from kombu import BrokerConnection, Exchange, Queue, Producer
import json


class PubSub(object):
    def __init__(self, username=None, password=None, host="localhost"):
        self.username = username
        self.password = password
        self.host = host
        self.virtual_host = "/"
        self.channel = None
        self.producer = None

    def connect(self):
        connection = BrokerConnection(hostname=self.host,
                                      userid=self.username,
                                      password=self.password,
                                      virtual_host=self.virtual_host)
        self.channel = connection.channel()
        return self.channel

    def create_exchange(self, exchange_name, exchange_type):
        return Exchange(exchange_name, type=exchange_type)

    def create_queue(self, queue_name, exchange, routing_key):
        return Queue(queue_name, exchange=exchange, routing_key=routing_key)

    def create_producer(self, queue, exchange):
        self.producer = Producer(channel=self.channel, exchange=exchange, routing_key=queue)

    def publish_message(self, message):
        json_data = json.dumps(message)
        x = self.producer.publish(json_data, content_type='application/json', serializer="json", compression="zlib", )
        return x


if __name__ == "__main__":
    obj = PubSub(username="guest", password="guest")
    obj.connect()
    exchange = obj.create_exchange("analytics", "topic")
    #queue = obj.create_queue("", exchange, routing_key="send.email")
    obj.create_producer("send.email", exchange)
    message = "Hi Naresh"
    obj.publish_message(message)
