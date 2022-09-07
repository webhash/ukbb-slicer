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


# get the kinship and ancestry information 
#python ukbiobank.py /home/vaibhash/projects/rrg-danilobz/common/access_40k_UKB_holmes/csv/ukb40507.csv  "21017" -n 100000000  -sc 1  -v 1

# get genetic sex and PCs
#python ukbiobank.py /home/vaibhash/projects/def-danilobz/common/access_40k_UKB_holmes/ukb40504.csv  "22001,22009" -n 100000000  -st 1 -sc 1  -v 1

# get all accelerometer average data 
#python ukbiobank.py /home/vaibhash/projects/def-danilobz/common/access_40k_UKB_holmes/ukb40504.csv  "90004,90012,90013,90019,90020,90021,90022,90023,90024,90025,90027,90028,90029,90030,90031,90032,90033,90034,90035,90036,90037,90038,90039,90040,90041,90042,90043,90044,90045,90046,90047,90048,90049,90050" -n 100000000  -st 1 -sc 1  -v 1

#python ukbiobank.py ~/projects/def-danilobz/common/ukb40500_cut_merged.csv "3,4,5,6,21,23" -ef ./eids.txt  -st 1 -v 0

#python ukbiobank.py ~/projects/def-danilobz/common/ukb40500_cut_merged.csv "3,4,5,6,21,23" -ef ./all_eids.txt  -st 1 -sc 1

#python ukbiobank.py ~/projects/def-danilobz/common/ukb40500_cut_merged.csv "3,4,5,6,21,23,47,48,49" -n 100000 -sc 1

#python ukbiobank.py ~/projects/def-danilobz/common/ukb40500_cut_merged.csv "3,4,5,6,21,23" -n 10000 -v 1 -st 1

# disable low_memory mode 
#python ukbiobank.py ~/projects/def-danilobz/common/ukb40500_cut_merged.csv "3,4,5,6,21,23" -n 10000 -v 1 -st 1 -l 0

#python ukbiobank.py ~/projects/def-danilobz/common/ukb40500_cut_merged.csv 3 -n 10 -v 2 -sc 1

#python ukbiobank.py ~/projects/def-danilobz/common/ukb40500_cut_merged.csv 3 -n 10 

check_status $? python-utility

echo "---------------------"
