# usage:
# python3 use_brother_printer.py removal 0
# python3 use_brother_printer.py rename 0
# python3 use_brother_printer.py double_page 0
# python3 use_brother_printer.py A3 0 1432
# 0 means dryrun

from helper_functions_brother_printer import *
import sys


inD="/Users/ytian/Pictures/test"
# only consider file names that cointain <name_pattern>
# this can be used to filter target file series
#name_pattern=""
name_pattern=""

name_suffix=".jpeg"

new_name_prefix=name_pattern+"_p"
#new_name_prefix=name_pattern

new_name_suffix=name_suffix

#initial new page number
pn_new=2

arg_func=sys.argv[1]
arg_exec=int(sys.argv[2])
#argv 3 exists for A3 functionality

if arg_func=="removal":
	#------ ------ duplicate removal ------ ------

	f_to_rm=brother_printer_find_duplicates(inD, name_suffix, name_pattern)
	print("files to be removed:",f_to_rm)
	
	if arg_exec:
		# calling the function to remove
		remove_files(f_to_rm, inD, arg_exec)
	else:
		print("files NOT removed")

elif arg_func=="rename":
	#------ ------ rename files ------ ------

	# obtain the order to rename
	orderedN=order_files(inD, name_pattern, 1, 0)
	print(len(orderedN),"files in total!")

	# calling the function to rename
	print('------ ------ preparing to change names of files...')
	rename_files(orderedN, new_name_prefix+"{}"+new_name_suffix, inD, pn_new, arg_exec, "renumber")

elif arg_func=="double_page" or arg_func=="A3":
	#------ ------ fix double page scan order ------ ------

	# get initial order of all files in the specified directory
	orderedNs=order_files(inD, name_pattern, 1, 0)

	"""
	name_pattern1=name_pattern+"_front"
	name_pattern2=name_pattern+"_back"
	# get initial order of all files in the specified directory
	orderedNs1=order_files(inD, name_pattern1, 1)
	orderedNs2=order_files(inD, name_pattern2, 1)
	orderedNs=orderedNs1+orderedNs2
	"""

	correct_order=[]
	correct_order=fix_scan_order(inD, orderedNs, 1)	
	print('------ ------ preparing to change names of files...')
	correct_order=rename_files(correct_order, new_name_prefix+"{}"+new_name_suffix, inD, pn_new, arg_exec, "append")

	if arg_func=="A3":
		print("A3 function not available yet!")
		"""
		#------ ------ fix cut-up A3 scan order ------ ------
		print("preparing to correct for A3 files:\n")
		# fold A3 paper then cut and scan
		A3_order_arg=sys.argv[3]
		correct_order=A3_order(inD, correct_order, A3_order_arg, 1)
		
		rename_files(correct_order, new_name_prefix+"{}"+new_name_suffix, inD, pn_new, arg_exec)
		"""

else:
	print("no functionality selected, did nothing\nusage: python3 <code name> <0 or 1> <functionality>")
print("use_brother_printer.py executed\n\n")
