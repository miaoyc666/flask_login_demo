#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File name    : __init__.py
Author       : miaoyc
Create date  : 2022/3/23 3:04 下午
Description  : 
"""

import os
import redis as redis_cli
from flask import Flask, Request, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_redis import FlaskRedis
from flask.signals import Namespace

from sites.common.session_handle import RedisSessionInterface


class CustomRequest(Request):
    """
    subclass Request, handle request remote_addr problem
    """

    @property
    def remote_addr(self):
        """The remote address of the client."""
        client_ip_str = self.headers.get(
            'X-Forwarded-For', self.environ.get('REMOTE_ADDR'))
        return client_ip_str.split(',')[0]


app = Flask(__name__)
app.request_class = CustomRequest
conf_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "config.py")
app.config.from_pyfile(conf_path)
db = SQLAlchemy(app)
redis = FlaskRedis(app)

login_manager = LoginManager()
login_manager.init_app(app)
app.session_interface = RedisSessionInterface(app.config['SESSION_REDIS'],
                                              app.config.get('SESSION_KEY_PREFIX', 'session:'),
                                              app.config.get('SESSION_USE_SIGNER', False),
                                              app.config['SESSION_PERMANENT'])

# 信号量
my_signals = Namespace()
user_login_signal = my_signals.signal('user-login-signal')
user_logout_signal = my_signals.signal('user-logout-signal')


def register_blueprint():
    pass

register_blueprint()

login_manager.login_view = 'home.login'


def create_db():
    db.create_all()

create_db()
