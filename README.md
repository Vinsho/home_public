sudo -iu postgres
CREATE DATABASE home;
CREATE USER <user> WITH ENCRYPTED PASSWORD 'yourpass';
GRANT ALL PRIVILEGES ON DATABASE home TO <user>;
GRANT postgres TO <user>;