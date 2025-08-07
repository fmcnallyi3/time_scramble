This is the analysis directory for the IC86.2011-IC86.2021 11-year cosmic ray
anisotropy analysis for planned publication in Astrophysical Journal.

The analysis is currently set up to be run in two parts. Scripts in the icesim,
timeScramble, and powerspec directories are meant to write to a directory in
/data/user to avoid accidentally overwriting final, processed data for the
analysis. Scripts that create final plots 

It includes:

- README.md : This file
- data : Summarized dipole phase and amplitude data from other experiments
- directories.py : Establishes input and output paths used in the analysis
- etc : Location for bonus tests
- icesim : Establishes histograms and splines for energy binning and estimation
- mapFunctions : Scripts relating to map manipulation and plotting
- plotMaker.py : Wrapper script for the creation of all plots for the paper
- powerspec : For the creation of angular power spectra
- stability : Tests of detector stablilty, livetime, missing files, time gaps, etc.
- submitter : Functions for submission to npx4
- timeScramble : For the creation and merging of map files

If running a new analysis, the following projects should be executed in order:

- directories.py
  - Make sure to edit this file to write to your desired output directories
- icesim
- timeScramble
- powerspec
- plotMaker.py


If re-making the plots for the analysis, run

./directories.py --user $(whoami)
./plotMaker.py --all

