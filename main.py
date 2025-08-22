
import argparse
from src.logger import log
from src.start_migration import run_migration

def argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument("--dbname", help="Database to which DCM is applied")
    parser.add_argument("--migration_schema", help="Schema to which liquibase DCM is to be applied")
    parser.add_argument("rollback_opt", help="yes/no on the rollback action")
    parser.add_argument("--tag", help="tag used for rollback and changeset")

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = argument_parser()

    log.info("STARTING liquibase migration...")
    run_migration(args=args)
    
    log.info('DONE!')