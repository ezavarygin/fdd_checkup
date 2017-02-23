from glob import glob
import os

class collect_results:
    """
    Module is to collect and plot the results of VPFIT calculations.

    """
    def __init__(self,abs_path_list,fort_path,ion1,ion2):
        with open(fort_path,'r') as fort:
            len_fort = len(fort.read().split('\n')) # number of lines in original f26
        with open('fdd_results.dat', 'w') as fdd_res_file: # open file to write results in
            for path in abs_path_list:
                print path
                path_to_newf26 = glob(path + '/f26.?????')
                if len(path_to_newf26) == 1:
                    error = 0
                elif len(path_to_newf26) == 0:
                    error = 1 # no f26 was found
                    fdd_res_file.write('{}  {:d}\n'.format(path.split('/')[-1],error))
                    continue
                else:
                    print " More than one f26 file was found in one folder:\n {}".format(path_to_newf26)
                    quit()
                # error = 0 => keep going
                with open(path_to_newf26[0],'r') as new_f26:
                    len_new_fort = len(new_f26.read().split('\n')) # number of lines in new f26
                if len_new_fort == len_fort: # error = 0 still
                    self.results = self.fort_parse(path_to_newf26[0],ion1,ion2) # array with results
                    print self.results
                else:
                    error = 2 # new and original f26's have different number of lines
                    fdd_res_file.write('{}  {:d}\n'.format(path.split('/')[-1],error))

                
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
        Hcol_unc = float(total_H_line[7]) # 7 for ions with space in lable (H I)
        Dcol_unc = float(total_D_line[7]) # 6 for those without space (HI)
        if Hcol[-1] in ('x','%','X'): # change to whatever you like
            Hcol = float(Hcol[:-1])   # consider 2 last figures if you used 2 instead of 1
        if Dcol[-1] in ('x','%','X'):
            Dcol = float(Dcol[:-1])
        return [Hcol,Hcol_unc,Dcol,Dcol_unc]


    def plot(self):
        print "Plot is done!"
