# usage: python3 change_date_time.py 0
import sys
import os

from helper_functions_YT.helper_functions_files_YT import add_path
from helper_functions_YT.helper_functions_files_YT import order_files

# ------ ------ commands ------ ------
# to check all time status of photos:
# exiftool -time:all -G1 /Users/ytian/Pictures/test/ 

# to run this script:
# python3 change_date_time.py 0
# 0 is dryrun. To execute, change 0 to 1

# don't forget to modify the actions according to your needs!

# ------ ------ configs ------ ------
inD="/Users/ytian/Pictures/test"
name_pattern="IMG"
f_names_ord=order_files(inD, name_pattern, 1, 0)
#f_names_ord=["2026_05_10_0889.MOV"]

change_time="+=1"
#0:0:1 0 or 00:00:01 00:00:00 if day, 1 if hour
time_zone=''
#time_zone='-timezone="+08:00"'
time_zone_city='-DaylightSavings="On"'
#time_zone_city='-TimeZoneCity="Hong Kong"'
## "-GPSTimeStamp-=1"

changes=change_time+'" '+time_zone+' '+time_zone_city

arg_exec=int(sys.argv[1])

def com_for_photos_videos(fN):
	fN_format=fN.split(".")[-1]
	coms=[]

	if fN_format.find("CR2")>=0 or fN_format.find("JPG")>=0:
		# if a video (MOV/MP4), this would only changes [QuickTime]     Create Date and Modify Date
		# for video, using this in thumbnail thing messes up the video
		com='exiftool -overwrite_original "-AllDates'+changes+' '+fN
		coms.append(com)

	if fN_format.find("MOV")>=0 or fN_format.find("MP4")>=0:
		# -AllDates changes:
		# [ExifIFD]       Date/Time Original
		# [Composite]     Create Date
		# [Composite]     Date/Time Original
		# [Composite]     Modify Date
		com='exiftool -overwrite_original -ThumbnailImage -b '+fN+' | exiftool "-AllDates'+changes
		com=com+" -wm w - | exiftool -overwrite_original -ThumbnailImage'<=-' "+fN
		coms.append(com)

		'''
		com="exiftool -overwrite_original -P "
		to_mod=[
		#'"-LocationDate-=00:00:01 0" ',
		# this messes up the next item "-Keys:LocationDate-=0:0:1 0"
		'"-QuickTime:CreateDate'+change_time+'" ',
		'"-QuickTime:ModifyDate'+change_time+'" ',
		'"-TrackCreateDate'+change_time+'" ',
		'"-TrackModifyDate'+change_time+'" ',
		'"-MediaCreateDate'+change_time+'" ',
		'"-MediaModifyDate'+change_time+'" ',
		]
		for one_mod in to_mod:
			com=com+one_mod
		com=com+fN
		coms.append(com)
		'''

	# [System]        File Modification Date/Time
	# [System]        File Access Date/Time
	com='exiftool -overwrite_original "-FileModifyDate<DateTimeOriginal" "-FileCreateDate<DateTimeOriginal" '+fN
	coms.append(com)
	com='exiftool -overwrite_original "-FileModifyDate+=6" '+fN 
	coms.append(com)
	#cannot on JPG, Warning: Shifting of MacOS FileCreateDate not yet supported #"-FileCreateDate-=1"
	return coms

for fN in f_names_ord:
	fN=add_path(inD, fN)
	coms=com_for_photos_videos(fN)
	for com in coms:
		print(com)
		if arg_exec: os.system(com)
	

