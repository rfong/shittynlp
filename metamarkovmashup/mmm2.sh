#!/bin/bash
# Smush two files together then run mmm script on them

name1=`echo $1 | cut -f1 -d'.'`
name2=`echo $2 | cut -f1 -d'.'`

basename=$name1'+'$name2'.txt'

cat $1 >> $basename
cat $2 >> $basename

./mmm.sh $basename
