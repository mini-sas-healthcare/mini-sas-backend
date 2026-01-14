# Mini-SAS Database Setup (PostgreSQL)

## Prerequisites
- PostgreSQL running locally
- Database created: `mini_sas`

## How to apply schema (run in order)

psql -U postgres -d mini_sas -f db/001_extensions.sql
psql -U postgres -d mini_sas -f db/002_users.sql
psql -U postgres -d mini_sas -f db/003_providers.sql
psql -U postgres -d mini_sas -f db/004_patients.sql
psql -U postgres -d mini_sas -f db/005_provider_schedule.sql
psql -U postgres -d mini_sas -f db/006_appointments.sql
psql -U postgres -d mini_sas -f db/007_cpt_codes.sql
psql -U postgres -d mini_sas -f db/008_payers.sql
