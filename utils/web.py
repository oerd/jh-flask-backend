from flask import request

import logging

logger = logging.getLogger('sample_app')


def request_wants_json(only_json=True):
    best = request.accept_mimetypes .best_match(['application/json', 'text/html'])
    print('Request best matches: %s' % (best,))
    print('Request best: %s' % (request.accept_mimetypes[best],))
    print('Request best: %s' % (request.accept_mimetypes['text/html'],))
    print(request.accept_mimetypes)
    if only_json:
        return best == 'application/json'
    return best == 'application/json' and request.accept_mimetypes[best] > request.accept_mimetypes['text/html']
