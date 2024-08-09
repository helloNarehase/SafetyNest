from binascii import hexlify
from hashlib import sha512
from os import urandom
import sqlite3

from flask import Flask, request, jsonify
from flask import Flask
import uuid

import yaml

app = Flask(__name__)
users = []

class User:
    def __init__(self, id:str, pwd:str, name:str, uuid:str) -> None:
        self._id_ = id
        self._pwd_ = pwd
        self._name_ = name
        self._uuid_ = uuid

    @classmethod
    def create_User(cls, id:str, pwd:str, name:str) -> 'User':
        return cls(id, sha512(pwd.encode("UTF-8")), name, uuid.uuid4().hex)
    
    @property
    def ID(self):
        return self._id_
    
    @property
    def UUID(self):
        return self._uuid_
    
    def equal(self, hash_pwd) -> bool:
        return self._pwd_ == hash_pwd
    
    def OutDict(self) -> dict:
        return {"identity" : self._id_, "name" : self._name_, "pwd" : self._pwd_, "uuid" : self._uuid_}

def id_equal(A, ID):
    for i in A:
        if i.ID == ID:
            return True
    return False

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    id = data.get('id')
    print(id)
    if len(users) > 0 and id_equal(users, str(id)):
        return jsonify({"UUID": "0000"})
    else: 
        username = data.get('username')
        password = data.get('password')

        userObject = User.create_User(id, password, username)
        users.append(userObject)
        return jsonify({"UUID": userObject.UUID})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port = 6000)
    