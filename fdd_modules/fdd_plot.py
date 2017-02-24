import matplotlib.pyplot as plt
from matplotlib import rc

#------------------------------------------------
# Customize layout
#------------------------------------------------
rc('lines',linewidth=1.0)
rc('font', family='Comic Sans MS')
rc('font', size=12)
rc('axes', labelsize=12)
rc('xtick', labelsize=10)
rc('ytick', labelsize=10)



def fdd_plot(result_file_list):
    """
    Module it to plot the results from fdd_results.dat file.

    """
    # Getting data from the file
    fdd_param_keys = [result_file.split('_')[0] for result_file in result_file_list]
    print "  Parameters to plot for:", fdd_param_keys
    plt.figure(figsize=(8.27,11.69))
    for j,result_file_name in enumerate(result_file_list):
        with open(result_file_name,'r') as res_file:
            res_data = res_file.read().split('\n')
        if res_data[-1] == "": # delete empty line if present
            del res_data[-1]
        else:
            pass
        fdd_list, H_list, Hunc_list, D_list, Dunc_list = [[] for i in range(5)]
        for line in res_data:
            line_split = line.split()
            if line_split[1] == '0':
                fdd_list.append(float(line_split[0].split('_')[-1])) # fdd_list
                H_list.append(float(line_split[2])) # H_list
                Hunc_list.append(float(line_split[3])) # Hunc_list
                D_list.append(float(line_split[4])) # D_list
                Dunc_list.append(float(line_split[5])) # Dunc_list
            elif line_split[1] == '1':
                print "  {} = {} <- excluded: error '1' (no f26 file was found, check 'stdout.dat' and 'stderr.dat')".format(fdd_param_keys[j], line_split[0])
            elif line_split[1] == '2':
                print "  {} = {} <- excluded: error '2' (new and original f26's have different number of lines, check 'stdout.dat')".format(fdd_param_keys[j], line_split[0])
            else:
                print "  Unknown error code was specified in {}".format(result_file_name)

        plt.subplot(len(fdd_param_keys),1,j+1)
        plt.plot(fdd_list,Dunc_list) # Plotting data
    plt.show()
    print "  Plot is done!"
