CREATE SCHEMA feizi;

CREATE TABLE IF NOT EXISTS feizi.users
(
    id                  serial primary key,
    username            varchar not null,
    email               varchar,
    password            varchar
);

CREATE TABLE IF NOT EXISTS feizi.uploaded_images
(
    id                  serial primary key,
    user_id             int,
    filename            varchar not null,
    foreign key (user_id) references feizi.users(id)
);
