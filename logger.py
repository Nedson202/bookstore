import logging
import os
import datetime

if not os.path.isdir('Logs'):
  os.mkdir('Logs')

logging.basicConfig(filename=f'Logs/log-{datetime.datetime.now().strftime("%Y-%m-%d")}.log', level=logging.INFO)