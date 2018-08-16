from flask_babelex import Babel
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin

exts={
    'db':SQLAlchemy(),
    'admin':Admin(),
    'babel':Babel(),
}
