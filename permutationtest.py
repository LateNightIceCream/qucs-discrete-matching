import itertools
from enum import Enum
import pathlib
import sys
import math
import os
import threading
import concurrent.futures
import queue
import cmath
import pprint
import numpy as np

# TODO: clean up this mess with windows PATH
import python_qucs.qucs.simulate as qucssim

c = list(range(1,37))
l = []

components = c + l


# ok now i know how it works, this needs a rewrite :D
class MySimulationDescription(qucssim.SimulationDescription):
	def __init__(self, name, netfile):
		self.name = name
		#self.template_netlist_file = os.path.abspath('netlist.txt') # path to netlist.txt
		self.template_netlist_file = netfile

	def modify_netlist(self):
		return self.template_netlist_file

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
	spfile  = "SPfile"
	spice  = "SPICE"

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
		return ' '.join(vals[4:11])

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
		self.string_specifics = self._get_string_specifics()

	def _get_filename(self):
		return str(self.file.resolve())

	def _get_type(self):
		type = None
		ending = self.filename.split('.')[-1].lower()
		if ending == "s2p":
			type = C_type.spfile
		elif ending == "sp":
			type = C_type.spice
		else:
			print("unknown ending " + ending)

		return type

	def _get_string_specifics(self):
		specifics = ""
		if self.type == C_type.spfile:
			#print("spfile")
			specifics = '\"' + self.filename + '\" ' + '1 \"rectangular\" 0 \"linear\" 0 \"open\" 0 \"2\"'

		elif self.type == C_type.spice:
			#print("spice")
			specifics = '\"' + self.filename + '\" ' + '1 \"_net1,_net2\" 0 \"yes\" 0 \"none\" 0'
		else:
			print("----")
			print(specifics)
			print("error at replacement component string specifics")
			print("----")

		return specifics

	def build_qucs_string(self, name, basic_properties):
		type = self.type.value
		specifics = self.string_specifics
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
		if line.strip().startswith("<SPfile TEMPLATE") or line.strip().startswith("<SPICE TEMPLATE"):
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

def generate_netlist(infile, outfile = "netlist.txt"):
	# TODO: error handling
	os.system('C:\\Users\\rg\\Desktop\\qucs-0.0.19-win32-mingw482-asco-freehdl-adms\\bin\\qucs.exe -n -i ' + str(infile) + ' -o ' + str(outfile))

# ------------------------------------------------------------------------------

def evaluate_results(sim_dat):
	'''
	minimize the maximum value of s11
	inside the frequency range of interest
	'''
	f_1_l = 780e6
	f_1_h = 980e6
	f_2_l = 1710e6
	f_2_h = 1910e6

	freq = np.array(sim_dat["frequency"])
	#freq = sim_dat["frequency"]
	s11_db = np.array(sim_dat["S11_dB"])
	#freq_indices = np.where((freq > f_1_l and freq < f_1_h) or (freq > f_2_l and freq < f_2_h))
	freq_indices = [i for i, n in enumerate(freq) if (n > f_1_l and n < f_1_h) or (n > f_2_l and n < f_2_h)]
	s11_db = s11_db[freq_indices]
	return max(s11_db)

# ------------------------------------------------------------------------------

def sim_worker(template, variation, i):
	name = "sim_" + str(i)
	filename = TMP_DIR + "schematic_" + str(i) + ".sch"
	netlistfile = "netlists/netlist_" + str(i) + ".txt"
	template.create_variation_file(filename, variation)
	# convert to netlist
	generate_netlist(filename, netlistfile)
	# simulate netlist
	sim_description = MySimulationDescription(name, netlistfile)
	sim = qucssim.Simulation(sim_description)
	sim.run()
	# store results
	sim.extract_data()
	# evaluate results
	res = evaluate_results(sim.results)
	# delete file
	os.remove(filename)
	os.remove(netlistfile)
	return (variation, res)


C_DIR 	      = "components/C"
L_DIR         = "components/L"
TEMPLATEFILE  = "template.sch"
TMP_DIR       = "temp/"

def main():
    # get all components
	template = SchTemplate(TEMPLATEFILE)

	component_files = []
	components = []

	test = os.listdir(C_DIR)
	for item in test:
		if item.endswith(".sp.lst"):
			os.remove(os.path.join(C_DIR, item))

	for filepath in pathlib.Path(C_DIR).glob('**/*'):
		component_files.append(filepath)

	for filepath in pathlib.Path(L_DIR).glob('**/*'):
		component_files.append(filepath)

	for file in component_files:
		components.append(ReplacementComponent(file))

	# TODO change suffle number r to some adjustable parameter
	component_variations = shuffle(components, 3)

	print("Setup done. Starting simulation")
	print("number of simulations: " + str(len(component_variations)))

	template.create_variation_file("testfile.sch", component_variations[0])
	generate_netlist("testfile.sch")

	sim_description = MySimulationDescription("test_simulation", "netlist.txt")
	sim = qucssim.Simulation(sim_description)
	sim.run()
	#sim.extract_data()

	# would be faster to directly edit the netlist every time instead of creating
	# a new one
	# TODO: REWRITE

	# a thread will return its opt_value evaluation

	i = 0
	num_of_simulations = len(component_variations)

	component_variations = component_variations[:300]

	with concurrent.futures.ThreadPoolExecutor() as executor:
			future_to_variation = []
			for variation in component_variations:
				future_to_variation.append(executor.submit(sim_worker, template, variation, i))
				i += 1

			i = 0
			best_data = 0
			for future in concurrent.futures.as_completed(future_to_variation):
				url = "p " + str(i)
				try:
					data = future.result()[1]
					variation = future.result()[0]
					print(data)
					if data < best_data:
						best_data = data
						print("--------")
						print(str(best_data) + " produced by ")
						for v in variation:
							print(v.file)
						print("--------")

				except Exception as exc:
					print("%r generated an exception: %s" % (url, exc))
				else:
					pass
				i += 1

	# loop over all component combinations
	'''
	for variation in component_variations:

		#printProgressBar(i, num_of_simulations)
		#print("current simulation: " + str(i), end = "\r")

		# create new file
		filename = TMP_DIR + "schematic_" + str(i) + ".sch"
		template.create_variation_file(filename, variation)

		# convert to netlist
		generate_netlist(filename)

		# simulate netlist
		sim_description = MySimulationDescription("test_simulation")
		sim = qucssim.Simulation(sim_description)
		sim.run()

		# store results
		sim.extract_data()

		# evaluate results
		best_val = 0
		best_variation = variation
		#res = opt_function(result_csv)
		#if res < best_val:
		#	best_val = res

		# delete file
		os.remove(filename)

		i += 1
		'''

if __name__ == "__main__":
    main()

# ------------------------------------------------------------------------------
