from flask import Flask, jsonify, request

class Mclientes:
  
    def return_clientes(self):
        clientes = {'nombre':'Henner', 'apellido':'guzman'}
        return clientes