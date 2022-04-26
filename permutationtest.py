import itertools
from enum import Enum
import pathlib
import sys
import math
import os

c = list(range(1,37))
l = []

components = c + l

# ------------------------------------------------------------------------------

def printProgressBar (iteration, total, prefix = '[', suffix = ']', decimals = 1, length = 60, fill = '█', printEnd = "\r"):
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

# ------------------------------------------------------------------------------

class C_type(Enum):
	s2p = "SPfile"
	spfile  = "SPfile"

# ------------------------------------------------------------------------------

class Component:
	def __init__(self, qucs_str):
		self.str = qucs_str
		self.name = self._get_name()
		self.type = self._get_type()
		self.basic_properties = self._get_basic_properties()

		print(self.basic_properties)

	def _get_type(self):
		return "unused"

	def _get_name(self):
		return self.str.split(' ')[3]

	def _get_basic_properties(self):
		'''
		basic properties are first seven values after type and name:
		name active x y xtext ytext mirrorX rotate
		'''
		vals = self.str.split(' ')
		return ' '.join(vals[4:9])

	def change_to(self, replacement):
		'''
		keep properties but change to replacement component
		'''
		return replacement.build_qucs_string(self.name, self.basic_properties)

# ------------------------------------------------------------------------------

class ReplacementComponent:
	def __init__(self, file):
		self.file = file
		self.filename = self._get_filename()
		self.type = self._get_type()

	def _get_filename(self):
		return str(self.file.resolve())

	def _get_type(self):
		'''
		!TODO!
		'''
		return C_type.s2p

	def build_qucs_string(self, name, basic_properties):
		type = self.type.value
		specifics = ""

		if self.type == C_type.s2p:
			specifics = '0 0 ' + '\"' + self.filename + '\" ' + '1 \"rectangular\" 0 \"linear\" 0 \"open\" 0 \"2\"'

		elif self.type == C_type.spfile:
			specifics = "placeholder :D"

		return '<' + type + ' ' + name + ' ' + basic_properties + ' ' + specifics + '>'


# ------------------------------------------------------------------------------

class SchTemplate:
	def __init__(self, filename):
		self._filename = filename
		self.lines = self._get_lines_from_file(filename)

		(p, l, comp) = self._get_template_lines()
		self.component_positions = p
		self.template_lines = l
		self.template_components = comp

	def _get_lines_from_file(self, filename):
		l = ""
		with open(filename, "r") as f:
			l = f.readlines()
		return l


	def _is_template_component(self, line):
		if line.strip().startswith("<SPfile X"):
			return True
		return False

	def _get_template_lines(self):
		pos = []
		lines = []
		comps = []
		i = 0
		for line in self.lines:
			if self._is_template_component(line):
				lines.append(line)
				pos.append(i)
				comps.append(Component(line))
			i += 1
		return (pos, lines, comps)

	def replace_template_components(self, replacements):
		i = 0
		replaced_lines = self.lines
		for pos in self.component_positions:
			#replaced_lines[pos] = "hellu\n"
			replaced_lines[pos] = self.template_components[i].change_to(replacements[i]) + '\n'
			i += 1

		return replaced_lines

	def create_variation_file(self, path, variation):
		lines = self.replace_template_components(variation)
		filestr = ''.join(lines)
		with open(path, "w+") as f:
			f.write(filestr)

# ------------------------------------------------------------------------------

def shuffle (l, r):
	product = itertools.product(l, repeat=r)
	return list(product)

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

C_DIR 	      = "components/C"
L_DIR         = "components/L"
TEMPLATEFILE  = "template.sch"
TMP_DIR       = "temp/"

def main():
    # get all components
	template = SchTemplate(TEMPLATEFILE)

	component_files = []
	components = []

	for filepath in pathlib.Path(C_DIR).glob('**/*'):
		component_files.append(filepath)

	for filepath in pathlib.Path(L_DIR).glob('**/*'):
		component_files.append(filepath)

	for file in component_files:
		components.append(ReplacementComponent(file))

	component_variations = shuffle(components, 4)

	print("number of simulations: " + str(len(component_variations)))

	template.create_variation_file("testfile.sch", component_variations[0])

	i = 0
	num_of_simulations = len(component_variations)
	# loop over all component combinations
	for variation in component_variations:

		#printProgressBar(i, num_of_simulations)

		# create new file
		filename = TMP_DIR + "schematic_" + str(i) + ".sch"
		template.create_variation_file(filename, variation)

		# simulate file


		# store results

		# evaluate results
		best_val = 0
		best_variation = variation
		res = opt_function(result_csv)
		if res < best_val:
			best_val = res

		# delete file
		os.remove(filename)

		i += 1


if __name__ == "__main__":
    main()

# ------------------------------------------------------------------------------
