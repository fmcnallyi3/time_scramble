#!/usr/bin/env python

##========================================================================##
## Creates a directory structure in your /data/user for output data       ##
##========================================================================##

from pathlib import Path


""" Paths to final data locations for input and internal project references """
def setup_default_paths():

    # Establish current directory and user
    current = Path(__file__).parent.resolve()
    user = Path.home().name

    # Default paths for analysis
    globalVals = globals().keys()
    global submitter, maps_out
    submitter = f'{current}/submitter'
    maps_out = f'/data/user/{user}/anisotropy/maps'

    # Print changes to global variables and establish paths if needed
    for key, key_path in globals().items():
        if key not in globalVals:
            print(f'Newly established path: {key} = {key_path}')
            Path(key_path).mkdir(parents=True, exist_ok=True)


