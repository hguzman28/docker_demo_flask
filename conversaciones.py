import pymongo
import re
import datetime
import sys
from bson import ObjectId

class DB:

    def _init_(self):
        self.con = None
        self.var_ID_exist_conversacion= None
        self.var_check_last_conversacion= None
        self.var_ID_crear_conversacion=None
        self.var_check_message_unsend=None
        self.var_check_last_message_in= None
        self.var_check_lasts_message_in_db=None
        self.var_check_last_photo_in=None
        self.var_update_state_msg_unsend=None
        self.var_check_lasts_photo_in=None
        self.con_monitoreo=None
        self.var_check_last_conversacion_id=None
        self.var_check_lasts_video_in = None
        self.var_check_lasts_docs_in = None
        self.var_check_lasts_audio_in = None
        self.var_check_file_unsend = None
        
   
    def conect(self):
        #DB = "iContactdb"
        #URL_DB = ""
        client = pymongo.MongoClient("mongodb://hguzman:Abcd.1234@cluster0-shard-00-00-ot7rd.mongodb.net:27017,cluster0-shard-00-01-ot7rd.mongodb.net:27017,cluster0-shard-00-02-ot7rd.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
        db = client['iContactdb']
        self.con = db

    def exist_conversacion(self,origen): 
        print("exist_conversacion")
        self.conect()
        db = self.con
        col = db['conversaciones']

        query={"origen":origen,"estado":{"$in":["ATENDIENDO","NO_ATENDIDO"]}}
        result = col.find_one(query,{"_id":1})
        

        if db.conversaciones.count_documents(query) != 0:
            self.var_ID_exist_conversacion = result['_id']
            #return result['_id']
        else:
            self.var_ID_exist_conversacion=None

    def check_last_conversacion(self,nombreContacto_origen):
        print("check_conversacion_terminada"+str(nombreContacto_origen))
        self.conect()
        db = self.con
        col = db['conversaciones']

        query={"origen":nombreContacto_origen}
        result = col.find(query,{"estado":1}).sort([("_id", -1)]).limit(1)

        if db.conversaciones.count_documents(query) != 0:
            #return result
            self.var_check_last_conversacion = result
        else:
            self.var_check_last_conversacion = None

    def check_last_conversacion_id(self,nombreContacto_origen):

        self.conect()
        db = self.con
        col = db['conversaciones']

        query={"origen":nombreContacto_origen}
        result = col.find(query,{"_id":1}).sort([("_id", -1)]).limit(1)
        

        if db.conversaciones.count_documents(query) != 0:
            self.var_check_last_conversacion_id = result[0]['_id']
            #return result['_id']
        else:
            self.var_check_last_conversacion_id = None    

     

    def crear_conversacion(self,origen,canal,API): 
        print("crear_conversacion")
        self.conect()
        db = self.con
        col = db['conversaciones']

        query={"origen":origen,"estado":"NO_ATENDIDO","canal":canal,"API":API,"fecha":datetime.datetime.now()} 
        col.insert_one(query)

        self.exist_conversacion(origen)

        #return id
        self.var_ID_crear_conversacion = self.var_ID_exist_conversacion



    def insert_chat(self,mensaje,id,hora,id_msg,type_messege,channelId,platform,caption):
        print("insert_chat "+str(type_messege)+":"+str(mensaje))
        self.conect()
        db = self.con

        fecha_dt = datetime.datetime.now()

        col = db['mensajes']
        try:

            check_file = re.search("^http", str(mensaje))

            if check_file: 
                query={"_id":ObjectId(id_msg),"rol":"cliente","file":mensaje,"texto":caption,"conversacion":id,"estado":"NO_VISTO","fecha":fecha_dt,"canal":platform,"tipo":type_messege,"channelIdAPI":channelId}  
                col.insert_one(query)
            else:
                query={"_id":ObjectId(id_msg),"rol":"cliente","texto":mensaje,"conversacion":id,"estado":"NO_VISTO","fecha":fecha_dt,"canal":platform,"tipo":type_messege,"channelIdAPI":channelId}  
                col.insert_one(query) 

        except:
            print("Unexpected error:", sys.exc_info()[0]) 


        
        

    def insert_chatB(self,mensaje,id,hora,id_msg,type_messege,channelId,platform,caption):
        print("insert_chat "+str(type_messege)+":"+str(mensaje))
        self.conect()
        db = self.con

        fecha_dt = datetime.datetime.now()

        col = db['mensajes']
        try:

            check_file = re.search("^http", str(mensaje))

            #if caption == "sin_caption":

            if check_file: 
                query={"rol":"cliente","file":mensaje,"texto":caption,"conversacion":id,"estado":"NO_VISTO","fecha":fecha_dt,"canal":platform,"tipo":type_messege,"channelIdAPI":channelId}  
                col.insert_one(query)
            else:
                query={"rol":"cliente","texto":mensaje,"conversacion":id,"estado":"NO_VISTO","fecha":fecha_dt,"canal":platform,"tipo":type_messege,"channelIdAPI":channelId}  
                col.insert_one(query)
            #else:
                #query={"_id":id_msg,"rol":"cliente","file":mensaje,"texto":caption,"conversacion":id,"estado":"NO_VISTO","fecha":fecha_dt,"canal":platform,"tipo":type_messege,"channelIdAPI":channelId}  
                #col.insert_one(query) 

        except:
            print("Unexpected error:", sys.exc_info()[0])




    def insert_monitoreo(self):
        print("insert_monitoreo")
        self.conect_monitoreo()
        db = self.con_monitoreo

        conf = configparser.ConfigParser()
        conf.read(r'conf.ini')
        CLIENTE = conf['DATOS']['CLIENTE']

        col = db['monitoreo_whastapp']

        query={"empresa":CLIENTE,"ultima_iteracion":datetime.datetime.now()}

        col.insert_one(query)
             

    def check_message_unsend(self,id):
        print("check_message_unsend")
        self.conect()
        db = self.con
        col = db['mensajes']

        query={"rol":"agente","conversacion":id,"estado":"NO_VISTO","texto":{ "$regex": "^." }}
        

        docs = col.find(query,{"texto":1})

        if db.mensajes.count_documents(query) != 0:
            #return docs
            self.var_check_message_unsend = docs
        else:
            self.var_check_message_unsend = None

    def check_file_unsend(self,id):
        print("check_file_unsend")
        self.conect()
        db = self.con
        col = db['mensajes']

        query={"rol":"agente","conversacion":id,"estado":"NO_VISTO","file":{ "$regex": "^." }}
        

        docs = col.find(query,{"file":1})

        if db.mensajes.count_documents(query) != 0:
            #return docs
            self.var_check_file_unsend = docs
        else:
            self.var_check_file_unsend = None
            

    def check_last_message_in(self,id):
        print("check_last_message_in")
        
        self.conect()
        db = self.con
        col = db['mensajes']

        query={"rol":"cliente","conversacion":id,"texto":{ "$regex": "^." }}
        docs = col.find(query,{"texto":1,"_id":0}).sort([("_id", -1)]).limit(1)

        if col.count_documents(query) != 0:
            #return docs
            self.var_check_last_message_in = docs
        else:
            self.var_check_last_message_in = None


    def check_lasts_message_in_db(self,id):
        print("check_lasts_message_in_db")
        
        self.conect()
        db = self.con
        col = db['mensajes']

        query={"rol":"cliente","conversacion":id,"texto":{ "$regex": "^." }}
        docs = col.find(query,{"texto":1,"_id":0}).sort([("_id", -1)]).limit(10)

        if col.count_documents(query) != 0:
            #return docs
            self.var_check_lasts_message_in_db = docs
        else:
            self.var_check_lasts_message_in_db = None     


    def check_last_photo_in(self,id):
        print("check_last_photo_in")
        
        self.conect()
        db = self.con
        col = db['mensajes']

        query={"rol":"cliente","conversacion":id,"imagen":{ "$regex": "^." }}
        docs = col.find(query,{"imagen":1,"_id":0}).sort([("_id", -1)]).limit(1)

        if col.count_documents(query) != 0:
            #return docs
            self.var_check_last_photo_in = docs
        else:
            self.var_check_last_photo_in = None

    def check_lasts_photo_in(self,id):
        print("check_lasts_photo_in")
        
        self.conect()
        db = self.con
        col = db['mensajes']

        query={"rol":"cliente","conversacion":id,"imagen":{ "$regex": "^." }}
        docs = col.find(query,{"imagen":1,"_id":0}).sort([("_id", -1)]).limit(5)

        if col.count_documents(query) != 0:
            #return docs
            self.var_check_lasts_photo_in = docs
        else:
            self.var_check_lasts_photo_in = None

    def check_lasts_video_in(self,id):
        print("check_lasts_video_in")
        
        self.conect()
        db = self.con
        col = db['mensajes']

        query={"rol":"cliente","conversacion":id,"texto":{ "$regex": "^." }}
        docs = col.find(query,{"texto":1,"_id":0}).sort([("_id", -1)]).limit(5)

        if col.count_documents(query) != 0:
            #return docs
            self.var_check_lasts_video_in = docs
        else:
            self.var_check_lasts_video_in = None

    def check_lasts_docs_in(self,id):
        print("check_lasts_docs_in")
        
        self.conect()
        db = self.con
        col = db['mensajes']

        query={"rol":"cliente","conversacion":id,"texto":{ "$regex": "^." }}
        docs = col.find(query,{"texto":1,"_id":0}).sort([("_id", -1)]).limit(10)

        if col.count_documents(query) != 0:
            #return docs
            self.var_check_lasts_docs_in = docs
        else:
            self.var_check_lasts_docs_in = None

    def check_lasts_audio_in(self,id):
        print("check_lasts_audio_in")
        
        self.conect()
        db = self.con
        col = db['mensajes']

        query={"rol":"cliente","conversacion":id,"texto":{ "$regex": "^." }}
        docs = col.find(query,{"texto":1,"_id":0}).sort([("_id", -1)]).limit(5)

        if col.count_documents(query) != 0:
            #return docs
            self.var_check_lasts_audio_in = docs
        else:
            self.var_check_lasts_audio_in = None                  


    def update_state_msg_unsend(self,id,texto):
        self.conect()
        db = self.con
        col = db['mensajes']

        query={"rol":"agente","conversacion":id,"estado":"NO_VISTO","texto":texto}
        new_state = { "$set": { "estado":"VISTO" } }

        col.update_many(query,new_state)

    def update_state_file_unsend(self,id,texto):
        self.conect()
        db = self.con
        col = db['mensajes']

        query={"rol":"agente","conversacion":id,"estado":"NO_VISTO","imagen":texto}
        new_state = { "$set": { "estado":"VISTO" } }

        col.update_many(query,new_state)    
