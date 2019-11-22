from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

api_prefix = '/v1/api'
component_prefix = '/consumables'


class Consumable(Resource):
    def get(self, cons_id=None):
        try:
            cons_id = int(cons_id)
        except ValueError:
            return {'error': ''}, 503
        if cons_id == 999:
            return

    def put(self, cons_id):
        pass

    def post(self, cons_id):
        pass


api.add_resource(Consumable, '/consumable/<cons_id>')

if __name__ == '__main__':
    app.run(debug=True)
