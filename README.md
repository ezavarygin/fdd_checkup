# README

## Description

The program is to determine optimal FDD's step sizes in [VPFIT](https://www.ast.cam.ac.uk/~rfc/vpfit.html) software by Robert Carswell and John Webb.

## Installation
The software was written to work with `python 2.7`. 
To get started, include the path to the `fdd_checkup` executable file into your system PATH.
That is it, you can run it from any directory on your machine.

If you don't specify the path to your VPFIT exicutable, the program will look for it ('vpfit') in the folders specified in your .profile, .bashrc, etc files.
Note, if you normally run VPFIT via alias, e.g if you have the following line:

`alias vpfit='/path/to/vpfit_executable'`

in your .profile file, this will raise an error.


**Python modules used:**

- subprocess
- numpy
- sys
- os
- glob
- time
- matplotlib (will be in future)

## Usage

`fdd_checkup fort.26 --param param_file [--options]`

where:
```
fort.26 - VPFIT output file for your, sort of, best-fit model.

param_file - Path to the file with fdd parameters to go through.

```
Optional arguments:
```
--vp_setup - Path to your vp_setup.dat file (default: './vp_setup.dat')
--vpfit - Path to your vpfit exicutable (default: 'vpfit').
--cpu - Number of vpfit instances to run at a time (default: '1').
--plot - Create a plot with results (not working yet).
```
**Keep in mind:**

Take into account that VPFIT will be run from folders lying 2 directories down in the directory tree. You may need to correct the paths to your spectral ranges specified in the fort.26 file.

## What it does

TBA...