from flask import request

import logging

logger = logging.getLogger('sample_app')


def request_wants_json(ignore_rest=True):
    best = request.accept_mimetypes .best_match(['application/json', 'text/html'])
    if ignore_rest:
        return best == 'application/json'
    return best == 'application/json' and request.accept_mimetypes[best] > request.accept_mimetypes['text/html']
