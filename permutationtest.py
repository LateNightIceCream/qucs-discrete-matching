import itertools
from enum import Enum
import pathlib
import sys
import math

c = list(range(1,37))
l = []

components = c + l

def printProgressBar (iteration, total, prefix = '[', suffix = ']', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
	"""
	Call in a loop to create terminal progress bar
	@params:
		iteration   - Required  : current iteration (Int)
		total       - Required  : total iterations (Int)
		prefix      - Optional  : prefix string (Str)
		suffix      - Optional  : suffix string (Str)
		decimals    - Optional  : positive number of decimals in percent complete (Int)
		length      - Optional  : character length of bar (Int)
		fill        - Optional  : bar fill character (Str)
		printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
	"""
	if not (iteration % math.floor(total/100) == 0):
		return
		
	percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
	filledLength = int(length * iteration // total)
	bar = fill * filledLength + '-' * (length - filledLength)
	print(f'\r{prefix} {bar} {percent}% {suffix}', end = printEnd)
	# Print New Line on Complete
	if iteration == total: 
		print()

class C_type(Enum):
	s1p = 1
	sp  = 2

class Component:
	def __init__(self, filename):
		self.filename = filename
		self.type 	  = get_type(filename)
		
	def get_type(self, filename):
		return C_type.s1p
	
	def _get_coordinates_from_string(self, str):
		pass
	
	def get_qucs_string_by_template(self, templatestr):
		
		str = ""
		
		if self.type == C_type.s1p:
			str = "<s1p placeholder>"
		elif self.type == C_type.sp:
			str = "<s2p placeholder>"
		else:
			str = "<undefined component type>"
		
		return "<" + self.type + " placeholder>"

def shuffle (l, r):
	product = itertools.product(l, repeat=r)
	return list(product)

def is_template_component(line):
	return True

def replace_template_components(templatelines, replacements):
	# read template file
	outlines = []
	
	i = 0
	
	for line in templatelines:
		# find next template line
		if is_template_component(line):
			# replace with component
			#line = replacements[i].get_qucs_string_by_template(line)
			i += 1

		outlines.append(line)
			
	return outlines

def get_template_lines(file):
	lines = []
	with open(file, "r") as f:
		lines = f.readlines()
	
	return lines

# ----------------------------------------------------------------------------

# get all components
c_dir         = "components/C"
l_dir         = "components/L"
TEMPLATEFILE  = "template.sch"
TEMPLATELINES = get_template_lines(TEMPLATEFILE)

component_files = []
components = []

for filepath in pathlib.Path(c_dir).glob('**/*'):
    component_files.append(filepath)
	
for filepath in pathlib.Path(l_dir).glob('**/*'):
    component_files.append(filepath)

for file in component_files:
	components.append(file)

component_variations = shuffle(components, 4)

print("number of simulations: " + str(len(component_variations)))

# ----------------------------------------------------------------------------

i = 0
num_of_simulations = len(component_variations)
# loop over all component combinations
for variation in component_variations:

	printProgressBar(i, num_of_simulations)

	# create new file
	s = replace_template_components(TEMPLATELINES, variation)
	
	# simulate file
	
	
	# store results
	
	# delete file
	
	# evaluate results
	
	i += 1
	
	pass