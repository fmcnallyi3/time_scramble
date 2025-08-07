#!/usr/bin/env python

import shutil
import argparse
import sys, os
from glob import glob

# Import standard analysis paths from directories.py in parent directory
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import directories as ani

if __name__ == "__main__":

    ani.setup_input_dirs(verbose=False)
    ani.setup_output_dirs(verbose=False)

    p = argparse.ArgumentParser(
            description='Identify and copy missing maps')
    p.add_argument('-c', '--config', dest='config',
            nargs='+',
            help='Detector configuration (IC86-2011|IC86-2012|...)')
    p.add_argument('--copy', dest='copy',
            default=False, action='store_true',
            help='Copy missing files from local storage to project directory')
    args = p.parse_args()
            

    src_dir = ani.maps_out
    dst_dir = ani.cfg_maps

    for cfg in args.config:

        print(f'\nWorking on {cfg}...')

        # Collect all files
        src_files = sorted(glob(f'{src_dir}/{cfg}/*.fits'))
        dst_files = sorted(glob(f'{dst_dir}/{cfg}/*.fits'))

        # Omissions not needed for this analysis (energy binned anti|ext|solar)
        src_files = [f for f in src_files if ('GeV' not in f) or ('sid' in f)]
        dst_files = [f for f in dst_files if ('GeV' not in f) or ('sid' in f)]

        # Identify maps absent from either list
        src_set = set([os.path.basename(f) for f in src_files])
        dst_set = set([os.path.basename(f) for f in dst_files])
        missing_src = sorted(dst_set - src_set)
        missing_dst = sorted(src_set - dst_set)

        # Always alert if missing entries in local directory (unusual!)
        if missing_src != []:
            print('  Files missing in src directory:')
            for f in missing_src:
                print(f'    {f}')

        # Copy/print missing entries in project directory
        if missing_dst != []:
            if args.copy:
                print('  Copying the following files...')
                for f in missing_dst:
                    print(f'    {f}')
                    shutil.copy(f'{src_dir}/{cfg}/{f}', f'{dst_dir}/{cfg}/{f}')
            else:
                print('  Files missing in dst directory:')
                for f in missing_dst:
                    print(f'    {f}')

        if missing_src == [] and missing_dst == []:
            print('  All files match!')

    print()

