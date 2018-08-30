import os
from app import create_app
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from extentions import exts
from app.admin_view import ExpenditureTypeModelView
from app.models import ExpenditureType
from app.api import api_bp


app = create_app(os.getenv('FLASK_CONFIG') or 'debug')
db = exts['db']
mdb = exts['mdb']
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db)


def init_app(app):
    app.register_blueprint(api_bp, url_prefix='/api')


admin = exts['admin']
admin.name = '网店管理'
admin.add_view(ExpenditureTypeModelView(ExpenditureType, db.session, name='开支类别'))

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def create_blueprint():
    pass


if __name__ == '__main__':
    init_app(app)
    manager.run()
