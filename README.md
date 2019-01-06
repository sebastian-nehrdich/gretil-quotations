![Gretil graph](doc/gretil-small.png)
# gretil-quotations
This repository contains the code and input data for the calculation of possible quotations and similar passages within the gretil corpus based on weighted averages of sum vectors as described in [this paper](https://openreview.net/forum?id=SyK00v5xx). The Sandhi-seperated input data was created with [this code](https://github.com/OliverHellwig/sanskrit/tree/master/papers/2018emnlp).
The code is licensed under the GNU AGPLv3 license.

The etext data has been taken entirely from the [GRETIL](http://gretil.sub.uni-goettingen.de/) collection.

The HTML-tables produced by this code can be downloaded [here](https://zenodo.org/record/2532723#.XDIToi4zZnI).


The code is built on [fasttext](https://github.com/facebookresearch/fastText) and [nmslib](https://github.com/nmslib/nmslib). You will need these along with numpy and scipy in order to be able to execute the code.

To run the calculations, execute the file 'run.sh' in the code-dir. 

Completing the calculations takes about 3 hours on a machine with 80 logical cores and 220gb of memory.



