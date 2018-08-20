import os
from app import create_app
from flask import request, jsonify, Response
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from extentions import exts


app = create_app(os.getenv('FLASK_CONFIG') or 'debug')
db = exts['db']
manager = Manager(app)
migrate = Migrate(app, db)


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


# @app.before_request()
# def app_before_request():
    # pass


def make_shell_context():
    return dict(app=app, db=db)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def create_blueprint():
    pass


if __name__ == '__main__':
    manager.run()
