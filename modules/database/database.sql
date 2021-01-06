create type request_type as enum ('pending', 'accepted', 'declined');

create table if not exists users
(
    id      serial primary key not null,
    uid     integer            not null,
    alias   varchar(255)       not null,
    name    varchar(255)       not null,
    surname varchar(255)       not null,
    request request_type       not null
);

create table if not exists queues
(
    id        serial primary key not null,
    title     varchar(255)       not null,
    curr_user integer default 0  not null
);

create table if not exists members
(
    user_id  integer references users (id) on delete cascade  not null,
    queue_id integer references queues (id) on delete cascade not null,
    skips    integer default 0                                not null
);

create table if not exists debts
(
    debtor_id   integer references users (id) on delete cascade not null,
    creditor_id integer references users (id) on delete cascade not null,
    value       integer                                         not null
);

alter table users
    owner to postgres;
alter table queues
    owner to postgres;
alter table members
    owner to postgres;
alter table debts
    owner to postgres;
