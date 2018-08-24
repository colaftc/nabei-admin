from app.models import ExpenditureType, ExpenditureDocument
from extentions import exts


db = exts['db']
mdb = exts['mdb']


class RepositoryInterface(object):
    def add(self, item):
        raise NotImplemented

    def all(self):
        raise  NotImplemented

    def get_or(self, id, default=None):
        raise NotImplemented

    def get_by(self, name):
        raise NotImplemented

    def remove(self, item):
        raise NotImplemented


class ExpenditureRepo(RepositoryInterface):
    def add(self, name, amount, category=None):
        item = ExpenditureDocument(name=name, amount=amount, category=category)
        item.save()
        return item

    def all(self):
        return ExpenditureDocument.objects.all()

    def get_or(self, identity, default=None):
        return ExpenditureDocument.objects(name=identity).first() or default

    def get_by(self, name):
        return self.get_or(name)

    def remove(self, condition={}):
        ExpenditureDocument.objects(**condition).delete()


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
