from crypt import methods
from flask import Flask, render_template,jsonify,request,redirect
import os
import pymongo
import time
from bson import ObjectId


#db = conversaciones.DB()

app = Flask(__name__)

#Routes
#from clientes import routes


def connDb():
    url = os.environ.get('MONGO_URL')
    print(url) 
    #client = pymongo.MongoClient("mongodb://hguzman:Abcd.1234@cluster0-shard-00-00-ot7rd.mongodb.net:27017,cluster0-shard-00-01-ot7rd.mongodb.net:27017,cluster0-shard-00-02-ot7rd.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
    client = pymongo.MongoClient(url)
    db = client['iContactdb']

    return db

@app.route('/', methods=['GET'])
def home():

    db = connDb()
    r = db.test.find()

    return render_template('index.html', nombres=list(r))


      
@app.route('/filtro', methods=['POST'])
def filtro():

    _nombre = request.form['nombre']
    db = connDb()
    r = db.test.find({'nombre': { '$regex': str(_nombre)} } )

    return render_template('index.html',nombres=list(r))

@app.route('/eliminar/<_id>')
def eliminar(_id):
    db = connDb()

    db.test.delete_one({'_id':ObjectId(_id)})

    return redirect('/')

@app.route('/agregarForm')
def agregarForm():
    
    return render_template('agregar.html')

@app.route('/agregar', methods=['post'])
def agregar():
    _nombre = str(request.form['nombre'])
    _apellido = str(request.form['apellido'])
    _cc = str(request.form['cc'])


    db = connDb()

    db.test.insert_one({'nombre':_nombre,'apellido':_apellido,'cc':_cc})  

    return redirect('/')


  


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)