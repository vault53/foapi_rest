import json

from flask import Flask
from flask_restful import Api, Resource
from kafka import (KafkaConsumer, KafkaProducer)

app = Flask(__name__)
api = Api(app)

api_prefix = '/v1/api'
component_prefix = '/consumables'

producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=lambda x:
    json.dumps(x).encode('utf-8')
)

consumer = KafkaConsumer(
    'rest_api_response',
    bootstrap_servers=['kafka:9092'],
    auto_offset_reset='earliest',
    enble_auto_commit=True,
    group_id='my_group',
    value_deserializer=lambda x:
    json.loads(x).decode('utf-8')
)


class Consumable(Resource):
    def get(self, cons_id=None):
        try:
            cons_id = int(cons_id)
        except ValueError:
            return {'error': ''}, 503
        producer.send(
            'rest_api_request',
            {
                "type": "item",
                "subtype": "consumable",
                "id": cons_id
            }
        )

        ret = consumer.poll()

        print(ret)

    def put(self, cons_id):
        pass

    def post(self, cons_id):
        pass


class Consumables(Resource):
    def get(self):
        return {}


api.add_resource(Consumable, '/consumable/<cons_id>')
api.add_resource(Consumables, '/consumables')

if __name__ == '__main__':
    app.run(debug=True)
