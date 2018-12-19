import jwt
import logging

def tokenGenerator(payload, secret):
  try:
    token = jwt.encode(payload, secret, algorithm='HS256')
    print(token)
    return token
  except:
    logging.exception('Error')