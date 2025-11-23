#!/bin/bash

out_fn="../docs/js/data.js"

echo "// Cited texts from literature sources in may be subject to license terms." > $out_fn
echo "// Please check the provided source URLs in case of re-use." >> $out_fn
echo "data = [" >> $out_fn
for fn in ./*.json; do
    cat "$fn" >> $out_fn
    echo "," >> $out_fn
done
echo "]" >> $out_fn
