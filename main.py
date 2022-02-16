from flask import Flask, render_template,jsonify,request
import os
import conversaciones

db = conversaciones.DB()

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])

def home():
    if (request.method=='POST'): 
        some_json = request.get_json()
        print(some_json)
        #return render_template('~/iLinkzi/docker_pruebas/app_demo/index.html')
        db.exist_conversacion(some_json['origen'])
        
        if db.var_ID_exist_conversacion:
            
            db.insert_chat2(some_json['mensaje'],db.var_ID_exist_conversacion,some_json['fecha'],"test","test","test","test")
            return jsonify({"registro":"exitoso","conversacion":"conocida","ID":str(db.var_ID_exist_conversacion)})
        else:
            db.crear_conversacion(some_json['origen'])
            db.insert_chat2(some_json['mensaje'],db.var_ID_crear_conversacion,some_json['fecha'],"test","test","test","test")
            return jsonify({"registro":"exitoso","conversacion":"nueva","ID":str(db.var_ID_crear_conversacion)})
        #return "Hola2"

    else:
        return "{'respuesta':'ok'}"  


#if __name__ == "__main__":
#    port = int(os.environ.get('PORT', 5000))
#    app.run(debug=True, host='0.0.0.0', port=port)