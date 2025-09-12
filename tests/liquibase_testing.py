from pyliquibase import Pyliquibase


def perform_liquibase_testing():
    try:
        liquibase = Pyliquibase(defaultsFile="tests/liquibase.properties",
                                jdbcDriversDir='external-jar')
        # Call execute with arguments
        liquibase.execute("status")
        # liquibase.execute("rollback", "MyTag")
        liquibase.validate()
        liquibase.status()
        liquibase.updateSQL()
        liquibase.update()
                
    except Exception as e:
        exit(e)

if __name__ == '__main__':
    perform_liquibase_testing()