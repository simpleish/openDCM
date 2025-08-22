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


def start_postgres_container(db_name, username, password):
    postgres_container = PostgresContainer('postgres:15',
                                           port=5432,
                                           username=username,
                                           password=password,
                                           dbname=db_name)
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
                                        db_name,
                                        schema_name,
                                        db_host,
                                        db_port,
                                        username,
                                        password):
    endpoint = db_host
    driver = 'org.postgresql.Driver'
    classpath = 'external-jar/postgresql-42.6.0.jar'
    search_path = 'liquibase-postgres-db/changelog'
    
    with open('tests/liquibase.properties', 'w') as file:
        file.write('changeLogFile:' + change_log_file + '\n')
        file.write('liquibase.searchPath: ' +  search_path + '\n')
        file.write('url: jdbc:postgresql://' + endpoint + ':' + db_port + '/' + db_name + '?currentSchema=' + schema_name + '\n')
        file.write('username: ' + username + '\n')
        file.write('password: ' + password + '\n')
        file.write('driver: ' + driver + '\n')
        file.write('classpath: ' + classpath + '\n')
        file.write('liquibase.liquibaseSchemaName: ' + schema_name + '\n')
        file.close()


def initialize_database(db_name, username, password, db_host, db_port, schema_name):
    try:
        conn = psycopg2.connect(database=db_name,
                                user=username,
                                password=password,
                                host=db_host,
                                port=db_port,
                                options=f'-c search_path={schema_name}')
    
        # Create schema
        create_schema = 'CREATE SCHEMA IF NOT EXISTS ' \
            + schema_name + ' AUTHORIZATION ' \
            + schema_name + '_role;'
        # Create role
        create_role = 'CREATE ROLE ' + schema_name \
            + '_role WITH ADMIN ' + username + ';'
        
        cur = conn.cursor()

        log.info('Create role: ' + create_role)
        cur.execute(create_role)
        log.info('ROLE created successfully!')

        log.info('Create schema: ' + create_schema)
        cur.execute(create_schema)
        log.info('SCHEMA created successfully!')

        cur.close()

        conn.commit()
        conn.close()
        
    except Exception as e:
        log.info(f"An error of type {type(e)} occured while initializing the database: {e}")
        exit(e)        


def start_migration_testing():
    change_log_file_name = 'change_log_main.xml'
    db_name = 'initial'
    schema_name = 'base_schema'
    username = 'admin'
    password = 'secret'
    # db_host, db_port, db_url = '', '', ''

    # Step 1
    log.info(f'STEP 1: Spawning container...')
    try:
        db_host, db_port, db_url = start_postgres_container(dbname=db_name, 
                                                            user_name=username, 
                                                            pass_nm=password)
    except Exception as E:
        log.info(
            "Error during initialization of postgres container " + str(e))
    
    if db_host == '' or db_port == '':
        raise Exception ("Something went wrong during container creation!")
    
    # Step 2
    log.info(f"STEP 2: Starting test migration for schema {schema_name}")
    
    scripts_path = 'liquibase-postgres-migration/changelog/sql/'
    files = os.listdir(scripts_path)

    if files:
        try:
            log.info("TESTING migration...")

            # Create liquibase properties
            create_testing_liquibase_properties(change_log_file=change_log_file_name,
                                                database_name=db_name,
                                                schema_name=schema_name,
                                                host=db_host,
                                                port=db_port,
                                                username=username,
                                                password=password)
            
            initialize_database(db_name, username, password, 
                                db_host, db_port, schema_name)
            
            # Step 3 - run liquibase
            log.info('Running liquibase...')

            try:
                command = 'python3 tests/liquibase_testing.py'
                p = subprocess.call(command, shell=True)
                if p==0:
                    log.info('SUCCESS!')
                else:
                    raise Exception("ERROR. Liquibase execution ran into an unknown error.")
            except subprocess.CalledProcessError as e:
                exit(e)
        except Exception as e:
            log.info(f"An error of type {type(e)} occured while initializing the database: {e}")
            exit(e)

        log.info('FINISHED runnning liquibase!')


class TestMigration(TestCase):
    def test_migration_run(self):
        self.assertEqual(start_migration_testing(), None)


if __name__ == '__main__':
    unittest.main()