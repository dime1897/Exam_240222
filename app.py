from flask import Flask, render_template, request
from flask_restful import Resource, Api
from wtforms import Form, IntegerField, StringField, validators, SubmitField, SelectField, BooleanField
from exam import UaaS

app = Flask(__name__,
            static_url_path='/static', 
            static_folder='static')
dao=UaaS()

api = Api(app)
basePath = '/api/v1'
umarell_fields = ['nome', 'cognome', 'cap']
cantiere_fields = ['indirizzo', 'cap']

class FilterForm(Form):
    cap = IntegerField('CAP: ', [validators.number_range(0,99999)])
    umarell = BooleanField('UMARELL')
    cantieri = BooleanField('CANTIERI')
    submit = SubmitField('FILTRA')
class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

def validate_cantiere(cantiere:dict) -> bool:
    try:
        if len(cantiere.keys()) != len(cantiere_fields): return False
        for field in cantiere.keys():
            if not field in cantiere_fields: return False
        if not isinstance(cantiere['cap'], int) or cantiere['cap'] < 0 or cantiere['cap'] > 99999: return False
        return True
    except: return False

def validate_umarell(umarell:dict) -> bool:
    try:
        if len(umarell.keys()) != len(umarell_fields): return False
        for field in umarell.keys():
            if not field in umarell_fields: return False
        if not isinstance(umarell['cap'], int) or umarell['cap'] < 0 or umarell['cap'] > 99999: return False
        return True
    except: return False

def validate_id(id:str):
    try:
        int(id)
        return True
    except: return False

class Cantiere(Resource):
    def get(self, id):
        if not validate_id(id): return None, 404
        cantiere = dao.get_cantiere(id)
        if cantiere is None: return None, 404
        return cantiere, 200
    def post(self, id):
        if not validate_id(id): return None, 400
        cantiere = request.json
        if not validate_cantiere(cantiere): return None, 400
        conflict = dao.get_cantiere(id)
        if not conflict is None: return None, 409
        rc = dao.insert_cantiere(cantiere, id)
        if rc is None: return None, 400
        return cantiere, 201

class Umarell(Resource):
    def get(self, id):
        if not validate_id(id): return None, 404
        umarell = dao.get_umarell(id)
        if umarell is None: return None, 404
        return umarell, 200
    def post(self, id):
        if not validate_id(id): return None, 400
        umarell = request.json
        if not validate_umarell(umarell): return None, 400
        conflict = dao.get_umarell(id)
        if not conflict is None: return None, 409
        rc = dao.insert_umarell(umarell, id)
        if rc is None: return None, 400
        return umarell, 201


class Clean_DB(Resource):
    def get(self):
        dao.clean_db()
        return None, 200
    

api.add_resource(Cantiere, f'{basePath}/cantiere/<id>')
api.add_resource(Umarell, f'{basePath}/umarell/<id>')
api.add_resource(Clean_DB, f'{basePath}/clean')

@app.route(f'{basePath}/list', methods = ['GET', 'POST'])
def gui():
    if request.method == 'GET':
        c = {}
        cform = FilterForm(obj=Struct(**c))
        return render_template('list_objects.html', c=0, u=0, cantieri=[], umarell=[], form=cform), 200
    if request.method == 'POST':
        cform = FilterForm(request.form)
        if not cform.umarell.data and not cform.cantieri.data: return render_template('list_objects.html', c=0, u=0, cantieri=[], umarell=[], form=cform), 200
        cantieri, umarell = dao.dump_db()
        if not cform.cap.data is None: 
            cantieri = [cn for cn in cantieri if cn['cap'] == cform.cap.data]
            umarell = [um for um in umarell if um['cap'] == cform.cap.data]

        if cform.umarell.data and cform.cantieri.data: return render_template('list_objects.html', c=1, u=1, cantieri=cantieri, umarell=umarell, form=cform), 200
        elif cform.umarell.data: return render_template('list_objects.html', c=0, u=1, cantieri=[], umarell=umarell, form=cform), 200
        else: return render_template('list_objects.html', c=1, u=0, cantieri=cantieri, umarell=[], form=cform), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)