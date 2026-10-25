import os
import sys

from helper_functions_YT.helper_functions_files_YT import order_files
from helper_functions_YT.helper_functions_files_YT import find_hidden_files
from helper_functions_YT.helper_functions_files_YT import remove_files
from helper_functions_YT.helper_functions_files_YT import rename_list_of_files

# usage: 
# python3 rename_files.py remove_hidden 0
# python3 rename_files.py space 0
# python3 rename_files.py replace_name 0 IMGL IMG_



#inD=""
inD="/Users/ytian/Pictures/test"

name_pattern=""
#name_pattern="IMG_"
name_suffix=""
#name_suffix=".heic"

new_name_prefix=name_pattern+""
new_name_suffix=name_suffix

pn_new=1 #initial new page number

fNs_i=[]
fNs_f=[]

# functionalities: 
# "remove_hidden"
# "space"
# "replace_name"
arg_func=sys.argv[1]
arg_exec=int(sys.argv[2])

rename_opt="append"
#rename_opt="overwrite"

# obtain files in folder
# (despite not needed) order the order to rename
fNs_ord=order_files(inD, name_pattern, 1, 0)
print(len(fNs_ord),"files in total!")

print("checking for hidden files...")
fNs_hidden=find_hidden_files(fNs_ord)

# remove names from file list (prepare for further tasks)
for fN in fNs_hidden:
	fNs_ord.remove(fN)
print(len(fNs_ord),"visible files in total!")

#------ ------ remove hidden files ------ ------
# usage: 
# python3 rename_files.py remove_hidden 0
# used for removing hidden operational files
# e.g. generated due to different systems and external hard drives
if arg_func.find("remove_hidden")>=0: 
	remove_files(fNs_hidden, inD, arg_exec)


#------ ------ remove after space ------ ------
# usage:
# python3 rename_files.py space 0
# originally intended for removing " 2" after duplicate files
if arg_func.find("space")>=0:
	print("\n------ task: rename files - remove names after space ------")
	fs_to_rename=[]
	for fN in fNs_ord:
		if fN.find(" ")>0:
			fN_main=fN.split(".")[0]
			fN_format=fN.split(".")[-1]
			fN_main=fN.split(" ")[0]
			fN_idx=fNs_ord.index(fN)
			#print("file no.",fN_idx,"has a space in it!")
			fs_to_rename.append([fN_idx,fN_main+"."+fN_format])
	#print(fs_to_rename)

	for f_to_rename in fs_to_rename:
		fNs_i.append(fNs_ord[f_to_rename[0]])
		fNs_f.append(f_to_rename[1])


#------ ------ rename files - replace ------ ------
# usage: 
# python3 rename_files.py replace_name 0 IMGL IMG_
# used for replacing unideal prefix/suffix
if arg_func.find("replace_name")>=0:
	arg_pat_i=sys.argv[3]
	arg_pat_f=sys.argv[4]
	for fN in fNs_ord:
		if fN.find(arg_pat_i)>=0:
			fNs_i.append(fN)
			fNs_f.append(fN.replace(arg_pat_i, arg_pat_f))
	

#------ ------ rename files ------ ------
# calling the function to rename
if len(fNs_i)!=0: rename_list_of_files(fNs_i, fNs_f, inD, fNs_ord, rename_opt, arg_exec)

