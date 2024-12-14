#!/bin/bash
PYTHON_VERSION=2.7

# FIXME put some of the below in a common routine
function checkout_version {
    local repo=$1
    local branch=${2:-python-2.4}
    echo Checking out $branch on $repo ...
    (cd ../$repo && git checkout $branch && pyenv local $PYTHON_VERSION) && \
	git pull
    return $?
}

export PATH=$HOME/.pyenv/bin/pyenv:$PATH
setup_trepan_owd=$(pwd)
bs=${BASH_SOURCE[0]}
mydir=$(dirname $bs)
cd $mydir/..
git checkout 2.0-for-Python-3.2 && pyenv local $PYTHON_VERSION && git pull
remake -c clean_pyc
cd $setup_trepan_owd
