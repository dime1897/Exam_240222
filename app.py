from flask import Flask, render_template, request
from flask_restful import Resource, Api
from wtforms import Form, IntegerField, StringField, validators, SubmitField
from exam import Name_of_class

app = Flask(__name__,
            static_url_path='/static', 
            static_folder='static')
dao=Name_of_class()

api = Api(app)
basePath = '/api/v1'

class Base_Handling(Resource):
    def get(self):
        pass
    def post(self):
        pass
    def put(self):
        pass


class Clean_DB(Resource):
    def get(self):
        dao.clean_db()
        return None, 200
    

api.add_resource(Base_Handling, f'{basePath}/pathototheapi')
api.add_resource(Clean_DB, f'{basePath}/clean')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)