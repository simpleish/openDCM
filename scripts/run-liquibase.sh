#!/bin/bash

# Set environment variables for database connection
export DATABASE_URL="jdbc:postgresql://localhost:5432/your_database"
export DATABASE_USERNAME="your_username"
export DATABASE_PASSWORD="your_password"

# Run Liquibase update command
liquibase --changeLogFile=changelogs/db.changelog-master.xml update

# Optionally, you can add more commands for rollback or generating SQL scripts
# Example for rollback:
# liquibase --changeLogFile=changelogs/db.changelog-master.xml rollbackCount 1

# Example for generating SQL scripts:
# liquibase --changeLogFile=changelogs/db.changelog-master.xml updateSQL > update.sql