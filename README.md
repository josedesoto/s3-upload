# s3-upload

Script  to upload logs or any other files to Amazon Busket. It will upload 1 per day and remove the old logs based in the variable: MONTH_TO_KEEP. 

Option you can use in the script:
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
