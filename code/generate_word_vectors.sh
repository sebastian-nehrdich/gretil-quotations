#!/usr/bin/env bash
cd ../data/etexts-combined/
perl -pe "s/[^\t]+\t//g;" * >> ../all.txt
cd ..
fasttext skipgram -dim 150 -thread 40 -input all.txt -output skt_vectors;
rm all.txt

