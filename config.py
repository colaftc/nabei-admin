import os


basedir = os.path.abspath(os.path.dirname(__file__))
MONGODB_SETTINGS = {
    'db': 'nabei_admin',
    'host': 'localhost',
    'port': 27017,
}


class Config:
    SECRET_KEY = os.environ.get('NABEI_SECRET_KEY') or 'nabei_admin_fcp_erdianma'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = os.environ.get('SQLALCHEMY_COMMIT_ON_TEARDOWN') or True
    BABEL_DEFAULT_LOCALE = 'zh_CN'
    MONGODB_SETTINGS = MONGODB_SETTINGS


class ProductionConfig(Config):
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
    MYSQL_PASSWD = os.environ.get('MYSQL_PASSWD') or '123456'
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
    MYSQL_PORT = os.environ.get('MYSQL_PORT') or '3306'
    MYSQL_DATABASE_NAME = os.environ.get('MYSQL_DATABASE_NAME') or 'nabei_admin'
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URI') \
            or 'mysql+pymysql://{0}:{1}@{2}:{3}/{4}'.format(
                MYSQL_USER,
                MYSQL_PASSWD,
                MYSQL_HOST,
                MYSQL_PORT,
                MYSQL_DATABASE_NAME)


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEBUG_MYSQL_DATABASE_URI') \
                         or 'mysql+pymysql://root:fcp0520@localhost:3306/nabei_admin_debug'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TESTING_MYSQL_DATABASE_URI') \
                         or 'mysql+pymysql://root:fcp0520@localhost:3306/nabei_admin_testing'


config = {
    'production': ProductionConfig,
    'debug': DevConfig,
    'testing': TestingConfig,
}
