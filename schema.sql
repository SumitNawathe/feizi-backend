CREATE SCHEMA feizi;

CREATE TABLE IF NOT EXISTS feizi.users
(
    id                 serial primary key,
    username           varchar not null,
    email              varchar,
    password           varchar
);
