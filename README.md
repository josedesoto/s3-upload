# s3-upload

Script  to upload logs or any other files to Amazon Busket. It will upload 1 per day and remove the old logs based in the variable: MONTH_TO_KEEP. 

Options you can use in the script:

0. python upload.py (will update the day before (yesterday). No overwrite file. Delete old files)
0. python upload.py full_update (will update all the files. No overwrite file. Not delete old files)
0. python upload.py full_update overwrite (will update all the files. Yes overwrite files. Not delete old files)
0. python upload.py manual 2012-01-27 (will update the date file. No overwrite file. Not delete old files)
0. python upload.py manual 2012-01-27 overwrite (will update the date file. Yes overwrite file. Not delete old files)
0. python upload.py manual 2012-01 overwrite (will update all month. Yes overwrite file. Not delete old files)
0. python upload.py manual 2012-01 (will update all month. No overwrite file. Not delete old files)

* Pid function
* Check MD5 when upload file
* Print the stdout to a log
* Delete the log from the date marked in MONTH_TO_KEEP
* Upload bar when the files are uploading manualy


# get-s3-file

Download logs or files from S3
 
Usage: python get_s3_file.py [options]
 
Options:
  -f ..., --log=...       Name of the log to download

  -D ..., --datelog=...   Date to thelog to donwload

  -l, --list              List all lthe content on the storage

  -h, --help              Show this help

  -s, size                Show total size of the bucket
  
  -d                      Show debugging information while parsing (disable)
 
Examples:
  ```
  python get_s3_file.py --list
  python get_s3_file.py -f example-of-name.log -D 2011-03-29
 ```
 
This script requires the boto module and dateutil for Python to be installed. For example: apt-get install python-boto python-dateutil