# -*- coding:utf8

from flask import Flask,request
from config import config
from extentions import exts

def create_app(config_name):
    app=Flask(__name__)
    app.config.from_object(config[config_name])

    for k,v in exts.items():
        v.init_app(app)

    return app
