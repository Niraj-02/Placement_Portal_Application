from flask import Flask
from flask_cors import CORS
from json import jsonify 

app = Flask(__name__)
CORS(app)

from flask_restful import Api, Resource

api = Api(app)

class Index(Resource):
    def get(self):
        return jsonify({"message": "Hello, World!"}) 
api.add_resource(Index, "/")



if __name__ == "__main__":
    app.run(debug=True)