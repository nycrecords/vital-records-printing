#!/usr/bin/env bash

# create tables
psql -d vital_records_printing -f birth/nyc_birth_index_create.sql
psql -d vital_records_printing -f birth/nyc_death_index_create.sql
psql -d vital_records_printing -f birth/nyc_marriages_index_create.sql

# insert rows
psql -d vital_records_printing -f birth/nyc_birth_index_add.sql
psql -d vital_records_printing -f birth/nyc_death_index_add.sql
psql -d vital_records_printing -f birth/nyc_marriages_index_add.sql
