#!/usr/bin/env python

# This will install various components of the expression cloud system

import optparse, re, subprocess, sys

config = 'epi_config'

class ConfigReader(object):
	def __init__(self):
		self.services = {}
		self.commands = {}
		self.packages = {}
		self.repositories = {}

	def updateDictionary(self, key, value, dictionary):
			dictionary[key.group(0)] = value.group(0)

	def parseFile(self, config):
		try:
			configfile = open(config, 'r').readlines()
		except (RuntimeError, TypeError, NameError, IOError):
			print "No such file found"
			sys.exit()

		for line in configfile:
# Comments
			if re.search(r'(#)|(^ )', line):
				pass 
# Repositories
			elif re.search(r'REPO', line):
				self.updateDictionary(re.search(r'((?<=(REPO: ))\w+.*(?= ))', line), re.search(r'((?<=(REPO: \w+.*(?= ) )).*)', line), self.repositories)
# Services
			elif re.search(r'\w+(?=\:)', line) and re.search(r'(on|off)', line):
				self.updateDictionary(re.search(r'(.*\w+.*(?=\: ))', line), re.search(r'((?<=\: )\w+.*)', line), self.services)
# Commands
			elif re.search(r'\w+(?=\:)', line) and not re.search(r'(on|off|REPO)', line):
				self.updateDictionary(re.search(r'(.*\w+.*(?=\: ))', line), re.search(r'((?<=\: )\"\w+.*\")', line), self.commands)
# Packages			
			elif re.search(r'(?<=\;)\w+', line):
				self.updateDictionary(re.search(r'(?<=\;)\w+.*', line), re.search(r'(?<=\;)\w+.*', line), self.packages)

class PackageInstaller(ConfigReader):
	def __init__(self):
		super(PackageInstaller, self).__init__()
		pass

	def setupRepos(self):
		for item in self.repositories:
			commandline = 'rpm -Uvh %s' % self.repositories[item].strip("\"")
			subprocess.check_call(commandline, shell=True)

	def installPackages(self):
		commandline = 'yum install -y'
		for item in self.packages:
			commandline = commandline + " %s" % item
		subprocess.check_call(commandline, shell=True)

class ServiceManager(ConfigReader):
	def __init__(self):
		super(ServiceManager, self).__init__()
		pass

	def manageServices(self):
		commandline = 'chkconfig'
		for item in self.services:
			commandline = 'chkconfig %s %s' % (item, self.services[item])
			subprocess.check_call(commandline, shell=True)

class SetupPlatform(PackageInstaller, ServiceManager):
	def __init__(self, config):
		super(SetupPlatform, self).__init__()
		self.parseFile(config)


#if __name__ == '__main__':
#	parser = optparse.OptionParser()


SP = SetupPlatform(config)
SP.manageServices()
