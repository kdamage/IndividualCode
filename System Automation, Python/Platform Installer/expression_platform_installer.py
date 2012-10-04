#!/usr/bin/env python
# Written by Kelcey Damage, 2012

# This will install various components of the expression cloud system

import optparse, re, subprocess, sys

baseconfig = 'epi_config'
extendedconfig = ''

class ConfigReader(object):
	def __init__(self):
		self.services = {}
		self.commands = {}
		self.packages = {}
		self.repositories = {}
		self.autoconfigservices = {}
		self.restricted = {}
		self.security = {}
		self.nagios = {}

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
# Autoconfig-Services
			elif re.search(r'AUTO_CONFIG', line):
				self.updateDictionary(re.search(r'(\w+.*(?=\:))', line), re.search(r'((?<= ).*\w+.*)', line), self.autoconfigservices)
# Commands
			elif re.search(r'(COMMAND)', line):
				self.updateDictionary(re.search(r'((?<=\: ).*\w+.*(?= \"))', line), re.search(r'((?<= )\"\w+.*\")', line), self.commands)
# Packages			
			elif re.search(r'(?<=\;)\w+', line):
				self.updateDictionary(re.search(r'(?<=\;)\w+.*', line), re.search(r'(?<=\;)\w+.*', line), self.packages)
# Restrictions
			elif re.search(r'(RESTRICT)', line):
				self.updateDictionary(re.search(r'(\w+.*(?=\:))', line), re.search(r'((?<= ).*\w+.*)', line), self.restricted)
# security
			elif re.search(r'(SECURITY)', line):
				self.updateDictionary(re.search(r'(\w+.*(?=\:))', line), re.search(r'((?<= ).*\w+.*)', line), self.security)
# Nagios
			elif re.search(r'(NAGIOS)', line):
				self.updateDictionary(re.search(r'(.*\w+.*(?=\:))', line), re.search(r'((?<=\: ).*\w+.*)', line), self.nagios)

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

	def configureMySQL(self):
		pass

class Security(ConfigReader):
	def __init__(self):
		super(Security, self).__init__()
		pass

	def restrictionHandling(self):
		pass

	def securityProfile(self):
		pass

	def configureNagios(self):
		pass

class AdvCommandExecution(ConfigReader):
	def __init__(self):
		super(AdvCommandExecution, self).__init__()
		pass

	def executeCommands(self):
		pass

class SetupPlatform(PackageInstaller, ServiceManager, AdvCommandExecution):
	def __init__(self, config):
		super(SetupPlatform, self).__init__()
		self.parseFile(config)
		print self.nagios

#if __name__ == '__main__':
#	parser = optparse.OptionParser()


SP = SetupPlatform(baseconfig)
#SP.manageServices()
