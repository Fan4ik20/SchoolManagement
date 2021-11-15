from flask import Flask

from sqlalchemy import create_engine

app = Flask(__name__)


db_engine = create_engine(
    'postgresql+psycopg2://tester:tester@localhost:5433/school'
)
