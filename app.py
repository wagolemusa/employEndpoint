from flask import Flask,jsonify,request, make_response
#from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
import jwt
import datetime
from functools import wraps
#import pyjwt

app = Flask(__name__)

app.config['SECRET_KEY'] = 'refuge'
empDB=[

{
    'id':'10',
    'username':'refuge',
    'password': 'wise12',
    'title':'Tevelling so much'

},
{
    'id':'20',
    'name':'Rajkubar',
    'title':'musa Software En'
}
]


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.args.get('token')=='':
            return jsonify({"message": 'You need to first Login'})
        try:
            data=jwt.decode(request.args.get('token'), app.config['SECRET_KEY'])

        except:
            return jsonify({"Alert":'please login again'})
        return f(*args, **kwargs)
    return decorated





@app.route('/')
def home():
    return "Hello refuge wise"

@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.get_json()['username']
    password = request.get_json()['password']
    if username == empDB[0]['username']:
        if password == empDB[0]['password']:
            token = jwt.encode({"username":username, "password":password, "exp":datetime.datetime.utcnow()+datetime.timedelta(minutes=20)},app.config['SECRET_KEY'])
            return jsonify({"token":token.decode('utf-8')})
        else:
            return jsonify({"message":"Invalid credentials"})
    else:
        return jsonify({"message":"Invalid credentials"})


# get employee 
@app.route('/empdb/employee', methods=['GET'])
@login_required
def getAllEmp():
    return jsonify({'emps': empDB})

# Specific employ
@app.route('/empdb/employee/<empId>', methods=['GET'])
def getEmp(empId):
    usr = [ emp for emp in empDB if (emp['id'] == empId)]
    return jsonify({'emp':usr})

#upating employee
@app.route('/empdb/employee_update/<empId>', methods=['PUT'])
def updateEmp(empId):
    em = [emp for emp in empDB if (emp['id'] == empId)]
    if 'name' in request.json:
        em [0]['name'] = request.json['name']
    if 'title' in request.json:
        em[0]['title'] = request.json['title']
    return jsonify({'emp':em[0]})

# post employee
@app.route('/empdb/employee_add', methods=['POST'])
def createEmp():
    data = {
    'id':request.json['id'],
    'name':request.json['name'],
    'title':request.json['title']
    }
    empDB.append(data)
    return jsonify(data)

# delete empyee datiels 
@app.route('/empdb/employee_delete/<empId>', methods=['DELETE'])
def deleteEmp(empId):
    em = [ emp for emp in empDB if (emp['id'] == empId)]
    empDB.remove(em[0])
    return jsonify({'response':'Success'})


if __name__ == '__main__':
    app.run()