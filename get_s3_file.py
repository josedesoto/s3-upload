#! /usr/bin/env python
"""Download logs or files from S3
 
Usage: python get_s3_file.py [options]
 
Options:
  -f ..., --log=...       Name of the log to download
  -D ..., --datelog=...   Date to thelog to donwload
  -l, --list              List all lthe content on the storage
  -h, --help              Show this help
  -s, size                Show total size of the bucket
  -d                      Show debugging information while parsing (disable)
 
Examples:
  python get_s3_file.py --list
  python get_s3_file.py -f example-of-name.log -D 2011-03-29
 
This script requires the boto module and dateutil for Python to be installed. For example: apt-get install python-boto python-dateutil
"""


import boto
from boto.s3.key import Key
import sys
from dateutil import parser
import getopt

_debug = 0

class LogError(Exception):   
        
    def __init__(self, message, value=None):
        self.message = message
        self.value=value


class MyStorage:



	BUCKET_NAME = 'bucket_name'
	AWS_ACCESS_KEY_ID=''
	AWS_SECRET_ACCESS_KEY=''	
	
	
	@staticmethod
	def __connect():
	    try:
		conn = boto.connect_s3(MyStorage.AWS_ACCESS_KEY_ID,MyStorage.AWS_SECRET_ACCESS_KEY)
		bucket = conn.get_bucket(MyStorage.BUCKET_NAME)
		
	    except:
		print LogError("ERROR, connecting to Amazon").message
		sys.exit(1)    
		
	    return bucket
	    
	@staticmethod
	def get_list():
	    list_files=MyStorage.__connect().list()
	    for i in list_files:
		print str(i.key)

	@staticmethod
	def get_size():
	    """Print the total size of the bucket"""
	    list_files=MyStorage.__connect().list()
	    size=0
	    for i in list_files:
		#size in bytes
		size=size+i.size
	
	    #SIZE IN GB
	    size = size / 1024 / 1024 / 1024
	    print "TOTAL SIZE: "+str(size)+"GB"
	
	
	@staticmethod
	def get_file(logname, datelog):

	    if logname=='':
		print 'ERROR parsing the log name. The script send exit status.'
		sys.exit(1)
		
	    if datelog=='':
		print 'ERROR parsing the date. The script send exit status.'
		sys.exit(1)
	    
	    try:
		day=parser.parse(datelog).strftime("%d")
		year=parser.parse(datelog).strftime("%Y")
		month=parser.parse(datelog).strftime("%m")
	    except:
		print 'ERROR parsing: '+datelog+' the date (date have to be in this format: 2011-03-29). The script send exit status.'
		sys.exit(2)	
	    
	    try:
		file_key=year+'/'+month+'/'+day+'/'+logname+'.'+datelog+'.bz2'  
		key=MyStorage.__connect().get_key(file_key)
		key.get_contents_to_filename(logname+'.'+datelog+'.bz2')
	    except:
		print LogError("ERROR, downloading the file").message
		sys.exit(2)
	    
	    print "The log have been donwload: "+logname+'.'+datelog+'.bz2'
	    

def usage():
    print __doc__    
    
def main(argv):
    datelog=''
    logname=''    
    
    try:
        opts, args = getopt.getopt(argv, "hlf:D:d:s", ["help", "list", "logname=", "datelog=","size"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):    
            usage()
            sys.exit()
	elif opt in ("-l", "--list"):
	    MyStorage.get_list()
	    sys.exit()
        elif opt == '-d':
            global _debug
            _debug = 1
        elif opt in ("-f", "--logname"):
            logname = arg
        elif opt in ("-D", "--datelog"):
            datelog= arg
	elif opt in ("-s", "--size"):
            MyStorage.get_size()
	    sys.exit()
    
    MyStorage.get_file(logname, datelog)
        


if __name__ == "__main__":
    main(sys.argv[1:])
