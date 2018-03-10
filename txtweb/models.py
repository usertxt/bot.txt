from datetime import datetime
from txtweb import db
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError

def get_one_or_create(session,
                      model,
                      create_method='',
                      create_method_kwargs=None,
                      **kwargs):
    try:
        return session.query(model).filter_by(**kwargs).one(), False
    except NoResultFound:
        kwargs.update(create_method_kwargs or {})
        created = getattr(model, create_method, model)(**kwargs)
        try:
            session.add(created)
            session.flush()
            return created, True
        except IntegrityError:
            session.rollback()
            return session.query(model).filter_by(**kwargs).one(), True

class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.BigInteger, primary_key=True)
    nickname = db.Column(db.String(32), index=True, unique=True)
    discord_id = db.Column(db.String(128), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    avatar_uri = db.Column(db.String(256), index=False, unique=False)
    description = db.Column(db.String(1024), index=False, unique=False)
    posts = db.relationship('Article', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<Author %r>' % (self.nickname)

class Curator(db.Model):
    __tablename__ = 'curators'
    id = db.Column(db.BigInteger, primary_key=True)
    nickname = db.Column(db.String(32), index=True, unique=True)
    discord_id = db.Column(db.String(128), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    avatar_uri = db.Column(db.String(256), index=False, unique=False)
    description = db.Column(db.String(1024), index=False, unique=False)
    posts = db.relationship('Article', backref='curator', lazy='dynamic')

    def __repr__(self):
        return '<Curator %r>' % (self.nickname)

class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    curator_id = db.Column(db.Integer, db.ForeignKey('curators.id'))
    discord_msg_id = db.Column(db.String(128), index=True, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    title = db.Column('title', db.String(256))
    content_markdown = db.Column('content', db.String(1024))
    visible = db.Column(db.Boolean)

    def __repr__(self):
        return '<Article %r>' % (self.title)
