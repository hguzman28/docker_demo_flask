#import clientes.clientes as cliente
from flask import Flask, jsonify, request, session, redirect
from app import app
from clientes.models import Mclientes

@app.route('/cliente', methods=['GET'])
def show_clientes():
    modelo = Mclientes()
    data = modelo.return_clientes()
    return data
