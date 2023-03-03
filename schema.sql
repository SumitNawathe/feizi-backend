CREATE SCHEMA feizi;

CREATE TABLE IF NOT EXISTS feizi.campaigns
(
    id                 serial primary key,
    username           varchar not null,
    password           varchar not null
);
