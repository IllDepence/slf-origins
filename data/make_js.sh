#!/bin/bash

out_fn="../docs/js/data.js"

echo "data = [" > $out_fn
for fn in ./*.json; do
    cat "$fn" >> $out_fn
    echo "," >> $out_fn
done
echo "]" >> $out_fn
