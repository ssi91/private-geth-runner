#!/bin/bash

DATA_PATH=(
  ~/geth_data/data1
  ~/geth_data/data2
  ~/geth_data/data3
  ~/geth_data/data4
)

for path in "${DATA_PATH[@]}"; do
  echo "Cleaning up $path"
  rm -r "$path"

  echo "Creating $path"
  mkdir "$path"
done
