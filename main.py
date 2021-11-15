from sqlalchemy.exc import IntegrityError

from app import app

import api

import views


from models.manage_school_db import InitSchoolDb


def db_initialization():
    db_manager = InitSchoolDb()
    db_manager.init_db()


if __name__ == '__main__':
    # db_initialization()

    app.run()
