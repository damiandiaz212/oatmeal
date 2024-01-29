import os

def get_alpha_key(local=False):
    if local:
        file = open('ALPHA_KEY.txt', "r")
        lines = file.readlines()
        file.close()
        return lines[0]
    return os.environ['ALPHA_KEY']

def get_db_creds(local=False):
    if local:
        file = open('DB_EXTERNAL.txt', "r")
        lines = file.readlines()
        file.close()
        return lines[0]
    return  os.environ['DB_INTERNAL']


def format_sse(data: str, event=None) -> str:
    msg = f'data: {data}\n\n'
    if event is not None:
        msg = f'event: {event}\n{msg}'
    return msg
