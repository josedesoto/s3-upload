"""
Created on May 10, 2012

Script  to upload logs or any other files to Amazon Busket. It will upload 1 per day and remove the old logs based in the variable: MONTH_TO_KEEP. 

- Option you can use in the script:
#1- python upload.py (will update the day before (yesterday). No overwrite file. Delete old files)
#2- python upload.py full_update (will update all the files. No overwrite file. Not delete old files)
#3- python upload.py full_update overwrite (will update all the files. Yes overwrite files. Not delete old files)
#4- python upload.py manual 2012-01-27 (will update the date file. No overwrite file. Not delete old files)
#5- python upload.py manual 2012-01-27 overwrite (will update the date file. Yes overwrite file. Not delete old files)
#6- python upload.py manual 2012-01 overwrite (will update all month. Yes overwrite file. Not delete old files)
#7- python upload.py manual 2012-01 (will update all month. No overwrite file. Not delete old files)

- Pid function
- Check MD5 when upload file
- Print the stdout to a log
- Delete the log from the date marked in MONTH_TO_KEEP
- Upload bar when the files are uploading manualy


"""

import boto
from boto.s3.key import Key
import sys, os
import commands, datetime
from datetime import date, timedelta
from time import strftime
from dateutil import parser
import fnmatch
import hashlib

#Configurations
MONTH_TO_KEEP=3.5
FULL_PATH_TO_LOGS='/var/logs/apache'
BUCKET_NAME = 'bucket_name'
AWS_ACCESS_KEY_ID=''
AWS_SECRET_ACCESS_KEY=''
LOG_SCRIPT='/var/log/s3_upload.log'
user_to_mail='example@example.com'
SENDMAIL = "/usr/sbin/sendmail"
pidfile = "/var/run/s3_upload.pid"

#Overwirte option: NO=0 and YES=1
OVERWRITE=0
#remove old logs option: NO=0 and YES=1. If we send any parameter to the script will be disable
REMOVE_OLD_LOGS=0
FULL_UPDATE=0
DEBUG=1
ARGV=""


#We open a file to write the log
sys.stdout = open(LOG_SCRIPT, 'a')

#We check the is running or not the script
pid = str(os.getpid())
if os.path.isfile(pidfile):
    print "ERROR, %s already exists, exiting." % pidfile
    sys.exit(1)
else:
    file(pidfile, 'w').write(pid)


print ('###############################START#########################################')
print ('***********************'+strftime("%Y-%m-%d-%H:%M:%S")+'**************************\n')

if (len(sys.argv) > 1):
    if( sys.argv[1] == 'full_update' ):
        #WRITE_LOG_SCRIPT.write('Full update have been choise. This will take long time... ')
	FULL_UPDATE=1
	REMOVE_OLD_LOGS=0
	if (len(sys.argv) == 3):
		if (sys.argv[2] == 'overwrite'):
			print 'You have choose overwrite all the files in Amazon. Becareful!!!'
			OVERWRITE=1
		else:
			print 'By default will not overwrite the files.'

    elif( sys.argv[1] == 'manual' ):
	
	try:
		if len(sys.argv[2].split('-')) == 3:
			today=parser.parse(sys.argv[2]).strftime("%Y-%m-%d")
		if len(sys.argv[2].split('-')) == 2:
			today=parser.parse(sys.argv[2]).strftime("%Y-%m")

		year=parser.parse(sys.argv[2]).strftime("%Y")
		month=parser.parse(sys.argv[2]).strftime("%m")
		ARGV='manual'
		REMOVE_OLD_LOGS=0

	except:
		print 'ERROR parsing: '+sys.argv[2]+' the date. The script send exit status.'
		sys.exit(1)

	if (len(sys.argv) == 4):
		if (sys.argv[3] == 'overwrite'):
			print 'You have choose overwrite the file in Amazon. Becareful!!!'
			OVERWRITE=1
		else:
			print 'By default will not overwrite the file.'

    else:
        print 'The parameter: '+sys.argv[1]+' is not correct... The script send exit status.'
	print 'Please try (full_update | full_update overwrite | manual date | or nothing)'
	sys.exit(1)

else:
	#We define the month and the year to create the key
	#We have change this part from the version 1.0. We have to take the day before. So today in on dey less
	today=(date.today() - timedelta(1)).strftime("%Y-%m-%d")
	year=today.split("-")[0]
	month=today.split("-")[1]
	day=today.split("-")[2]


global totalSize
global sizeWritten

sizeWritten=0
def timeleft(filesize):
    global sizeWritten
    sizeWritten += filesize
    percentComplete=(sizeWritten*100 / totalSize)
    sys.stdout.write ('\r[{0}] {1}%'.format('#'*(percentComplete/2), percentComplete))
    sys.stdout.flush()

#Email Function. Dont Touch!!! Any change can do that the funtion stop to work.
def mail(destinatario, asunto, cuerpo):
	#Envia un correo electonico si algo ha fallado
	mensaje = """To: %(destinatario)s
Subject: %(asunto)s

%(cuerpo)s
""" % vars()

	p = os.popen("%s -t" % SENDMAIL, "w") 	# Pipe a sendmail
	p.write(mensaje) 			# Send Mail to Pipe
	estado = p.close() 			# Close (pipe) connection 
	if estado: return estado



def getFolderSize(folder):
	total_size = 0
	for item in os.listdir(folder):
		itempath = os.path.join(folder, item)
		if os.path.isfile(itempath) and FULL_UPDATE==1:
			total_size += os.path.getsize(itempath)
		if os.path.isfile(itempath) and FULL_UPDATE==0 and pattern.replace('*','').replace('.bz2','')  in item:
			total_size += os.path.getsize(itempath)
			
	return total_size


def uploadFile(bucket,key,fn,filename):
	try:
		k=Key(bucket)
		k.key=key
		k.set_contents_from_filename(fn)
				
		filehash = hashlib.md5(open(fn,'rb').read())

		if '"'+filehash.hexdigest()+'"' == k.etag:
			filesUploaded.append(filename)
		else:
			filesErrorUploaded.append(filename)

	except:
		print "ERROR uploading the files... The process have been stoped"
		sys.exit(1)





# set boto lib debug to critical
#logging.getLogger('boto').setLevel(logging.CRITICAL)
# connect to the bucket
try:
	conn = boto.connect_s3(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY)
	bucket = conn.get_bucket(BUCKET_NAME)
except:
	print "ERROR when try to conenct to the bucket"
	sys.exit(1)

#Filter to upload today files
if FULL_UPDATE==0:
	pattern='*'+today+'*.bz2'
	print 'Files we have update in Amazon for: '+today
else:
	pattern='*.bz2'

totalSize=getFolderSize(FULL_PATH_TO_LOGS)-4096

print "\nTOTAL SIZE TO UPLOAD: "+str(round(totalSize/1024/1024.0))+" MB"

filesErrorUploaded=[]
filesUploaded=[]
#We search the logs for today and we upload all of them
for root, dirs, files in os.walk(FULL_PATH_TO_LOGS):
    for filename in fnmatch.filter(files, pattern):
	if FULL_UPDATE==1:
		date=filename.split('.')[3]
		year=parser.parse(date).strftime("%Y")
		month=parser.parse(date).strftime("%m")
		day=parser.parse(date).strftime("%d")
	elif ARGV=='manual':
		date=filename.split('.')[3]	
		day=parser.parse(date).strftime("%d")

	key = year+'/'+month+'/'+day+'/'+filename
	fn = os.path.join(root, filename)
	timeleft(os.path.getsize(os.path.join(root, filename)))

	if OVERWRITE==0:
		#We check if the Key already exist
		if not bucket.get_key(key):
			if DEBUG==1:
				print " Upload the file: "+filename+' ('+str(round(os.path.getsize(os.path.join(root, filename))/1024/1024.0))+'MB)'
			# create a key to keep track of our file in the storage
			uploadFile(bucket,key,fn,filename)

			
	if OVERWRITE==1:
		if DEBUG==1:
			print " Upload the file: "+filename+' ('+str(round(os.path.getsize(os.path.join(root, filename))/1024.0/1024.0))+'MB)'
		# create a key to keep track of our file in the storage
		uploadFile(bucket,key,fn,filename)
	

if filesErrorUploaded:
	mail_text="Error when upload files to Amazon. Please check the logs in /var/log/upload_bucket.log"
	mail_text+="\n\n"+str(filesErrorUploaded)

	if mail(user_to_mail, "ERROR TO UPLOAD AMAZON LOGS IN ED PROJECT", mail_text):
		print '\n\n ERROR Emailing!!!'	

	else:									
		print '\n\n OK Emailing!!!'

	print '\n\n Files ERROR when UPLOAD!!!'
	print '-------------------------------------------------'
	print filesErrorUploaded

if filesUploaded:
	print '\n\n Files have been upload!!!'
	print '-------------------------------------------------'
	print filesUploaded

else:
	print '\n\n No files have been upload!!!'
	print '-------------------------------------------------'
	

if REMOVE_OLD_LOGS==1:
	#After upload the files we searh the logs to remove: MONTH_TO_KEEP
	day_to_remove=date.today() - timedelta(MONTH_TO_KEEP * 31)
	day_to_remove=day_to_remove.strftime("%Y-%m-%d")
	pattern='*'+day_to_remove+'.bz2'

	print '-------------------------------------------------'
	print 'Ready to remove logs for '+day_to_remove
	for root, dirs, files in os.walk(FULL_PATH_TO_LOGS):
	    for filename in fnmatch.filter(files, pattern):
		print filename
		os.remove(os.path.join(root, filename))

print ('\n------------------------------------END----------------------------------------')
print ('***************************'+strftime("%Y-%m-%d-%H:%M:%S")+'********************************\n')
try:
	sys.stdout.close()
	
except:
	print "ERROR clossing the FILE LOG"
	sys.exit(1)

os.unlink(pidfile)

# we need to make it public so it can be accessed publicly
# using a URL like http://s3.amazonaws.com/bucket_name/key
#k.make_public()
# remove the file from the web server
#os.remove(fn)
