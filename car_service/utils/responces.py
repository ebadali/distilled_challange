# -*- coding: utf-8 -*-


''' Responder suit: Single point of controll for the API Responses'''

from flask import jsonify


def getFailResponse(reason=None,error=404):
    response = {'status': 'failure', 'error': reason}
    return jsonify(response), error


def getSuccessResponse(data=None,message_code=200):
    response = {
        'status': 'success',
        'data': data,
    }
        
    return jsonify(response), message_code
