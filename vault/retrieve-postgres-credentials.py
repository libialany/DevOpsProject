# how o setup the plugin: https://developer.hashicorp.com/vault/docs/secrets/databases/postgresql
# video explanation: https://youtu.be/yUxvbJOtSTE?si=Q2H6X4nFSQtHcX_A
import hvac
import requests
import os
PATH = 'database/creds/test-role'

class Hvac:
  def __init__(self):
    self.url = self._get_url()
    self.token = self._get_token()
    self.client = hvac.Client(url=self.url, token=self.token)
  @staticmethod
  def _get_url():
    return os.getenv(key="VAULT_ADDR")


  @staticmethod
  def _get_token():
    return os.getenv(key="VAULT_TOKEN")

  def read_dynamic_pwd_with_hvac(self):
    response = self.client.read(PATH)
    if response and 'data' in response:
        secret_data = response['data']
        user = secret_data['username']
        password = secret_data['password']
        print(f"User: {user}, Password:  {password}")


if __name__ == '__main__':
    vault = Hvac() 
    print(vault.client.is_authenticated())
    vault.read_dynamic_pwd_with_hvac()
