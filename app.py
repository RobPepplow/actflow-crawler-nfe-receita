from flask import Flask, request, jsonify
from flask_cors import CORS
from nfeDownload import crawlerUpdate
from nfeEmitidas import crawlerAgendarEmitidas
from nfeDestinadas import crawlerAgendarDestinadas
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)

@app.route('/')
def resposta():
    return "A Api de Nfe - Paraná esta no Ar"

@app.route('/api/crawler/nfe/download', methods=['POST'])
def update():
    data = request.get_json()

    id = data['id']
    userNfeReceitaPr = data['userNfeReceitaPr']
    passwordNfeReceitaPr = data['passwordNfeReceitaPr']
    documentNumber = data['documentNumber']
    documentNumberOffice = data['documentNumberOffice']
    escritorioId = data['escritorioId']
    empresaId = data['empresaId']
    razaoSocial = data['razaoSocial']
    requestNumber = data['requestNumber']
    referenceDate = data['referenceDate']

    dados = crawlerUpdate(
        id=id,
        userNfeReceitaPr=userNfeReceitaPr,
        passwordNfeReceitaPr=passwordNfeReceitaPr,
        documentNumber=documentNumber,
        documentNumberOffice=documentNumberOffice,
        escritorioId=escritorioId,
        empresaId=empresaId,
        razaoSocial=razaoSocial,
        requestNumber=requestNumber,
        referenceDate=referenceDate,
    )

    if dados:
        return jsonify(dados)
    else:
        return 'Nenhum resultado encontrado.'

@app.route('/api/crawler/nfe/emitidas', methods=['POST'])
def Emitidas():
    data = request.get_json()

    userNfeReceitaPr = data['userNfeReceitaPr']
    passwordNfeReceitaPr = data['passwordNfeReceitaPr']
    documentNumber = data['documentNumber']
    documentNumberOffice = data['documentNumberOffice']
    escritorioId = data['escritorioId']
    empresaId = data['empresaId']
    razaoSocial = data['razaoSocial']
    initialDate = data['initialDate']
    endDate = data['endDate']

    dados = crawlerAgendarEmitidas(
        userNfeReceitaPr=userNfeReceitaPr,
        passwordNfeReceitaPr=passwordNfeReceitaPr,
        documentNumber=documentNumber,
        documentNumberOffice=documentNumberOffice,
        escritorioId=escritorioId,
        empresaId=empresaId,
        razaoSocial=razaoSocial,
        initialDate=initialDate,
        endDate=endDate,
    )

    if dados:
        return jsonify(dados)
    else:
        splitDate = initialDate.split('/')
        formattedDate = splitDate[1] + '/' + splitDate[2]
        data_hora_atual = datetime.now()
       
        formato = "%d/%m/%Y %H:%M:%S"
        atualDate = data_hora_atual.strftime(formato)
        filterDate = f"{initialDate} 00:00:00 a {endDate} 23:59:59"

        print(atualDate) 

        resultado_encontrado = {
            "filterDate": filterDate,
            "countInvoices": 'Não tem',
            "documentNumber": documentNumber,
            "docType": "Emitidas",
            "description": "Cnpj Não Cadastrado",
            "escritorioId": escritorioId,
            "empresaId": empresaId,
            "requestNumber": "Não tem",
            "documentNumberOffice": documentNumberOffice,
            "processDate": "Não tem",
            "requestDate": atualDate,
            "referenceDate": formattedDate,
            "razaoSocial": razaoSocial,
            "urlFile": 'Não tem',
            "msg": "CNPJ Não Cadastrado no Receita-Pr",
        }

        print("Resultado encontrado:")
        print(json.dumps(resultado_encontrado, indent=2, ensure_ascii=False).encode('utf-8').decode('utf-8'))        
        return resultado_encontrado 

@app.route('/api/crawler/nfe/destinadas', methods=['POST'])
def Destinadas():
    data = request.get_json()

    userNfeReceitaPr = data['userNfeReceitaPr']
    passwordNfeReceitaPr = data['passwordNfeReceitaPr']
    documentNumber = data['documentNumber']
    documentNumberOffice = data['documentNumberOffice']
    escritorioId = data['escritorioId']
    empresaId = data['empresaId']
    razaoSocial = data['razaoSocial']
    initialDate = data['initialDate']
    endDate = data['endDate']

    dados = crawlerAgendarDestinadas(
        userNfeReceitaPr=userNfeReceitaPr,
        passwordNfeReceitaPr=passwordNfeReceitaPr,
        documentNumber=documentNumber,
        documentNumberOffice=documentNumberOffice,
        escritorioId=escritorioId,
        empresaId=empresaId,
        razaoSocial=razaoSocial,
        initialDate=initialDate,
        endDate=endDate,
    )

    if dados:
        return jsonify(dados)
    else:       
        splitDate = initialDate.split('/')
        formattedDate = splitDate[1] + '/' + splitDate[2]
        data_hora_atual = datetime.now()
       
        formato = "%d/%m/%Y %H:%M:%S"
        atualDate = data_hora_atual.strftime(formato)
        filterDate = f"{initialDate} 00:00:00 a {endDate} 23:59:59"

        print(atualDate) 

        resultado_encontrado = {
            "filterDate": filterDate,
            "countInvoices": 'Não tem',
            "documentNumber": documentNumber,
            "docType": "Destinadas",
            "description": "Cnpj Não Cadastrado",
            "escritorioId": escritorioId,
            "empresaId": empresaId,
            "requestNumber": "Não tem",
            "documentNumberOffice": documentNumberOffice,
            "processDate": "Não tem",
            "requestDate": atualDate,
            "referenceDate": formattedDate,
            "razaoSocial": razaoSocial,
            "urlFile": 'Não tem',
            "msg": "CNPJ Não Cadastrado no Receita-Pr",
        }

        print("Resultado encontrado:")
        print(json.dumps(resultado_encontrado, indent=2, ensure_ascii=False).encode('utf-8').decode('utf-8'))        
        return resultado_encontrado 


