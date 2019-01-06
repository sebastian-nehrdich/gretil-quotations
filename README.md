# gretil-quotations
This repository contains the code and input data for the calculation of possible quotations and similar passages within the gretil corpus based on simple sum vectors. 

The data has been taken entirely from the [GRETIL](http://gretil.sub.uni-goettingen.de/) collection.

The code is built on [fasttext](https://github.com/facebookresearch/fastText) and [nmslib](https://github.com/nmslib/nmslib).

To run the calculations, execute the file 'run.sh' in the code-dir. 

Completing the calculations takes about 3 hours on a machine with 80 logical cores and 220gb of memory.

In order to make it work on a system with different specifiations the scripts might need some adjustments. 

