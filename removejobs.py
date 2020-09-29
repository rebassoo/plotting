import subprocess

for i in range(291985,292013):
    subprocess.call("condor_rm {0}".format(i),shell=True)
