# ezid_update

Scripts to update ezid DOIs by following patterns

## Requirements

I ended up setting up a python2.7 environment in conda using:

conda create -n py27 python=2.7 anaconda
source activate py27

You need to install the EZID package from Mark Redar

[Download](https://bitbucket.org/mredar/ezid/downloads/) and install
by changing to the directory and typing `python setup.py install` 

You'll also need to install the datacite package by typing.

pip install datacite

(I had to make a change to the package to get the schema to validate.  
Download the source and type python setup.py develop)

## Usage

Set your EZID credentials by opening terminal and typing

`export EZID_USER=username`
`export EZID_PWD=password`

replacing username and password with your actual credentials.

## TCCON

python2.6 tccon.py extracts info from the TCCON doi and updates doi links
