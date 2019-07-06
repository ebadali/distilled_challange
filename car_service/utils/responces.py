# -*- coding: utf-8 -*-


''' Responder suit: Generate Response for apis'''

from flask import jsonify


def getResponce(status, message, sessionvalue):
    response = {}
    if status == "error":
        response = {'status': 'error', 'error': message}
    else:
        response = {
            'status': 'success',
            'sessionkey': sessionvalue,
            'message': message}
    return jsonify(response)


def getFailResponse(reason=None,error=404):
    response = {'status': 'failure', 'error': reason}
    return jsonify(response), error


def getSuccessResponse(data=None,message_code=200):
    response = {
        'status': 'success',
        'data': data,
    }
        
    return jsonify(response), message_code
