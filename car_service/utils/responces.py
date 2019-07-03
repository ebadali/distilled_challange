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


def getFailResponse(reason=None):
    response = {'status': 'failure', 'error': reason}
    return jsonify(response), 404


def getSuccessResponse(data=None, sessionvalue=None, userdata=None, msg=None,favs=None):
    response = {
        'status': 'success',
        'data': data,
        'sessionkey': sessionvalue,
        'users': userdata,
        'message': msg}

    if favs:
        response['favs'] = favs
        
    return jsonify(response), 200
