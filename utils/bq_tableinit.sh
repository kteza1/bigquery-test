#!/bin/bash

declare -a tables=("can")
DATA_SET="bq_testing"

echo "y" | bq rm -r $DATA_SET
bq -q mk $DATA_SET

echo $(dirname $BASH_SOURCE)
## now loop through the above array
for table in "${tables[@]}"
do
  bq -q mk --schema "utils/can_schema.json" -t $DATA_SET.${table}
done
