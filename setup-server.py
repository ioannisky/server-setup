#! /usr/bin/python

import argparse
import ConfigParser
from paramiko.client import SSHClient,MissingHostKeyPolicy
from paramiko.sftp_client import SFTPClient
import os
import os.path
import sys
import base64
import sys
import datetime


class MissingHostKeyPolicy2(MissingHostKeyPolicy):
	def missing_host_key(self,client, hostname, key):
		global server_public_keys		
		nkey=self.toHex(key)

		if( (nkey[0] in server_public_keys) and (server_public_keys[nkey[0]]==nkey[1])):
			return True
		else:
			raise Exception("Key {0!s} not in list {1!s}".format(nkey,server_public_keys))

		print client,hostname,
		return False

	def toHex(self,key):
		hk=key.get_fingerprint().encode("hex")
		fk=[hk[i:i+2] for i in range(0,len(hk),2)]
		fk=":".join(fk)
		t="Unknown"
		c=key.get_name()
		c=c.split("-")
		t=c[1].upper()

		return t,fk


def execCommand(client,command):
	stdin, stdout, stderr=client.exec_command(command)
	while True:
		line=stdout.readline()
		if(line==""):
			break
		print line.strip()

def writeLog(line):
	global log
	n=datetime.datetime.now().isoformat()
	log.write("[ {0} ] {1}\n".format(n,line))

if __name__=="__main__":
	#print sys.argv[0],__file__
	base_dir=os.path.dirname(sys.argv[0])
	log_dir=base_dir+"./logs/"

	now=datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

	logfile=log_dir+"log_"+now+".txt"

	log=open(logfile,"w")

	ap=argparse.ArgumentParser(description='The arguments')
	ap.add_argument("-c","--config")
	ap.add_argument("-s","--setup")
	args = ap.parse_args()
	
	config_file_path=args.config
	setup_type=args.setup
	cp=ConfigParser.ConfigParser()
	cp.read(config_file_path)
	
	host=cp.get(setup_type,"host")
	host=host.split(":")
	if(len(host)==2):
		port=int(host[1])
		host=host[0]
	else:
		host=host[0]
		port=22
	public_keys=cp.get(setup_type,"public-keys")
	client_certificate=cp.get(setup_type,"key")
	client_username=cp.get(setup_type,"username")
	run_file=cp.get(setup_type,"run-file")
	
	if(not os.path.exists(run_file)):
		print "File {0} does not exists".format(run_file)


	server_public_keys={}
	public_keys=public_keys.split(",")
	for pk in public_keys:
		pk=pk.strip().split("::")
		server_public_keys[pk[0]]=pk[1]

	


	client=SSHClient()
	client.set_missing_host_key_policy(policy=MissingHostKeyPolicy2())
	client.connect(host,username=client_username,port=port,key_filename=client_certificate)
	
	f=open(run_file,"r")
	while True:
		line=f.readline()
		if line=="":
			break
		line=line.strip()
		line=line.split(" ")
		if(line[0]=="RUN"):
			writeLog("=============================================")
			cs=client.get_transport().open_session()
			stdout=cs.makefile()
			stderr=cs.makefile_stderr()
			command=" ".join(line[1:])
			writeLog("Running Command "+command)
			cs.exec_command(command)
			out=stdout.read()
			err=stderr.read()
			rc=cs.recv_exit_status()
			writeLog("Exit code "+str(rc))
			writeLog("====== STDOUT =====\n"+out)
			writeLog("====== STDERR =====\n"+err)
			cs.close()
			writeLog("=============================================")
		elif(line[0]=="COPY"):
			writeLog("=============================================")
			sftp=client.open_sftp()
			source=line[1].strip()
			destination=line[2].strip()
			writeLog("COPY {0} to {1}".format(source,destination))
			sftp.put(source,destination)
			writeLog("=============================================")

