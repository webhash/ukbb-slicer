Intent of this tool is to slice the huge ukbb csv in a memory efficient way 
As ukbb has many instances for a particular field , this tool allows us to get all the
instances of a field passed to the tool

0. Though this tool is so efficient that one can run it on landing space of SLURM systems
1. its easiest to use the salloc command to first a job allocted for you and then running the command
2. many sample commands are provided in the run_ubb.sh script
3. below is the usage for the utility

usage: ukbiobank.py [-h] [-ef EIDSFILE | -n NUMROWS] [-v {0,1,2}] [-sc {0,1}]
                    [-st {0,1}]
                    csvfile fields

positional arguments:
  csvfile               pass the path to the csv file containing the data from
                        the ukbiobank
  fields                pass a comma separated values of all the fields you
                        want to extract the information about. please note
                        that you need not to pass the instances ids, just path
                        the root field ids

optional arguments:
  -h, --help            show this help message and exit
  -ef EIDSFILE, --eidsfile EIDSFILE
                        pass the path to the text file containing the list of
                        eids. file should have only one eid in one line
                        without any header. please note that this approach is
                        bit memory extensive as we first load the csv file
                        with all the rows, and selected columns, and then we
                        apply the filtering based on a list created from the
                        eid passed by the user. Please try to pass less number
                        of columns, so that the program could run even on low
                        memory system. on high memory system there would not
                        be any trouble
  -n NUMROWS, --numrows NUMROWS
                        pass the number of lines of data you want to see, in
                        default mode we shall print 1000 rows
  -v {0,1,2}, --verbosity {0,1,2}
                        increase output verbosity, by default we only print
                        the final dataframe as text, with input as 2 we will
                        also print the unique dict created, we will describe
                        the stats of the dataframe, etc...
  -sc {0,1}, --savecsv {0,1}
                        save the selected dataframe as a csv file
  -st {0,1}, --savetxt {0,1}
                        save the selected dataframe as a txt file
