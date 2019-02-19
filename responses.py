# -*- coding: utf-8 -*-
import json

from flask import Response


def make_response(body, status_code):
    response = Response(json.dumps(body, ensure_ascii=False), status=status_code,
                        mimetype='application/json')
    response.headers['Server'] = 'AirTradex v1.0'
    return response
