--liquibase formatted sql
--changeset user:simpleish

CREATE TABLE IF NOT EXISTS app.example (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);