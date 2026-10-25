import sys
import os

from helper_functions_YT.helper_functions_files_YT import *



# eliminate brother printer files that repeat themselves
#in the format of int(previous numbering) int

def brother_printer_find_duplicates(dir_path, fname_suffix=".jpeg", fname_base=""):
	# obtain files
	print("finding files in "+dir_path)
	files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f)) and fname_base in f]
	# sorts the files
	files.sort()
	
	f_to_remove=[]
	for fileN in files:
		fileN_l=fileN.split()
		fileN_l[-1]=fileN_l[-1].replace(fname_suffix,"")
		#print(fileN_l)

		if len(fileN_l)>1 and fileN_l[-1].isdigit() and fileN_l[-2].isdigit():
			#print(fileN_l[-1],fileN_l[-1].isdigit(),fileN_l[-2],fileN_l[-2].isdigit())
			f_to_remove.append(fileN)
	#print(f_to_remove)
	return f_to_remove


#currently startn not used
# for double-sided files, give 1 list of names, distinguish front and back, and determine new order
def fix_scan_order(dir_path, orderedNs, startn=1):
	n_files=len(orderedNs)
	n_front=int(n_files/2)
	# make sure always round up
	if n_front<n_files/2:
		n_front=n_front+1

	f_names_ft=orderedNs[0:n_front]
	f_names_bk=orderedNs[n_front:len(orderedNs)]
	print('the front pages ('+str(len(f_names_ft))+' pages):')
	print(f_names_ft,"\n")
	print('the back pages ('+str(len(f_names_bk))+' pages):')
	print(f_names_bk,"\n")
	f_names_bk.reverse()

	fNs_correct_ord=[]
	for i in range(len(f_names_ft)):
		fNs_correct_ord.append(f_names_ft[i])
		if i < len(f_names_bk):
			fNs_correct_ord.append(f_names_bk[i])
	print('correct order of double-sided scan files:')
	print(fNs_correct_ord,"\n")
	return fNs_correct_ord


def A3_order(dir_path, orderedNs, order_arg, startn=1):
	fNs_correct_ord=[]
	if len(order_arg)!=4:
		print("the argument that specifies A3 scan rearrangement order must be of four digits! aborting...")
		return fNs_correct_ord

	idx_1=(int(order_arg[0]))
	idx_2=(int(order_arg[1]))
	idx_3=(int(order_arg[2]))
	idx_4=(int(order_arg[3]))

	print(len(orderedNs),len(orderedNs)%4)
	for i in range(len(orderedNs)//4):
		fNs_correct_ord.append(orderedNs[i*4+idx_1-1])
		fNs_correct_ord.append(orderedNs[i*4+idx_2-1])
		fNs_correct_ord.append(orderedNs[i*4+idx_3-1])
		fNs_correct_ord.append(orderedNs[i*4+idx_4-1])
	print('correct order of A3 scan files:')
	print(fNs_correct_ord)

	return fNs_correct_ord
