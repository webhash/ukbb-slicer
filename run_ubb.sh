#!/bin/bash
#SBATCH --account=def-some-prof
#SBATCH -t 0-00:15 # (time)
#SBATCH --mem=2000 # (in MB)
#SBATCH -c 1 # number of cores requested
#SBATCH --output=ukb_slicer.out
#SBATCH --job-name=ukb_slicer
# we need not to use sbatch to use this utility, one can directly execute this bash file 
check_status(){

	s=$1
	v=$2
	if test $s -eq 0
	then
	        echo "Succesfully executed the $v"
	else
		echo "$v failed"
		echo 'Exiting ....'
		exit 1
	fi

}

echo 'if you are using slurm one can use module load to load the modules'
echo 'load required modules before attempting to run the script'
echo "---------------------"
echo 'load python'
module load python/3.7.4
check_status $? load-python-3-7-4

echo "---------------------"
echo 'load scipy-stack'
module load scipy-stack/2019a
check_status $? load-scipy-stack-2019a

echo "---------------------"
module list

echo "---------------------"
echo 'we will use the python version'
python --version
echo "---------------------"


# st will save the result as text file
# sc will save the result as csv file
# n is the number of rows, if you not sure of number of rows, pass a big number
# so all the rows are selected
# we have three level of verbose 0,1,2
python ukbiobank.py ~/ukbcsv/ukb40501.csv 31 -n 10000000  -st 1 -sc 1 -v 2

# we can pass multiple fields values as comma separated values
# we can also pass the list of eids to be extracted via ef
# but this approach is bit memory extensive so pass less number of coloums,
# if you are working on a low memory machine
#python ukbiobank.py ~/ukbcsv/ukb40500_cut_merged.csv "3,4,5,6,21,23" -ef ./eid_files/eids.txt  -st 1 -sc 1

#python ukbiobank.py ~/ukbcsv/ukb40500_cut_merged.csv 3 -n 10 -v 2 -sc 1

#python ukbiobank.py ~/ukbcsv/common/ukb40500_cut_merged.csv 3 -n 10

check_status $? python-utility

echo "---------------------"
