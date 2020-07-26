import sys
import json
import os.path

# Store() class is just a wrapper for the singleton __Singleton_Store() class.
class Store():
	class __Singleton_Store():
		def __init__(self, path:str = "vars.json"):
			# Set the path only if the file exists.
			if os.path.exists(path):
				self.path = path
			else:
				if path is self.__init__.defaults[0]:
					sys.exit("\"vars.json\" not found. Please create a vars.json file and place it in this directory.")
				else:
					print("Supplied path \"{}\" does not exist. Trying default \"vars.json\".".format(path))
					if not os.path.exists("vars.json"):
						sys.exit("The file \"vars.json\" does not exist. Please create the file from the provided template and try again.")
				self.path = "vars.json"

		def __getitem__(self, var: str):
			# Get a var from the var store
			return self.json[var]

		def loadVars(self):
			# Open the var file
			self.varFile = open(self.path, "r+")
			self.rawJson = self.varFile.read()

			# Print the vars to STDOUT for debugging
			print(self.rawJson)

			self.json = json.loads(self.rawJson)

		def saveVars(self):
			# Check if the var file is still open
			if self.varFile.closed:
				# Re-open it if it is closed
				self.varFile = open(self.path, "r+")

			# Generate a JSON dump
			self.rawJson = json.dumps(json)

			# Write the JSON dump to disk
			self.varFile.write(json_dump)

		def updateVar(self, var: str, val: str):
			# Update a var
			self.json[var] = val

	__sStore = None

	def __init__(self, path:str = "vars.json"):
		__sStore = self.__class__.__sStore
		# Skip loading a new file if we've already got one
		if __sStore == None:
			self.__class__.__sStore = self.__class__.__Singleton_Store(path)

	def __getitem__(self, var: str):
		return self.__sStore[var]

	def __eq__(self, obj):
		return type(self) == type(obj)

	def loadVars(self):
		self.__sStore.loadVars()

	def saveVars(self):
		self.__sStore.saveVars()
		
	def updateVar(self, var: str, val: str):
		self.__sStore.updateVar(var, val)