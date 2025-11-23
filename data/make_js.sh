#!/bin/bash

out_fn="../docs/js/data.js"

echo "// Cited texts from literature sources in the JSON files may be subject to" > $out_fn
echo "// license terms. Please check the provided source URLs in case of re-use." > $out_fn
echo "data = [" > $out_fn
for fn in ./*.json; do
    cat "$fn" >> $out_fn
    echo "," >> $out_fn
done
echo "]" >> $out_fn
