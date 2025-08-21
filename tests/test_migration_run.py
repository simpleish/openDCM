""" This is not a unit-test for run_migration fn, but an application test for hte whole app """

import multiprocessing
import unittest
from unittest import TestCase

import asyncio
import logging
import subprocess
import sys
import os.path
import psycopg2
import sqlalchemy
from testcontainers.postgres import PostgresContainer

from tests.liquibase_testing import perform_liquibase_testing

# Create print handler
handler_print = logging.StreamHandler(sys.stdout)
# Set logging level for print handler
handler_print.setLevel(logging.INFO)
# Set formatting for print handler
formatter = logging.Formatter("%(asctime)s %(levelname)s - %(messages)s")
handler_print.setFormatter(formatter)
# Create logger
log = logging.getLogger("test_migration_run_log")
log.addHandler(handler_print)
log.setLevel(logging.INFO)


def start_postgres_container(datastore, user_name, pass_nm):
    postgres_container = PostgresContainer('postgres:15',
                                           port=5432,
                                           username=user_name,
                                           password=pass_nm,
                                           dbname=datastore)
    postgres_container.start()
    postgres_container.with_bind_ports(5432)
    db_url = postgres_container.get_connection_url()
    db_port = postgres_container.get_exposed_port(5432)
    db_host = postgres_container.get_container_host_ip()
    e = sqlalchemy.create_engine(postgres_container.get_connection_url())

    log.info("DB created for testing.")
    log.info("HOST: " + db_host)
    log.info("PORT: " + db_port)
    log.info("URL: " + db_url)

    return db_host, db_port, db_url

def create_testing_liquibase_properties(change_log_file,
                                        database_name,
                                        schema_name,
                                        host,
                                        port,
                                        username,
                                        password):
    endpoint = host
    driver = 'org.postgresql.Driver'
    classpath = 'external-jar/postgresql-42.6.0.jar'
    search_path = 'liquibase-postgres-db/changelog'
    
    with open('tests/liquibase.properties', 'w') as file:
        file.write('changeLogFile:' + change_log_file + '\n')
        file.write('liquibase.searchPath: ' +  search_path + '\n')
        file.write('url: jdbc:postgresql://' + endpoint + ':' + port + '/' + database_name + '?currentSchema=' + schema_name + '\n')
        file.write('username: ' + username + '\n')
        file.write('password: ' + password + '\n')
        file.write('driver: ' + driver + '\n')
        file.write('classpath: ' + classpath + '\n')
        file.write('liquibase.liquibaseSchemaName: ' + schema_name + '\n')
        file.close()
        

