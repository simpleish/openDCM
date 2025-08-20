import argparse
import json
import logging
import subprocess
import sys
import os

from pyliquibase import Pyliquibase

# Create logging format
formatter = logging.Formatter("%(asctime)s %(levelname)s - %(message)s")
# Create print handler
handler_print = logging.StreamHandler(sys.stdout)
handler_print.setLevel(logging.INFO)
handler_print.setFormatter(formatter)
# Create logger
log = logging.getLogger("migration_run_log")
log.addHandler(handler_print)
log.setLevel(logging.INFO)


def create_liquibase_props(change_log_file, database_name, schema_name):
    log.info("CREATING liquibase.properties file for deployment")

    username = os.environ.get("DB_USER")
    password = os.environ.get("DB_PASS")
    endpoint = os.environ.get("DB_ENDPOINT")
    port = os.environ.get("DB_PORT")
    driver = 'org.postgresql.Driver'
    classpath = 'external-jar/postgresql-42.6.0.jar'
    search_path = 'changelog/'

    with open('liquibase.properties', 'w') as file:
        file.write('changeLogFile:' + change_log_file + '\n')
        file.write('url: jdbc:postgresql://' + endpoint + ':' + port + '/' + database_name + '?currentSchema=' + schema_name + '\n')
        file.write('username: ' + username + '\n')
        file.write('password: ' + password + '\n')
        file.write('driver: ' + driver + '\n')
        file.write('classpath: ' + classpath + '\n')
        file.write('liquibase.searchPath: ' +  search_path + '\n')
        file.write('liquibase.liquibaseSchemaName: ' + schema_name + '\n')

def run_migration():
    pass

if __name__ =='__main__':
    pass