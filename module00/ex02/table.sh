#!/bin/bash

set -e
export PGPASSWORD=mysecretpassword

DB="piscineds"
USER="bcaumont"
FILE="../subject/customer/data_2022_oct.csv"
TABLE="data_2022_oct"

psql -h localhost -U "$USER" -d "$DB" <<EOF
DROP TABLE IF EXISTS "$TABLE";

CREATE TABLE "$TABLE" (
    event_time TIMESTAMP,
    event_type TEXT,
    product_id BIGINT,
    price NUMERIC,
    user_id BIGINT,
    user_session UUID
);
EOF

psql -h localhost -U "$USER" -d "$DB" \
    -c "\copy \"$TABLE\" FROM '$FILE' CSV HEADER"

echo "Table $TABLE created and imported."
