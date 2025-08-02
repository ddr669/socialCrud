#from django.test import TestCase

# Create your tests here.

import requests

def get_user_list(
                url: str = 'http://127.0.0.1:8000/users/',
                headers={'Authorization': 'Token  04b5f'}
                ) -> requests.Response:
    '''
        Just authenticated users can
        List all other users.
    '''
    return requests.get(url, headers=headers)
    

def update_user(
                url: str = 'http://127.0.0.1:8000/users/',
                id: str = '9',
                headers={'Authorization': 'Token  04b5f'},
                payload={}
                ) -> requests.Response:
    '''
        just authenticated ( TOKEN | BasicAuth ) can 
        Update himself.
    '''
    return requests.patch(url+str(id)+'/', headers=headers, data=payload)

def create_user(
                url: str = 'http://127.0.0.1:8000/users/',
                headers={'Authorization': 'Token  04b5f'},
                payload={}
                ) -> requests.Response:
    ''' everyone can create a account. '''

    return requests.post(url, headers=headers, data=payload)
def delete_user(
                url: str = 'http://127.0.0.1:8000/users/',
                headers={'Authorization': 'Token  04b5f'},
                id: str = '0',
                payload={}
                ) -> requests.Response:
    ''' Only authenticated and owner or admin user. '''
    return requests.delete(url+str(id)+'/', headers=headers)

print(delete_user(id='10').json()) # unauthorized error 401