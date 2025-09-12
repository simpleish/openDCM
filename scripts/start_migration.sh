#!/bin/bash

chmod 777 main.py

set e; python3 ./main.py \
--dbname $1 \
--migration_schema $2 \
--rollback_opt $3 \
--tag $4

rm liquibase.properties