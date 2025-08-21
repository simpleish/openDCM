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

def argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument("--dbname", help="Database to which DCM is applied")
    parser.add_argument("--migration_schema", help="Schema to which liquibase DCM is to be applied")
    parser.add_argument("rollback_opt", help="yes/no on the rollback action")
    parser.add_argument("--tag", help="tag used for rollback and changeset")

    args = parser.parse_args()
    return args

def create_liquibase_props(change_log_file, database_name, schema_name):
    log.info("CREATING liquibase.properties file for deployment")

    username = os.environ.get("DB_USER")
    password = os.environ.get("DB_PASS")
    endpoint = os.environ.get("DB_ENDPOINT")
    port = os.environ.get("DB_PORT")
    driver = 'org.postgresql.Driver'
    classpath = 'external-jar/postgresql-42.6.0.jar'
    search_path = 'liquibase-postgres-db/changelog'

    with open('liquibase.properties', 'w') as file:
        file.write('changeLogFile:' + change_log_file + '\n')
        file.write('liquibase.searchPath: ' +  search_path + '\n')
        file.write('url: jdbc:postgresql://' + endpoint + ':' + port + '/' + database_name + '?currentSchema=' + schema_name + '\n')
        file.write('username: ' + username + '\n')
        file.write('password: ' + password + '\n')
        file.write('driver: ' + driver + '\n')
        file.write('classpath: ' + classpath + '\n')
        file.write('liquibase.liquibaseSchemaName: ' + schema_name + '\n')
        file.close()

def run_migration():
    args = argument_parser()

    # Standard arguments 
    change_log_file_name = 'change_log_main.xml'
    db_name = args.dbname if hasattr(args, 'dbname') else 'initial'
    mig_schema = args.migration_schema if hasattr(args, 'migration_schema') else 'base_schema'
    rollback_opt = str(args.rollback_opt).lower() if hasattr(args, 'rollback_opt') else 'no'

    # Create liquibase properties
    log.info("CREATING liquibase.properties for database migration...")
    create_liquibase_props(change_log_file=change_log_file_name, 
                           database_name=db_name,
                           schema_name=mig_schema)
    
    log.info("EXECUTING update on database...")
    if rollback_opt == 'no':
        try:
            liquibase = Pyliquibase(defaultsFile="liquibase.properties",
                                    logLevel="INFO")
            # Liquibase execution
            liquibase.validate()
            liquibase.status()
            liquibase.updateSQL()
            liquibase.update()

            # Liquibase maintainance commands
            # <--- maintainanace commands will go here --->

        except Exception as e:
            raise Exception(
                "Database migration ran into an unknown error: " + str(e)) 
    elif rollback_opt == 'yes':
        try:
            liquibase = Pyliquibase(defaultsFile="liquibase.properties",
                                    logLevel="INFO")
            liquibase.rollback(args.tag)
        except Exception as e:
            raise Exception (
                "Database rollback failed: " + str(e))
    else:
        raise Exception("Database migration failed because 'rollback_opt'\
                        had incorrect values. Accepted values are yes/no.")


if __name__ =='__main__':
    run_migration()