![Gretil graph](graph/gretil-small.png)
# gretil-quotations
This repository contains the code and input data for the calculation of possible quotations and similar passages within the gretil corpus based on SIF-weighted averages of word vectors as described in [this paper](https://openreview.net/forum?id=SyK00v5xx). The Sandhi-seperated input data was created with [this code](https://github.com/OliverHellwig/sanskrit/tree/master/papers/2018emnlp).
The code of this repository is licensed under the GNU AGPLv3 license.

The etext data has been taken entirely from the [GRETIL](http://gretil.sub.uni-goettingen.de/) collection.



The HTML-tables produced by this code can be accessed [here](http://buddhist-db.de/sanskrit-html/0_index.html) ([download](https://zenodo.org/record/2532838#.XDLBMy4zZnI)).

A graphic visualization is available [here](http://buddhist-db.de/graph/).


The code is built on [fasttext](https://github.com/facebookresearch/fastText) and [nmslib](https://github.com/nmslib/nmslib). These are needed along with numpy and scipy in order to be able to execute the code.
The code for handling/storing the word vectors (fasttext.py) was taken from [this repository](https://github.com/Babylonpartners/fastText_multilingual).

To run the calculations, execute the file 'run.sh' in the code-dir. 

Completing the calculations takes about 8 hours on a multicore machine with sufficient memory (please adjust the scripts according to the hardware before running them).

Given the BOW-nature of averaged word vectors, the system can quite reliably detect passages where the word order was changed or different particles have been inserted between the words. It is not yet very good at detecting phrases where a larger part of the vocabulary was exchanged with synonyms. Stemming can certainly help with regard to this problem.



