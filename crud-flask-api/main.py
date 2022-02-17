from flask import Flask , request, jsonify
from flask_sqlalchemy import SQLAlchemy

DATABASE_URI = 'sqlite:///users.db'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
db = SQLAlchemy(app)
#create table using class that stand for ORM
class Todo(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String)

    def __repr__(self):
        return f'Todo("{self.name}")'

@app.route('/todos' , methods=['GET' , 'POST'])
def todos():
    if request.method == 'GET':
        todos = Todo.query.all()
        result = []
        for todo in todos:
            dict={}
            dict['id'] = todo.id
            dict['name'] = todo.name
            dict['description'] = todo.description
            result.append(dict)
        return jsonify({
            "data": result
        })
    if request.method == 'POST':
        id=request.json.get('id')
        name = request.json.get('name')
        description = request.json.get('description')
        todo = Todo(id = id , name = name , description = description)
        db.session.add(todo)
        db.session.commit()
        return jsonify({
            "status": "success",
            "data": f"{name} added successfully"
        }), 201

@app.route('/todos/<int:id>' , methods=['GET' , 'PUT' , 'DELETE'])
def mod_todo(id):
    todo = Todo.query.filter_by(id=id).first()
    if request.method == 'GET':
        dict = {}
        dict['id'] = todo.id
        dict['name'] = todo.name
        dict['description'] = todo.description
        return jsonify( {
          "data": dict
        })
    if request.method == 'PUT':
        todo.name = request.json.get('name')
        todo.description = request.json.get('description')

        db.session.commit()
        return jsonify({
            "status": "success",
            "data": "user updated successfully"
        })
    if request.method == 'DELETE':
        db.session.delete(todo)
        db.session.commit()
        return jsonify({
            "status": "success",
            "data": "user delete successfully"
        })



@app.route('/')
def hello_world():
    return 'Hello World!'
db.create_all()
app.run(debug=True)