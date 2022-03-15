#!/bin/bash

gsed -e 's/"//g' $1 | sed -e 's/$/,/g' >& $2

cat $1 | grep "diff_order_ids" | awk -F= '{print $2 $3 $4}'  

cat $1 | grep "diff_order_ids" | awk -F= '{print $2}' | awk -F, '{print $1}'
