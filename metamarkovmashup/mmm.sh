#!/bin/bash

basename=`echo $1 | cut -f1 -d'.'`

python preprocess.py $1
python train.py $basename.sentences
python generate.py $basename.chain

echo "to generate more: python generate.py $basename.chain"
