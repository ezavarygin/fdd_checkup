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
                if len(path_to_newf26) == 1:
                    error = 0
                elif len(path_to_newf26) == 0:
                    error = 1 # no f26 was found
                    data_list.append([float(path.split('/')[-1].split('_')[-1]),error, np.nan,np.nan,np.nan,np.nan])
                    continue
                else:
                    print " More than one f26 file was found in one folder:\n {}".format(path_to_newf26)
                    quit()
                # error = 0 => keep going
                with open(path_to_newf26[0],'r') as new_f26:
                    len_new_fort = len(new_f26.read().split('\n')) # number of lines in new f26
                if len_new_fort != len_fort:
                    error = 2 # new and original f26's have different number of lines
                    data_list.append([float(path.split('_')[-1]),error,np.nan,np.nan,np.nan,np.nan])

                else: # error = 0 still
                    results = self.fort_parse(path_to_newf26[0],ion1,ion2) # array with results
                    if results[1] == -3 or results[3] == -3:
                        error = 3 # '*******' uncertainty in f26
                        data_list.append([float(path.split('_')[-1]),error,np.nan,np.nan,np.nan,np.nan])
                    else:
                        data_list.append([float(path.split('_')[-1]),error,results[0],results[1],
                                          results[2],results[3]])
          
            data_list = np.array(data_list) # Convert to np.array for the following sorting
            data_list = data_list[np.argsort(data_list[:,0])] # Sort the array by fdd values (1st column)
            np.savetxt(result_file_name,data_list,delimiter='  ',fmt='%.10g') # save sorted results to file
        
        
    def fort_parse(self,path_to_f26,ion1,ion2):
        """
        Module is to parse f26 file and get H and D values with uncert.

        """
        with open(path_to_f26,'r') as new_f26:
            all_lines = new_f26.read().split('\n')
        if all_lines[-1] =='': # delete last empty line if present
            del all_lines[-1]
        all_ions = [line for line in all_lines if line.split()[0] != "%%" and line.split()[0] != "!"]
        total_H_line = all_ions[ion1-1].split() # Pick up ions specified in command line
        total_D_line = all_ions[ion2-1].split()
        Hcol = total_H_line[6] # 6 for ions with space in lable (H I)
        Dcol = total_D_line[6] # 5 for those without space (HI)
        if "*" in total_H_line[7]:
            Hcol_unc = -3 # will write error
        else:
            Hcol_unc = float(total_H_line[7]) # 7 for ions with space in lable (H I), 6 for those without space (HI)
        if "*" in total_D_line[7]:
            Dcol_unc = -3 # will write error
        else:
            Dcol_unc = float(total_D_line[7]) # 7 for ions with space in lable (D I), 6 for those without space (DI)
        if Hcol[-1] in ('x','%','X'): # change to whatever you like
            Hcol = float(Hcol[:-1])   # consider 2 last figures if you used 2 instead of 1
        else:
            Hcol = float(Hcol)
        if Dcol[-1] in ('x','%','X'):
            Dcol = float(Dcol[:-1])
        else:
            Dcol = float(Dcol)
        return [Hcol,Hcol_unc,Dcol,Dcol_unc]

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
