from sqlalchemy import create_engine


test_engine = create_engine(
    'postgresql+psycopg2://tester:tester@localhost:5433/test_school'
)
