from flask import Flask,jsonify,request
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
import jwt
class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

users = [
    User(1, 'user1', 'abcxyz'),
    User(2, 'user2', 'abcxyz'),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}

def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'

jwt = JWT(app, authenticate, identity)



empDB=[

{
    'id':'10',
    'name':'savanaj',
    'title':'Tevelling so much'
},
{
    'id':'20',
    'name':'Rajkubar',
    'title':'musa Software En'
}
]

@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity


@app.route('/')
def home():
    return "Hello refuge wise"
# get employee 
@app.route('/empdb/employee', methods=['GET'])
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