# README

## Description

The program is to determine optimal FDD's step sizes in [VPFIT](https://www.ast.cam.ac.uk/~rfc/vpfit.html) software.

## Installation
The software was written to work with `python 2.7`. 
To get started, include the path to the `fdd_checkup` executable file into your system PATH.
That is it, you can run it from any directory on your machine.

If you don't specify the path to your VPFIT exicutable, the program will look for it ('vpfit') in the folders specified in your `.profile`, `.bashrc`, etc. files.
Note, if you normally run VPFIT via alias, e.g if you have the following line:

`alias vpfit='/path/to/vpfit_executable'`

in your `.profile` file, this will raise an error.


**Python modules used:**

- subprocess
- numpy
- sys
- os
- glob
- time
- matplotlib

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
--cpu  - Number of vpfit instances to run at a time (default: '1').
--ions - Number of 2 ions to collect results for.
--plot - Create a plot with results (1st ion is H, 2nd ion is D in plots).
```

For each FDD parameter which you want to test your model for, `param_file` contains the following line:

```
parameter_name  start  end  number_of_steps
```

where `parameter_name` can be *fdbstep*, *fdzstep*, *fdclog* or *fd4vst*. `start` and `end` specify the range to go through for the corresponding FDD parameter. `number_of_steps` is a number of steps (equaly distributed in log10 space) to go through.


**Keep in mind:**

Take into account that VPFIT will be run from folders lying 2 directories down in the directory tree. You may need to correct the paths to your spectral ranges specified in the fort.26 file.

## What it does:

`fdd_checkup` consists of three main steps:

1. `fdd_checkup` creates a directory tree. For each FDD parameter specified in the `param_file` it creates a folder. The latter will contain as many folders as `number_of_steps` specified in you `param_file`. Each of these folder will contain a `vp_setup.dat` file with corresponding FDD parameters. Note, `fdd_checkup` tests one parameter at a time. Other FDD parameters are taken as those in your default `vp_setup.dat` file (specified with `--vp_setup` option).

2. `fdd_checkup` runs VPFIT from each of the folders, i.e. for each of the FDD parameter. It runs each VPFIT instance as a subprocess. At a time it runs as many VPFIT instances as was specified with `--cpu` option. Using a number larger than a number of cores your machine has will result in reducing efficiency. Once one of the instances finishes the calculation, a new one is run in place of it (untill no instances left to run).

3. `fdd_checkup` collects results of the calculations. It checks each of the folders for a f26 file and picks uncertainties and best-fit values of the parameter of interest for two ions specified with `--ions` option. The order of ions is the same as in fort.18 files. Being motivated by D/H measurements, the default parameter of interest was set to be column density (you can modify the code to whichever parameter you are interested in). The collected results are saved in text files (in a separate file for each FDD parameter).

**The structure of the output files:**

```
FDD_parameter_value  ERROR_key  Number_of_iterations  ion1_value  ion1_unc  ion2_value  ion2_unc
```

**ERROR keys:**

```
  0. no errors

  1. no f26 file was found

  2. error happened during VPFITing, check 'stderr.dat' file

  3. zero size f26 file, check 'stdout.dat' file

  4. new and original f26 files have different number of lines

  5. '*******'-like uncertainty for one (or both) of the ions was found in f26
```

There is also an optional (4th) step in `fdd_checkup` which will be useful to those doing a D/H analysis:

4. You can also plot the results using `--plot` option (do not use this option at first run of `fdd_checkup` but run it again with this option once you have got the results). Again, being motivated by D/H measurements, the labels on the axes were set to the case where the first and the second ions (specified with `--ions` option) are H I and D I respectively.
