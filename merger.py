#!/usr/bin/env python

#############################################################################
## Merges raw files to complete ones based on calendar or detector year
##############################################################################

import numpy as np
import healpy as hp
import argparse
import datetime as dt

from pathlib import Path

# Import default paths for output
import default_paths


# Extract map parameters other than date and detector configuration
def map_params(filename, ignore_last=False):

    map_info = Path(filename).stem          # filename ignoring path and ext
    params = map_info.split('_')
    params = params[1:]                     # ignore config (always first)
    if ignore_last:
        params = params[:-1]                # ignore date (always last)

    return '_'.join(params)



def merger(files, out, overwrite, nmaps=3):

    # Option for overwriting existing merged file
    out_path = Path(out)
    if out_path.is_file():
        if not overwrite:
            return
        out_path.unlink()

    print('Working on', out_path.stem)
    print(len(files), 'files found...')
    if len(files) == 0:
        return

    # Merge files
    for i, f in enumerate(files):
        print(f'Loading {Path(f).stem}'
        temp = hp.read_map(f, range(nmaps))
        if i == 0:
            combined_map = [np.zeros(temp[j].shape) for j in range(nmaps)]
        for k in range(nmaps):
            combined_map[k] += temp[k]

    # Write to file
    hp.write_map(out, combined_map)



if __name__ == "__main__":

    # Establish standard output paths
    default_paths.setup_output_dirs(verbose=False)

    p = argparse.ArgumentParser(
            description='Creates merged map files')
    p.add_argument('-c', '--configs', dest='configs', nargs='*',
            help='Specify which detector configuration (optional)')
    p.add_argument('--startDate', dest='startDate',
            default='05-13',
            help='Month and day at which to start the calendar year')
    p.add_argument('--detector', dest='detector',
            default='IC86', choices=['IC86','IT81'],
            help='Choose to merge in-ice (IC86) or IceTop (IT81) files')
    p.add_argument('--detectorYear', dest='detectorYear',
            default=False, action='store_true',
            help='Run using detector years instead of calendar years')
    p.add_argument('--prefix', dest='prefix',
            default=default_paths.maps_out,
            help='Map storage location')
    p.add_argument('--overwrite', dest='overwrite',
            default=False, action='store_true',
            help='Option to overwrite existing merged maps')
    args = p.parse_args()


    # Collect all daily map files
    map_path = Path(args.prefix)
    masterList = sorted(map_path.glob(f'*/{args.detector}*_????-??-??.fits'))

    # Default behavior: merge all detector configurations
    if args.configs == None:
        args.configs = sorted(set([f.stem.split('_')[0] for f in masterList]))

    for cfg in args.configs:

        fileList = []

        if args.detectorYear:
            fileList += [f for f in masterList if cfg in f]

        else:
            yyyy = int(cfg[-4:])
            s = f'{yyyy}-{args.startDate}'
            e = f'{yyyy+1}-{args.startDate}'
            start = dt.datetime.strptime(s, '%Y-%m-%d')
            end = dt.datetime.strptime(e, '%Y-%m-%d')
            delta = end - start
            runDates = [start+dt.timedelta(days=i) for i in range(delta.days)]
            for date in runDates:
                d = date.strftime('%Y-%m-%d')
                fileList += [f for f in masterList if d in f]

        fileList.sort()

        # Calculate comprehensive list of all unique parameters
        paramList = sorted(set([map_params(f, True) for f in fileList]))

        # Run merger on each set of parameters
        for params in paramList:
            files = [f for f in fileList if map_params(f, True)==params]
            out = f'{args.prefix}/merged/{cfg}_{params}.fits'
            if args.detectorYear:
                out = f'{args.prefix}/detector_merge/{cfg}_{params}.fits'
            merger(files, out, args.overwrite)


    # Always run project merger (merge all years or detector configs)
    files = sorted(Path(args.prefix).glob(f'merged/{detector}-*.fits'))
    paramList = sorted(set([map_params(f) for f in files]))
    for params in paramList:
        files = [f for f in files if map_params(f)==params]
        out = f'{args.prefix}/merged/{detector}_{params}.fits'
        merger(files, out, True)


