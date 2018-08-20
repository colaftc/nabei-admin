from app.models import Expenditure, ExpenditureType
from extentions import exts


db = exts['db']


class RepositoryInterface(object):
    def add(self):
        raise NotImplemented

    def all(self, item):
        raise  NotImplemented

    def get_or(self, id, default=None):
        raise NotImplemented

    def get_by(self, name):
        raise NotImplemented

    def remove(self, item):
        raise NotImplemented


class RepoMixin(RepositoryInterface):
    def __init__(self, model, by='name'):
        super(RepoMixin, self).__init__()
        self.model = model
        self._by = getattr(self.model, by)

    @property
    def by(self):
        return self._by

    def all(self):
        return db.session.query(self.model).all()

    def get_or(self, id, default=None):
        return db.session.query(self.model).get(id) or default

    def remove(self, item):
        db.session.delete(item)
        db.session.commit()

    def get_by(self, val):
        return db.session.query(self.model).filter(self._by.like(val)).all()


class ExpenditureRepository(RepoMixin):
    def __init__(self, page_size=10, by='name'):
        super(ExpenditureRepository, self).__init__(ExpenditureType, by)
        self._by = getattr(self.model, by)
        self.page_size = page_size

    @property
    def by(self):
        return self._by

    def add(self, name):
        if not ExpenditureType.query.filter_by(name=name).first():
            db.session.add(ExpenditureType(name=name))
            db.session.commit()
