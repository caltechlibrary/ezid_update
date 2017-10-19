# ezid_update

Scripts to update ezid DOIs by following patterns

## Requirements

I ended up setting up a python2.7 environment in conda using:

conda create -n py27 python=2.7 anaconda
source activate py27

You need to install the EZID package from Mark Redar

[Download](https://bitbucket.org/mredar/ezid/downloads/) and install
by changing to the directory and typing `python setup.py install` 

The main version currently works with python 2.7.  Python 3.0 support coming
soon

You can set up a
python2.7 environment in conda using:

conda create -n py27 python=2.7 anaconda
source activate py27

You'll also need to install the datacite package by typing.

pip install datacite


## Usage

Set your EZID credentials by opening terminal and typing

`export EZID_USER=username`
`export EZID_PWD=password`

replacing username and password with your actual credentials.

## Testing

python update_from_cd.py 

## TCCON

python tccon.py #extracts info from the TCCON doi and updates doi links
