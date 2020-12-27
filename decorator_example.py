import os
import logging
import requests
import functools

def make_logger(logger_name=None):
    logger = logging.getLogger(logger_name)

    if len(logger.handlers) > 0:
        return logger

    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(filename=logger_name + '.log')
    stream_handler = logging.StreamHandler()
    
    file_handler.setLevel(logging.INFO)
    stream_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('\n[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')

    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger

logger = make_logger('api_log_information')

def logger_decorator(logger):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*func_args, **func_kwargs):
            logger.info('[REQUEST], params: {0}'.format(func_kwargs))
            result = func(*func_args, **func_kwargs)
            logger.info('[RESPONSE], {0}'.format(result))
            return result
        return wrapper
    return decorator

@logger_decorator(logger)
def call_api_server(data, api_url):
    api_dict = {}
    api_dict['data'] = data
    tempres = requests.post(api_url, json = api_dict)
    if tempres.status_code == 200:
        result = tempres.content
        return result

