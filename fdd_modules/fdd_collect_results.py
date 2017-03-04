from glob import glob
import os
import numpy as np

class collect_results:
    """
    Module is to collect the results of VPFIT calculations and save them into 'fdd_results.dat' file.

    """
    def __init__(self,result_file_list,abs_path_list,fort_path,ion1,ion2):
        with open(fort_path,'r') as fort:
            len_fort = len(fort.read().split('\n')) # number of lines in original f26
        for result_file_name in result_file_list: # for each fd*_resuts.dat file (i.e. each parameter)
            abs_path_sublist = [abs_path for abs_path in abs_path_list if abs_path.split('/')[-2]==result_file_name.split('_')[0]] # sublist for each fdd parameter
            data_list = [] # Put all the results in the list to sort afterwards
            for path in abs_path_sublist:
                path_to_newf26 = glob(path + '/f26.?????') # look for f26 files
                # Series of checks for errors =====================================================
                if len(path_to_newf26) == 0:
                    error = 1 # no f26 was found
                    data_list.append([float(path.split('_')[-1]),error,np.nan,np.nan,np.nan,np.nan,np.nan])
                    continue
       	      	elif len(path_to_newf26) > 1:
		    print " More than one f26 file was found in one folder:\n {}".format(path_to_newf26)
                    quit()
                    # continue
                elif os.path.getsize(path + '/stderr.dat') != 0:
                    error = 2 # Error happened, check stderr.dat file
                    data_list.append([float(path.split('_')[-1]),error,np.nan,np.nan,np.nan,np.nan,np.nan])
                    continue
                elif os.path.getsize(path_to_newf26[0]) == 0:
                    error = 3 # zero size f26 file, check stdout.dat
                    data_list.append([float(path.split('_')[-1]),error,np.nan,np.nan,np.nan,np.nan,np.nan])
                    continue
                else:
                    pass # no errors so far => keep going
                with open(path_to_newf26[0],'r') as new_f26:
                    len_new_fort = len(new_f26.read().split('\n')) # number of lines in new f26
                if len_new_fort != len_fort:
                    error = 4 # new and original f26's have different number of lines
                    data_list.append([float(path.split('_')[-1]),error,np.nan,np.nan,np.nan,np.nan,np.nan])
                else:
                    results = self.fort_parse(path_to_newf26[0],ion1,ion2) # array with results
                    if results[1] == -5 or results[3] == -5:
                        error = 5 # '*******' uncertainty in f26
                        data_list.append([float(path.split('_')[-1]),error,np.nan,np.nan,np.nan,np.nan,np.nan])
                    else:
                        with open(path + '/stdout.dat','r') as iter_file:
			    n_iter = iter_file.read().count('iteration') # count occurrence of 'iteration' in vpfit output
                            n_iter = n_iter - 1 # remove zero iteration
                        if n_iter == 125:
                            error = -1 # indicate that we are not in the minimum yet, more iterations needed
                        else:
                            error = 0 # no errors
                        data_list.append([float(path.split('_')[-1]),error,n_iter,results[0],results[1],
                                          results[2],results[3]])
          
            data_list = np.array(data_list) # Convert to np.array for the following sorting
            data_list = data_list[np.argsort(data_list[:,0])] # Sort the array by fdd values (1st column)
            np.savetxt(result_file_name,data_list,delimiter='  ',fmt='%.10g') # save sorted results to file
        
        
    def fort_parse(self,path_to_f26,ion1,ion2):
        """
        Module is to parse f26 file and get ion1 and ion2 values with uncertainties.

        """
        with open(path_to_f26,'r') as new_f26:
            all_lines = new_f26.read().split('\n')
        if all_lines[-1] =='': # delete last empty line if present
            del all_lines[-1]
        all_ions = [line for line in all_lines if line.split()[0] != "%%" and line.split()[0] != "!"]
        total_ion1_line = all_ions[ion1-1].split() # Pick up ions specified in command line
        total_ion2_line = all_ions[ion2-1].split()
        ion1_col = total_ion1_line[6] # 6 for ions with space in lable (H I)
        ion2_col = total_ion2_line[6] # 5 for those without space (HI)
        if "*" in total_ion1_line[7]:
            ion1_col_unc = -5 # will write error
        else:
            ion1_col_unc = float(total_ion1_line[7]) # 7 for ions with space in lable (H I), 6 for those without space (HI)
        if "*" in total_ion2_line[7]:
            ion2_col_unc = -5 # will write error
        else:
            ion2_col_unc = float(total_ion2_line[7]) # 7 for ions with space in lable (D I), 6 for those without space (DI)
        if ion1_col[-1] in ('x','%','X'): # change to whatever you like
            ion1_col = float(ion1_col[:-1])   # consider 2 last figures if you used 2 instead of 1
        else:
            ion1_col = float(ion1_col)
        if ion2_col[-1] in ('x','%','X'):
            ion2_col = float(ion2_col[:-1])
        else:
            ion2_col = float(ion2_col)
        return [ion1_col,ion1_col_unc,ion2_col,ion2_col_unc]

def get_default_fdds(vp_setup_path):
    """
    The module is to get default fdd step sizes from vp_setup.dat.

    """
    with open(vp_setup_path,'r') as f:
        vp = f.read().split('\n')
    if vp[-1] == "":
        del(vp[-1])
    else: pass
    default_fdds = {}
    for line in vp:
        if line.split()[0] in ['fdbstep','fdzstep','fdclog','fd4vst']:
            default_fdds[line.split()[0]] = float(line.split()[1])
        else: pass
    return default_fdds
