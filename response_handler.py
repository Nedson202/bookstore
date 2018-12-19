from flask import Response, json

def response_handler(new_book, status, message):
    response = Response(json.dumps(
      {
        'error': False,
        'status': status,
        'data': new_book,
        'message': message
      }
    ), status, mimetype='application/json')
    return response

def error_response_handler(error, status):
  response = Response(json.dumps(
    {
      'error': True,
      'status': status,
      'data': error
    }
  ), status, mimetype='application/json')
  return response