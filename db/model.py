# -*- coding: utf-8 -*-
import shutil
from pathlib import Path

from flask_login import UserMixin, current_user
from sqlalchemy import MetaData, func
from flask_sqlalchemy import SQLAlchemy

from config import *

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)


class Review(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    review = db.Column(db.String(1024), nullable=False)
    visible = db.Column(db.Boolean, nullable=False, default=False)
    date = db.Column(db.DateTime(timezone=True), server_default=func.now())


def db_init():
    dbs = [REVIEW_DATABASE_NAME]

    # Check if db file already exists. If so, backup it
    for db_ in dbs:
        db_file = Path(db_)
        if db_file.is_file():
            shutil.copyfile(db_, '_'.join(db_.split('_').insert(-1, 'BACKUP')))

        # Init DB
        db.session.commit()  # https://stackoverflow.com/questions/24289808/drop-all-freezes-in-flask-with-sqlalchemy
        db.drop_all()
        db.create_all()
