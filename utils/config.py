import os


def read_file(file):
  try:
    return open(file, 'r').readline()
  except:
    return None

client_id_file = read_file('/run/secrets/github_client')
client_secret_file = read_file('/run/secrets/github_client_secret')
client_id_env = os.environ['GITHUB_CLIENT']
client_secret_env = os.environ['GITHUB_CLIENT_SECRET']

def get_github_client():
  return client_id_file or client_id_env

def get_github_client_secret():
  return client_secret_file or client_secret_env
