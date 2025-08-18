--liquibase formatted sql
--changeset user:001-initial-schema

CREATE SCHEMA IF NOT EXISTS app;

CREATE TABLE IF NOT EXISTS app.example (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);