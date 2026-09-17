#!/bin/bash

set -e
export PGPASSWORD=mysecretpassword

DB="piscineds"
USER="bcaumont"
FILE="../subject/item/item.csv"
TABLE="item"

psql -h localhost -U "$USER" -d "$DB" <<EOF
DROP TABLE IF EXISTS "$TABLE";

CREATE TABLE "$TABLE" (
    product_id BIGINT,
    category_id BIGINT,
    category_code TEXT,
    brand TEXT
);
EOF

psql -h localhost -U "$USER" -d "$DB" \
    -c "\copy \"$TABLE\" FROM '$FILE' CSV HEADER"

echo "Table $TABLE created and imported."
