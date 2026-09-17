#!/bin/bash

set -e
export PGPASSWORD=mysecretpassword

DB="piscineds"
USER="bcaumont"
FOLDER="../subject/customer"

for file in $FOLDER/*.csv
do
    table=$(basename "$file" .csv)
    echo "Processing $table..."
    psql -h localhost -U $USER -d $DB <<EOF
DROP TABLE IF EXISTS $table;

CREATE TABLE $table (
    event_time TIMESTAMP,
    event_type TEXT,
    product_id BIGINT,
    price NUMERIC,
    user_id BIGINT,
    user_session UUID
);

EOF

    psql -h localhost -U $USER -d $DB -c "\copy $table FROM '$file' CSV HEADER"

    echo "$table imported successfully."

done
