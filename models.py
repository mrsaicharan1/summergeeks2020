import uuid

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from app import db

engine = create_engine('sqlite:///database.db', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def generate_uuid():
    return str(uuid.uuid4())[:4]


class Visitor(Base):
    __tablename__ = 'Visitor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    phone = db.Column(db.String(50))
    email = db.Column(db.String(120))
    check_in = db.Column(db.DateTime)
    check_out = db.Column(db.DateTime)
    uuid_code = db.Column(db.String(10))
    host_id = db.Column(db.Integer, db.ForeignKey('Host.id'))

    def __init__(self, name=None, role=None, phone=None, uuid_code=None, email=None, check_in=None, check_out=None, host_name=None):
        self.name = name
        self.phone = phone
        self.email = email
        self.check_in = check_in
        self.check_out = check_out
        self.uuid_code = generate_uuid()

class Host(Base):
    __tablename__ = 'Host'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    phone = db.Column(db.String(50))
    email = db.Column(db.String(120))
    check_in = db.Column(db.DateTime)
    check_out = db.Column(db.DateTime)
    uuid_code = db.Column(db.String(10))
    visitors = db.relationship('Visitor', backref='host')


    def __init__(self, name=None, phone=None, email=None, uuid_code=None, check_in=None, check_out=None):
        self.name = name
        self.phone = phone
        self.email = email
        self.check_in = check_in
        self.check_out = check_out
        self.uuid_code = generate_uuid()

# Create tables.
Base.metadata.create_all(bind=engine)
