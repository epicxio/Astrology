#!/bin/bash

# Database credentials
DB_USER="root"
DB_PASS=""  # Remove the default password
DB_NAME="epic_x_horoscope"

# Function to check if a command succeeded
check_error() {
    if [ $? -ne 0 ]; then
        echo "Error: $1 failed"
        exit 1
    fi
}

# Create database and load schema
echo "Creating database and loading schema..."
mysql -u $DB_USER -e "DROP DATABASE IF EXISTS $DB_NAME;"
check_error "Dropping existing database"

mysql -u $DB_USER -e "CREATE DATABASE $DB_NAME;"
check_error "Creating database"

mysql -u $DB_USER $DB_NAME < schema.sql
check_error "Loading schema"

# Load seed data
echo "Loading places data..."
mysql -u $DB_USER $DB_NAME < seeds/places.sql
check_error "Loading places data"

echo "Loading translations data..."
mysql -u $DB_USER $DB_NAME < seeds/translations.sql
check_error "Loading translations data"

echo "Database initialization complete!" 