# -*- coding:utf8

from flask import Flask, request
from config import config
from extentions import exts


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    for k, v in exts.items():
        v.init_app(app)

    @app.errorhandler(404)
    def page_not_found(e):
        if request.accept_mimetypes.accept_json and \
                not request.accept_mimetypes.accept_html:

            app.logger.warn('an json client accept and 404')
            response = jsonify({'error': 'object not found'})
            response.status_code = 404
            return response

        else:
            app.logger.warn('an html client accept and 404')
            return "<html><body><h1>Sorry , Object Not Found</h1></body></html>", 404

    @app.before_request
    def app_before_request():
        pass

    return app


from . import models
