#!/bin/bash -l
#NOTE the -l flag!
# myFirstScript.sh used to showcase the basic slurm
# commands. Modify this to suit your needs.
# Name of the job -You'll probably want to customize this
#SBATCH -J crawl_data
# Use the resources available on this account
#SBATCH -A loop
#Standard out and Standard Error output files 
#SBATCH -o log/%J.o
#SBATCH -e log/%J.e
#To send mail for updates on the job
#SBATCH --mail-user=zxyvse@rit.edu
#SBATCH --mail-type=ALL
#Request 4 Days, 6 Hours, 5 Minutes, 3 Seconds run time MAX, 
# anything over will be KILLED
#SBATCH -t 4-06:05:03
# Put in debug partition for testing small jobs, like this one
# But because our requested time is over 1 day, it won't run, so
# use any tier you have available
#SBATCH -p tier3
# Request 4 cores for one task, note how you can put multiple commands
# on one line
#SBATCH -n 1 -c 1
#Job memory requirements in MB
#SBATCH --mem=16G
#Job script goes below this line
mkdir -p log
spack load py-urllib3
spack load py-pandas
python3 parse.py

