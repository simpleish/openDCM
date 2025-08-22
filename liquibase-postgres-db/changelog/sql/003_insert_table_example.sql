--liquibase formatted sql
--changeset user:simpleish

INSERT INTO app.example (name) VALUES
  ('Alice'),
  ('Bob'),
  ('Charlie'),
  ('Diana'),
  ('Eve'),
  ('Frank'),
  ('Grace'),
  ('Heidi');