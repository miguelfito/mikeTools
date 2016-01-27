#!/usr/bin/python
# coding=utf-8

import os
import sys, getopt
from pwd import getpwuid

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
	
def find_owner(filename):
	# Para un determinado path, vamos a analizar todos los elementos que contiene
    return getpwuid(os.stat(filename).st_uid).pw_name
	
def list_dir(path, user, ident):
	# Para un determinado path, vamos a analizar todos los elementos que contiene
	for member in os.listdir(path):
		owner = find_owner(path + '/' + member)
		# Si es un directorio, tendremos que operar recursivamente con él... 
		if os.path.isdir(path + '/' + member): 
			print (' ' * ident) + '{:<49} {:>40}'.format((bcolors.OKBLUE + member + bcolors.ENDC), owner)
			list_dir(path + '/' + member, user, ident+2)
			
		# Si no es un directorio, es un fichero y lo recopilaremos
		else:
			print (' ' * ident) + '{:<40} {:>40}'.format(member, owner)
			
			''' 
				Hay dos opciones para volcarlo al fichero: 
					1- Que no venga parámetro user (no queremos los ficheros de un usuario en concreto, queremos los de todos)
						
						ó
						
					2- Que venga un user dado. En este caso, comprobaremos que el owner del fichero que estamos analizando coincide
					con el usuario que queremos.
					
				Evidentemente, si estamos buscando los de un usuario en concreto y no es el owner del fichero que analizamos, no lo volcamos.
			'''
			if user == '' or (user != '' and owner == user):
				fo = open('files_' + owner + '.log', "a")
				fo.write(path + '/' + member + '\n')
				fo.close()

def main(argv):
	
	path = '.'
	user = ''
	
	try:
		opts, args = getopt.getopt(argv,"hp:u:",["path=","user="])
	except getopt.GetoptError:
		print 'list_files.py -p <path> -u <user>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'list_files.py -p <path> -u <user>'
			sys.exit()
		elif opt in ("-p", "--path"):
			path = arg
		elif opt in ("-u", "--user"):
			user = arg
	
	list_dir(path,user, 0);

if __name__=='__main__':
	os.system("clear");
	os.system("rm files_*.log");
	main(sys.argv[1:])
	print '\n' * 5;
