import os
import time
import subprocess as sub

def start_calculation(vpfit_path,fort_path,abs_path_list,n_cpu):
    """
    The module is to run multiple vpfit's in background.

    """
    len_of_list = len(abs_path_list) # Number of VPFIT instances to be run
    if len_of_list <= n_cpu: # check if number of processes is less than number of CPUs specified
        n_cpu = len_of_list  # change n_cpu if needed

    vpfit_sub = {}
    for first_set_i in abs_path_list[:n_cpu]: # run as many vpfit instances as n_cpu
        fdd_key = '{}/{}/'.format(first_set_i.split('/')[-2],first_set_i.split('/')[-1])
        #    print fdd_key, '<-- started!'
        vpfit_sub[fdd_key] = run_vpfit(vpfit_path,first_set_i,fort_path)

    print "======================= Summary ========================"
    for sub_key in vpfit_sub.keys(): # list folders fo all the instances
        print " {} <-- VPFIT is being run for...".format(sub_key)
    print "........................................................"
    print " {} instances in the waiting list...".format(len_of_list-n_cpu)
    print "========================================================\n"

    n_i = n_cpu # n_i will go through the rest instances
    print_n = 60 # for every print_n of time.sleep()'s the list of instances is printed out
    check_n = 0
    while vpfit_sub:
        for sub_key in vpfit_sub.keys():
            if vpfit_sub[sub_key].poll() != None: # check if instance's vpfit ended
                print sub_key, '<-- finished!'
                del vpfit_sub[sub_key] # remove the finished instance
                try: # try to start new instance of VPFIT in place of finished one
                    rest_path_i = abs_path_list[n_i] # note, array starts from 0
                    fdd_key = '{}/{}/'.format(rest_path_i.split('/')[-2],rest_path_i.split('/')[-1])
                    print fdd_key, '<-- started in place of it!'
                    vpfit_sub[fdd_key] = run_vpfit(vpfit_path,rest_path_i,fort_path) # start new instance of VPFIT
                    n_i = n_i + 1
                except IndexError:
                    # print "There is no fdd setup left to run VPFIT for."
                    pass
            else:
                pass
        if check_n >= print_n:
            print "======================= Summary ========================"
            for sub_key in vpfit_sub.keys(): # list folders fo all the instances
                print " {} <-- VPFIT is being run for...".format(sub_key)
            print "........................................................"
            print " {} instances in the waiting list...".format(len_of_list-n_i)
            print "========================================================\n"
            check_n = 0
        #print 'wait 10 sec...'
        time.sleep(10.0)
        check_n = check_n + 1



def run_vpfit(vpfit_path,path2vpsetup,fort_path):
    """
    The module is to run vpfit with specific vp_setup.file

    """
    # Go to the directory to run VPFIT from
    if os.path.exists(path2vpsetup):
        os.chdir(path2vpsetup)
    else:
        print "\n There is no {} directory!\n".format(path2vpsetup)
        quit()
    stdin_vpfit = 'f\n?\n\n\n{}\nn\n\n'.format(fort_path)
    stdout_path = path2vpsetup + '/stdout.dat'
    stderr_path = path2vpsetup + '/stderr.dat'
    with open(stdout_path,'w') as out, open(stderr_path,'w') as err:
        process = sub.Popen([vpfit_path],stdin = sub.PIPE, stdout=out, stderr=err)
        process.stdin.write(stdin_vpfit)
#    os.chdir('../../')
    return process
