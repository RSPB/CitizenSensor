# Citizen Sensor

We are using existing Convolutional Neural Networks to produce tags (so-called scene categories and scene attributes) for photographs. Each of these tags is provided a number: the higher the number, the higher likelyhood that the picture belongs to a certain class. Scene categories outcome is normalized (between 0 and 1), while scene attributes are not. In addition, we also provide output from penultimate layer of the neural network, which describes an image in terms of 4096 numbers that make a high-level characteristic of the image. The project consists of two main componenets: a web server and tools for batch processing.

## Web server

The web server serves a web site that allows user to submit an image and get in return set top-N scene categories and attribues associated with a picture. Live web site can be made available - do shout. 

## Batch processing

Command line tool to handle batch processing of images stored in a given location.

```
python batch_classifier.py -h
usage: Citizen Sensor [-h] -d DIRECTORY [-o OUTPUT] [-c CONFIG] [-x EXTRA]
                      [-k KEY] [-v VALUES [VALUES ...]] [-r ROTATE]
                      [--remove_completed] [--write_header]

Batch classifier

optional arguments:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        Path to the directory with images
  -o OUTPUT, --output OUTPUT
                        Output file name
  -c CONFIG, --config CONFIG
                        Path to the config file
  -x EXTRA, --extra EXTRA
                        Path to a supplementary data set, organised as CSV,
                        which contains key to join and values to be joined
  -k KEY, --key KEY     Index of column (counted from 0) in which the key is
                        present. The key should be unique and match exactly
                        file name in the dataset. Use in conjunction with
                        <extra> option
  -v VALUES [VALUES ...], --values VALUES [VALUES ...]
                        Indices of columns (starting from zero) to be joined.
                        Use in conjunction with <extra> option
  -r ROTATE, --rotate ROTATE
                        CSV rolling
  --remove_completed    Remove file after processing
  --write_header        Write header to the output files
```

## Requirements

The only module not available through pypi is Caffe - an open framework for deep learning. Instructions for installation are available [here](http://caffe.berkeleyvision.org/installation.html).
