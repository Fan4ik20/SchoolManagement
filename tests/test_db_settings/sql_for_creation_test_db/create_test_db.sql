CREATE DATABASE test_school;

CREATE USER tester WITH PASSWORD 'tester';
GRANT ALL PRIVILEGES ON DATABASE "test_school" to tester;