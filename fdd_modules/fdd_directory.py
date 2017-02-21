import os

class fdd_folders_set_up:
    """
    The class is to create directories to test FDDs.

    A bunch of directories containing vp_setup.dat files, modified to cover
    the specified FDD ranges, is created.
    """
    def __init__(self,fdd_param,vp_setup_path):
        self.fdd_param = fdd_param
        fdd_list = fdd_param.keys()
        self.vp_setup_parse(vp_setup_path)
        self.fdd_directory(self.vp_without_fdd,self.vp_fdd,fdd_param)

        
    def vp_setup_parse(self, vp_setup_path):
        """
        The module is to parse the vp_setup.dat file.

        Output is 2-dimential table (str).
        """
        with open(vp_setup_path,'r') as f:
            vp = f.read().split('\n')
        if vp[-1] == "":
            del(vp[-1])
        else: pass
        self.vp_without_fdd = [line for line in vp if line.split()[0] not in ['fdbstep','fdzstep','fdclog','fd4vst']]
        self.vp_fdd = [line for line in vp if line.split()[0] in ['fdbstep','fdzstep','fdclog','fd4vst']]

    def fdd_directory(self,vp_without_fdd,vp_fdd,fdd_param):
        """
        The module creates folders and vp_setup files.

        Using a specified vp_setup as a template it creates a net of directories
        containing vp_setup.dat with different FDDs.
        """
        # First, create directories main directories for each of the parameters
        for key in fdd_param.keys():
            main_fdd_path = './' + key
            if not os.path.exists(main_fdd_path):
                os.makedirs(main_fdd_path)
            else:
                print '\n ', main_fdd_path, 'directory already exists!\n'
            # Then, create subdirectories for each FDD value and
            # create vp_setup.dat files
            for i in range(len(fdd_param[key])):
                subfolder_path = main_fdd_path+'/'+key+"_{:.1e}".format(fdd_param[key][i])
                os.makedirs(subfolder_path)
                with open(subfolder_path+'/vp_setup.dat','w') as f:
                    for line in vp_without_fdd:
                        f.write(line + '\n')
                    for line in vp_fdd:
                        if line.split()[0]!=key:
                            f.write(line + '\n')
                        else:
                            # Double formating is required in order to evoid scientific notation
                            f.write(key + ' {:.1E}\n'.format(fdd_param[key][i]))
