# -*- coding:utf-8

# define the user interface for api authenticate

from itsdangerous import Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app


class ApiUserRepo:
    def __init__(self):
        self._data = (
            {
                'id': 101,
                'username': 'colaftc',
                'is_admin': True,
                'password': 'fcp0520'
            },
            {
                'id': 102,
                'username': 'fengcuiping85',
                'is_admin': True,
                'password': 'f05072021'
            },
        )

    def get(self, id):
        user = ApiUser(repo=self)
        for item in self._data:
            if item['id'] == id:
                user.username = item['username']
                user.id = item['id']
                user.is_admin = item['is_admin']
                user.password = item['password']

        return user


class ApiUser:
    def __init__(self, repo):
        self.repo = repo
        self._pwd = None
        self.username = None
        self._token = None
        self.id = 0
        self.is_login = False
        self.is_admin = True

    @staticmethod
    def load(identity):
        return ApiUserRepo().get(identity)

    @property
    def password(self):
        return self._pwd

    @password.setter
    def password(self, pwd):
        self._pwd = generate_password_hash(pwd)

    def authenticate(self, pwd):
        if check_password_hash(self._pwd, pwd):
            current_app.logger.info('user %s login', self.username)
            self.is_login = True
            return self.is_login
        else:
            current_app.logger.warning('login failed username : %s', self.username)
            return False

    def generate_token(self, expiration=15*60):
        if self.is_login:
            s = Serializer(current_app.config['SECRET_KEY'])
            self._token = s.dumps({'username': self.username, 'id': self.id})
            return self._token
        else:
            current_app.logger.warning('please get token after login')
            return None

    @property
    def token(self):
        return self._token

    def clone_from(self, other):
        self.username = other.username
        self.id = other.id
        self.is_login = other.is_login
        self._pwd = other.password
        self._token = other.token

    def verify_token(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)

        except:
            return False

        else:
            user = self.repo.get(data['id'])
            if data['username'] == user.username:
                current_app.logger.info('token ok, username : %s', user.username)
                self.clone_from(user)
                return True
            else:
                current_app.logger.warning('token wrong , username : %s', user.username)

            return False
