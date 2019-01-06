# gretil-quotations
This repository contains the code and input data for the calculation of possible quotations and similar passages within the gretil corpus based on simple sum vectors. 

The data has been taken entirely from the [GRETIL](http://gretil.sub.uni-goettingen.de/) collection.

The code is built on [fasttext](http://gretil.sub.uni-goettingen.de/) and [nmslib](http://gretil.sub.uni-goettingen.de/).

To run the calculations, just execute the file 'run.sh' in the code-dir. It might work only on *nix-machines because it uses a few shell commands that might not be available on Windows. 

In order to run the calculations, a system with 220gb of memory and 80 logical cores was used, taking roughly three ours to complete for the entire collection.

In order to make it work on a system with different specifiations the scripts might need some adjustments. 

