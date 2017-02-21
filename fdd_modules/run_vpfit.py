import os
import subprocess as sub

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
