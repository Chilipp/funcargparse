#!/bin/bash
# script to automatically generate the sphinx_nbexamples api documentation using
# sphinx-apidoc and sed
sphinx-apidoc -f -M -e  -T -o api ../funcargparse/
# replace chapter title in funcargparse.rst
sed -i '' -e 1,1s/.*/'API Reference'/ api/funcargparse.rst
sed -i '' -e 2,2s/.*/'============='/ api/funcargparse.rst
