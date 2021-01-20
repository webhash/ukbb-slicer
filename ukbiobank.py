'''
------------------------------
------------------------------

This program tries to print only the user specified columns and specified number of rows 
the goal is to free user from the complication of passing instances information as we 
automatically picks all the instances for the specified field.

This program can load data from large files even on a small memory system, even in computer canada landing space

------------------------------
------------------------------

todo: we can improve the performance further by changing the datatypes in pandas, like float64 to float32, handling mixed types

------------------------------
------------------------------

note 1 : user can add more steps in play_with_relevant_data function depending 
on their own requirement and usage

------------------------------
------------------------------

note 2 : we have use tabs for indentation, dont hate the tabs, and also please note that we have used python 3

------------------------------
------------------------------
sample usage :
------------------------------
------------------------------


we pass the filename of the program --- i.e. ukbiobank.py

followed by path to the csv file, a required field, user can pass partial path

followed by a string that contains comma separated field values, this is also a required field

we can either specify the number of rows to print by using optional parameter -n followed by number of lines, default value is 1000
or we can pass a text file containing the list of eids - one eid value in one line with flag -ef 
we cant' pass both of them together. if you don't specify anything than we would show default number of lines. 

we can change verbosity to 0, 1 or 2, with 0 we only print the text output of selected portion of dataframe 
with verbosity value of 1 we print some verbose information, and with verbosity 2 we also print the unique dict, we describe the dataframe, etc 

we can use -st flag to save the dataframe as a text file , this is an optional parameter and can take wither 0 or 1 as value 

we can use -sc flag to save the dataframe as a csv file, this is an optional parameter and can take wither 0 or 1 as value 

------------------------------
------------------------------
---1---

prints 100 lines, and also save the dataframe as csv and txt file. this will have some verbosity  

ukbiobank.py ./ukb40500_cut_merged.csv "34,3,4,5,6,104920,110005,110006,5990,20140,20192,24025" -v 1 -n 100 -sc 1 -st 1

------------------------------
------------------------------

---2---
here we will be less verbose and print only the rows with matching eid values provided via text file, 
verbosity is set to 0, we save the dataframe as text file 

ukbiobank.py ./ukb40500_cut_merged.csv "34,3,4,5,6,104920,110005,110006,5990,20140,20192,24025"  -ef eid.txt -v 0 -st 1 

------------------------------
------------------------------
	
---3---
we can pass only one field too, this one shall have verbosity set to 0 , no text file or csv file saved 

ukbiobank.py ./ukb40500_cut_merged.csv 34

------------------------------
------------------------------
'''
import pandas as pd
import re
import argparse
import sys
from os import path
import gc
import datetime


#########################
## user passed setting ##
#########################


# numbers of rows we want to print 
num_rows = None

#set verbose mode, default is zero 
verbose = int()

# this variable shall point to the path of the valid input csv file
csv_file = str()

# this variable points to the file that contains eid values
# each eid should be in newline  
eids_file = None 

# this list will contain all the eids provided by the user 
eids_list = list()

# this contains the list of all the relevant field ids as requested by user 
field_list = list()

# this flag is used to decide if we want to save the dataframe as csv file 
save_csv = bool()

# this flag is used to decide if we want to save the dataframe as txt file 
save_txt = bool()




##############################
## internal data structures ##
##############################


# create an empty dict which shall contain the field id 
# as key and all the different instances as keys
unique_col_dict = dict()

# points to the dataframe that contains the only the columns data 
df_col_csv = None

# points to the df that contains the relevant cols and specified no of rows 
df_data_csv = None


# although we have eid value as eid, lets put some other values too so that in future 
# we may run the tool on diff files with diff eid names
possible_eid_names = ['eid','e_id', 'id']

# we shall use below as the eid identifier in our dict
eid_identifier = 'eid'

csv_eid = str()

#########################
## internal functions  ##
#########################



# just a wrapper around print to print only when we have verbose set
# we use this in place of print when we want to print non-critical information
# so that user can decide if they want to print it or not 
def vprint(*args, **kwargs):
	if verbose:
		time = str(datetime.datetime.now().time()) + ' :: '
		print( time + " ".join(map(str,args)) , **kwargs)
	else:
		pass



def extract_unique_fields():
	global unique_col_dict
	global df_col_csv
	global eid_identifier
	# we onlt print when we have verbosity set to 2 
	def print_dict():
		if verbose>=2:
			# using the verbose flag this can be a long loop to iterate 
			# why waste time ?
			vprint("------------------------------------------------")
			vprint("unique field found")
			vprint("------------------------------------------------")
			vprint()
			for k in unique_col_dict:
				vprint("------------------------------------------------")
				vprint(k, end='  :  ')
				vprint(unique_col_dict[k])
				vprint("------------------------------------------------")
			vprint()

	# match numbers , as soon as we any other character the match shall stop 
	# as our instances have pattern of digits-0.x we shall get the digits 
	p = re.compile('^[0-9]+')
	try:
		for c in df_col_csv.columns:
			k= p.match(c)
			# if we found a match 
			if k:
				# get the match 
				key = k.group()
				# check if key already exists in dict 
				if key in unique_col_dict:
					# update the dict which should have previous values as list 
					unique_col_dict[key] = unique_col_dict[key] + [c]
				else:
					# else add the value to the dict as a list 
					unique_col_dict[key] = [c]
			else:
				# though we can hardcore this value 'eid' directly 
				# we are using possible eid names list so that we can support diff
				# eid names , which could be the scenario in future 
				if c.lower() in possible_eid_names:
					# we will have eid key as 'eid'
					# we assumke that we will have 
					# only one eid in the file, thus we dont make it a list 
					unique_col_dict[eid_identifier] = c
				else:
					vprint("------------------------------------------------")
					print("IMPORTANT :: we found a non number and non eid type column with the name ", c )
					vprint("we only deal with the column names that starts with numbers")
					vprint("------------------------------------------------")
					continue
		vprint("------------------------------------------------")
		vprint("total unique field ids ", len(unique_col_dict))
		vprint("------------------------------------------------")
		print_dict()
	except:
		print("Unexpected error:", sys.exc_info()[0])
		raise
	finally:
		# we are creating only one reference to this dataframe thus 
		# we shall hit the garbage collection immediately, ok hopefully we shall hit the GC 
		del df_col_csv
		# lets call gc.collect to make sure we do garbage collection 
		gc.collect()



def get_col_df_from_csv():
	global df_col_csv
	try:
		# we are only interested in the column info, and thus we are not loading any rows
		df_col_csv = pd.read_csv(csv_file , header=0 , nrows=0, low_memory=True)
	except MemoryError:
		print("Failed to load the csv file for the purpose of extracting column names")
		exit(-1)
	except:
		print("Unexpected error:", sys.exc_info()[0])
		print(sys.exc_info())
		exit(-1)



def load_relevant_field_data():
	global df_data_csv
	global num_rows
	global unique_col_dict
	global eids_list
	col_list = list()
	# as we also want to have the eid field in the out put we will  
	# add the eid col name to the list of the column name 
	# as the unique_col_dict[eid_identifier] is a string, we make it a list  
	# so that we can use the + operation to append the data 
	col_list = col_list + [unique_col_dict[eid_identifier]]
	for f in field_list:
		if f in unique_col_dict:
			col_list = col_list  + unique_col_dict[f]
		else:
				vprint("------------------------------------------------")
				vprint("Field value ( i.e column name)  : ", f, " not found in the unique col dict" )
				vprint("Please confirm that you have picked the correct value")
				vprint("remember you need not to pass the instance info like X-0.0, X-0.1, just pass X")
				vprint("------------------------------------------------")
				continue
	try:
		vprint("------------------------------------------------")
		vprint("we shall be reading from csv following columns")
		vprint()
		vprint(col_list)
		vprint()
		if num_rows:
			vprint("and we will try to extract : ", num_rows , " from the csv")
			vprint("if number of rows specified is greater than max row count then we shall return max row count items ")
			vprint("------------------------------------------------")
			df_data_csv = pd.read_csv(csv_file , usecols=col_list, nrows=num_rows, low_memory=True)
		else:
			vprint("------------------------------------------------")
			key = str(unique_col_dict[eid_identifier])
			vprint("we will use the list of eids provided to filter the dataframe")
			vprint("we have no other way than to load the entire frame with selected coloums")
			vprint("and then apply the filtering based on the list")
			vprint("this is memory extensive task and we should limit the no of columns")
			vprint("if we are using a very low memory machine")
			temp_data_csv = pd.read_csv(csv_file, usecols=col_list, low_memory=True)
			df_data_csv = temp_data_csv[temp_data_csv[key].isin(eids_list)]
			# delete the original data frame
			del temp_data_csv
	except MemoryError:
		print("Failed to load the csv file for the purpose of extracting column names")
		exit(-1)
	except:
		print("Unexpected error:", sys.exc_info()[0])
		print(sys.exc_info())
		exit(-1)
	finally:
		# not required but lets just do it !!!
		del col_list
		del unique_col_dict
		gc.collect()




###################################################
# this function plays with the selected dataframe #
###################################################
def play_with_relevant_data():
	global df_data_csv
	global save_txt
	global save_csv
	global num_rows
	# we only print this when verbosity is set to 2
	def print_df_information():
		if verbose>=2:
			vprint()
			vprint("------------------------------------------------")
			vprint("shape of dataframe")
			vprint(df_data_csv.shape)
			vprint("------------------------------------------------")
			vprint("statistic of the dataframe")
			vprint(df_data_csv.describe().to_string())
			vprint("------------------------------------------------")
			vprint()

	# we always print the output of dataframe as txt file 
	def print_df_as_string():
		vprint()
		vprint("------------------------------------------------")
		vprint("data from dataframe")
		# we always print the dataframe
		# we can also use the option_context but to_string() solves our purpose 
		#with pd.option_context('display.max_rows', None, 'display.max_columns', None):
		print(df_data_csv.to_string(index=False))
		vprint("------------------------------------------------")
		vprint()

	# we only print this when verbosity is set to 2
	def print_df_memory_usage():
		if verbose>=2:
			vprint()
			vprint("------------------------------------------------")
			df_data_csv.info(memory_usage='deep')
			vprint("------------------------------------------------")
			vprint()


	def save_df_to_txt():
		if save_txt:
			vprint("------------------------------------------------")
			vprint('saving dataframe to txt file')
			filename = '_'.join([str(f) for f in field_list])
			time = str(datetime.datetime.now().time()).replace('.','-').replace(':','-')
			filename = filename + '_' + time + '.txt'
			vprint('filename is : ', filename)
			# we dont want to have pandas index 
			data = df_data_csv.to_string(index=False)
			with open(filename, 'w') as f:
				f.write(data)
			vprint("------------------------------------------------")


	def save_df_to_csv():
		if save_csv:
			vprint("------------------------------------------------")
			vprint('saving dataframe to csv file')
			filename = '_'.join([str(f) for f in field_list])
			time = str(datetime.datetime.now().time()).replace('.','-').replace(':','-')
			filename = filename + '_' + time + '.csv'
			vprint('filename is : ', filename)
			df_data_csv.to_csv(filename, na_rep='NaN', index = False)
			vprint("------------------------------------------------")


	try:
		print_df_memory_usage()
		print_df_information()
		print_df_as_string()
		save_df_to_csv()
		save_df_to_txt()
		#########################################################
		####################USER  TODO ##########################
		
		'''
		user can do whatever pandas operation they want to do here
		on the df_data_csv
		!!! happy pandas !!!
		'''
		#################PLAY WITH THE DF_DATA_CSV###############
		#########################################################
	finally:
		del df_data_csv
		# lets call gc.collect to make sure we do garbage collection 
		gc.collect()




def run_parser():
	# internal function to validate file path and file type
	def check_file_path_type(filepath, type):
		if path.exists(filepath):
		# check if path points to a file 
			if path.isfile(filepath):
				# confirm the extension of the file
				extns = filepath.split(".")[-1]
				if extns.lower() == type.lower():
					# great its a valid file return true 
					return True
				else:
					# not a csv type file
					print("we expect a ", type, " as input, please pass path to a valid file")
					print("the current file is not of type ", type)
					return False
			else:
				# not a file
				print("we expect a file as input, please pass path to a file")
				print("the current path doesn't point to a file")
				return False
		else:
			# not a valid path
			print(filepath, " file doesnt point to a valid path")
			print("please pass a valid path to the ", type, " file")
			return False

	parser = argparse.ArgumentParser()
	
	parser.add_argument("csvfile", type=str,
	help = "pass the path to the csv file containing the data from the ukbiobank")
	
	
	parser.add_argument("fields", type=str,
	help = "pass a comma separated values of all the fields you want to extract the information about. \
	please note that you need not to pass the instances ids, just path the root field ids")

	group = parser.add_mutually_exclusive_group(required=False)
	
	# user can pass either the number of lines or the list of eids 
	
	group.add_argument("-ef", "--eidsfile", type=str,
	help="pass the path to the text file containing the list of eids. file should have only one eid in one line without any header.\
	please note that this approach is bit memory extensive as we first load the csv file with all the rows, and selected columns,\
	and then we apply the filtering based on a list created from the eid passed by the user. Please try to pass less number of columns,\
	so that the program could run even on low memory system. on high memory system there would not be any trouble")
	
	group.add_argument("-n", "--numrows", type=int, default=1000,
	help="pass the number of lines of data you want to see, in default mode we shall print 1000 rows")
	
	parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2], default=0, 
	help="increase output verbosity, by default we only print the final dataframe as text, \
	with input as 2 we will also print the unique dict created, we will describe the stats of the dataframe, etc...")
	
	parser.add_argument("-sc", "--savecsv", type=int, choices=[0, 1], default=0, 
	help="save the selected dataframe as a csv file ")
	
	parser.add_argument("-st", "--savetxt", type=int, choices=[0, 1], default=0, 
	help="save the selected dataframe as a txt file ")
	
	args = parser.parse_args()
	
	global verbose
	if args.verbosity:
		verbose = args.verbosity
	else:
		verbose = 0
		
	global csv_file
	if args.csvfile:
		# we shall use the absolute path so that we remain independent 
		# of the platform on which we execute this python code
		if(check_file_path_type(args.csvfile, 'csv')):
			# first check if path is valid
			csv_file = path.abspath(args.csvfile)
			vprint("------------------------------------------------")
			# set the global path to the file name passed by the user
			vprint("we will use the csv file : " , csv_file)
			vprint("------------------------------------------------")
		else:
			print("Exiting ....")
			exit(-1)
	
	
	global field_list
	field_list = [f.strip() for f in args.fields.split(",")]
	
	vprint("------------------------------------------------")
	vprint("user requested information about the following fields: ")
	vprint(field_list)
	vprint("------------------------------------------------")

	# user shall either provide the num of rows or the eid values through a text file 
	global eids_file
	global num_rows
	global eids_list
	if args.eidsfile:
		# we shall use the absolute path so that we remain independent 
		# of the platform on which we execute this python code
		if(check_file_path_type(args.eidsfile, 'txt')):
			# first check if path is valid
			eids_file = path.abspath(args.eidsfile)
			vprint("------------------------------------------------")
			# set the global path to the file name passed by the user
			vprint("we will use the eids file to get list of eids to be selected from dataframe : " , eids_file)
			with open(eids_file, 'r') as f:
				 eids_list  = f.read().splitlines() 
			# we set the num_rows to zero so that we know that user has 
			# requested for selection based on eids 
			num_rows = 0
			vprint("------------------------------------------------")
		else:
			print("Exiting ....")
			exit(-1)
	elif args.numrows:
		num_rows = int(args.numrows)
		vprint("------------------------------------------------")
		# inform user about the number of row we shall print
		vprint("we will print total number of rows : ", num_rows)
		vprint("------------------------------------------------")

	
	global save_csv
	if args.savecsv:
		vprint("------------------------------------------------")
		# inform user about the number of row we shall print
		vprint("we will save the dataframe as csv file")
		save_csv = True
		vprint("------------------------------------------------")
	else:
		vprint("------------------------------------------------")
		# inform user about the number of row we shall print
		vprint("we will NOT save the dataframe as csv file")
		save_csv = False
		vprint("------------------------------------------------")

	global save_txt
	if args.savetxt:
		vprint("------------------------------------------------")
		# inform user about the number of row we shall print
		vprint("we will save the dataframe as txt file")
		save_txt = True
		vprint("------------------------------------------------")
	else:
		vprint("------------------------------------------------")
		# inform user about the number of row we shall print
		vprint("we will NOT save the dataframe as txt file")
		save_txt = False
		vprint("------------------------------------------------")

##########
## main ##
##########

def main():
	# call the parser and update all the global variables 
	run_parser()
	# load the csv and create the dataframe 
	# we dont load any row data here, just the header, with low_memory as True 
	get_col_df_from_csv()
	# now we shall use the dataframe that contains only the header and get the unique fields
	# after extraction we will delete the reference to the dataframe and call gc collection 
	extract_unique_fields()
	# now call the  load_relevant_field_data that should only load cols user specified 
	load_relevant_field_data()
	# finally lets see the loaded dataframe , we delete the dataframe reference inside this function 
	play_with_relevant_data()
	
	return 0



if __name__== "__main__":
	main()