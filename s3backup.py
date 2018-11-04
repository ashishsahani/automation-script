#!/usr/bin/python3
                                                                            
# PROGRAMMER: Ashish Sahani                                             
# DATE CREATED: 04/11/2018                                
# REVISED DATE:             <=(Date Revised - if any)                         
# PURPOSE: To take a backup of mysql database backup in ec2 instance and upload it to s3 bucket 


import datetime
import boto3
import os
import smtplib

'''
Function to upload a zip file to s3 bucket
@Input : zipfilename, bucket_name
'''
def upload(zipfilename,bucket_name):
	try:
		print('uploading.....')
		s3 = boto3.client('s3','us-east-1')
		s3.upload_file(zipfilename, bucket_name, zipfilename)
	except Exception as e:
		print('uploading failed.....',e)
		failedmail()

'''
Function to archive a file
@Input : zipfilename, originalname
'''
def archiveFile(zipfilename,originalname):
	zip_shell_command = 'zip {} {}'.format(zipfilename,originalname)
	try:
		print('archving.....')
		os.system(zip_shell_command)
	except Exception as e:
		print('archving failed.....',e)
		failedmail()

'''
Function to take a mysql dump
@Input : username, password, databasename, sqlFilename
'''
def mysqldump(username,password,databasename,sqlFilename):
	try:
		print('taking dump.......')
		shell_command = 'mysqldump -u {} --password={} {} > {}'.format(username,password,databasename,sqlFilename)
		os.system(shell_command)
	except Exception as e:
		print('taking dump failed.......',e)
		failedmail()

'''
Function send a mail
'''
def failedmail():

	sender = 'senderemail'
	receivers = ['receiverpassword']
	message = 'Textinbulk backup failed!'
	try:
		smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
		smtpObj.starttls()
		smtpObj.login('youremail', 'emailpassword')
		smtpObj.sendmail(sender, receivers, message)
		print('Successfully sent email')
	except Exception as e:
		print('Error: unable to send email', e)
	
'''
Main Function to be executed when this file runs
'''
def main():
	print('backup starts ......')
	databasename = 'yourdatabasename'
	username = 'yourdatabaseuser'
	password = 'yourdatabasepassword'
	zipfilename = databasename + datetime.date.today().strftime('%m-%d-%y') + ".zip"
	bucket_name = 's3-bucket-name'
	sqlFilename = databasename + datetime.date.today().strftime('%m-%d-%y') + ".sql"
	mysqldump(username,password,databasename,sqlFilename)
	archiveFile(zipfilename,sqlFilename)
	os.remove(sqlFilename)
	upload(zipfilename,bucket_name)
	os.remove(zipfilename)

if __name__ == '__main__':
	main()
