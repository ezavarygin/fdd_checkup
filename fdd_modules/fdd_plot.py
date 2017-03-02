import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np

#------------------------------------------------
# Customize layout
#------------------------------------------------
rc('lines',linewidth=1.0)
rc('font', family='Comic Sans MS')
rc('font', size=12)
rc('axes', labelsize=12)
rc('xtick', labelsize=10)
rc('ytick', labelsize=10)



def fdd_plot(result_file_list,default_fdds):
    """
    Module it to plot the results from fdd_results.dat file.

    """
    # Getting data from the file
    fdd_param_keys = [result_file.split('_')[0] for result_file in result_file_list]
    print "  Parameters to plot for:", fdd_param_keys
    fig = plt.figure(figsize=(8.27,11.69))
    axs = [None]*(len(result_file_list)*4+1) # List of axes: 2 ions x (1 uncert + 1 value)
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
            elif line_split[1] == '3':
                print "  {} = {} <- excluded: error '3' ('****' uncertainty was found for one of specified ion! Check f26 file)".format(fdd_param_keys[j], line_split[0])
            else:
                print "  Unknown error code was specified in {}".format(result_file_name)

        # Data are ready to plot
        # First column of subplots (uncertainties)
        axs[4*j+1] = plt.subplot(len(fdd_param_keys),2,2*j+1)
        axs[4*j+1].plot(fdd_list,Dunc_list,color='b') # Plotting data
        axs[4*j+1].set_ylabel(r'$\Delta$N(D I)',color='b')
        axs[4*j+1].tick_params('y',colors='b')
        axs[4*j+1].ticklabel_format(useOffset=False)
        axs[4*j+1].set_xscale('log')
        if fdd_param_keys[j] == 'fdbstep':
            axs[4*j+1].set_xlabel('{} [{:g}], km/s'.format(fdd_param_keys[j],default_fdds[fdd_param_keys[j]]))
        else:
            axs[4*j+1].set_xlabel('{} [{:g}]'.format(fdd_param_keys[j],default_fdds[fdd_param_keys[j]]))
        axs[4*j+1].axvline(default_fdds[fdd_param_keys[j]],linewidth=1.2,color='g') # indicate fdd from vp_setup.dat
#        axs[4*j+1].margins(y=np.ptp(Dunc_list)/2.0) # Include marging above and below the data to show default fdds
        axs[4*j+2] = axs[4*j+1].twinx() # second plot on the same axis
        axs[4*j+2].plot(fdd_list,Hunc_list,color='r')
        axs[4*j+2].set_ylabel(r'$\Delta$N(H I)',color='r')
        axs[4*j+2].tick_params('y',colors='r')
        axs[4*j+2].ticklabel_format(useOffset=False,axis='y')
        # Second column of subplots (middle values)
        axs[4*j+3] = plt.subplot(len(fdd_param_keys),2,2*j+2)
        plot_interal = False # Add 1-sigma interval
        if plot_interal == True:
            median  = np.median(D_list)
            med_unc = np.median(Dunc_list)
            print "median = {} +/- {} for {}".format(median,med_unc,fdd_param_keys[j])
            axs[4*j+3].fill_between(fdd_list, median-med_unc, median+med_unc,facecolor='green', alpha=0.4)
        axs[4*j+3].plot(fdd_list,D_list) # Plotting data
        axs[4*j+3].set_ylabel(r'N(D I)',color='b')
        axs[4*j+3].ticklabel_format(useOffset=False)
        axs[4*j+3].tick_params('y',colors='b')
        axs[4*j+3].set_xscale('log')
        if fdd_param_keys[j] == 'fdbstep':
            axs[4*j+3].set_xlabel('{} [{:g}], km/s'.format(fdd_param_keys[j],default_fdds[fdd_param_keys[j]]))
        else:
            axs[4*j+3].set_xlabel('{} [{:g}]'.format(fdd_param_keys[j],default_fdds[fdd_param_keys[j]]))
        axs[4*j+3].axvline(default_fdds[fdd_param_keys[j]],linewidth=1.2,color='g') # indicate fdd from vp_setup.dat
#        axs[4*j+3].margins(y=np.ptp(D_list),tight=False) # Include marging above and below the data to show default fdds
        axs[4*j+4] = axs[4*j+3].twinx()
        axs[4*j+4].plot(fdd_list,H_list,color='r')
        axs[4*j+4].set_ylabel(r'N(H I)',color='r')
        axs[4*j+4].tick_params('y',colors='r')
        axs[4*j+4].ticklabel_format(useOffset=False,axis='y')
#    plt.tight_layout()
    fig.subplots_adjust(hspace=0.3,wspace=0.9) # Set up spaces between subplots
    plt.savefig("fdd_plot.pdf",bbox_inches='tight', pad_inches=0)
    plt.show()
    print "  Plot is done!"
