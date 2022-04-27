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
import subprocess
import numpy as np
import logging as l

# TODO: clean up this mess with windows PATH
import python_qucs_3.qucs.simulate as qucssim

l.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"))


class MySimulationDescription(qucssim.SimulationDescription):
	def __init__(self, name, template_netlist_file, component_variation):
		self.name = name
		self.component_variation = component_variation
		self.template_netlist_file = template_netlist_file # path to netlist.txt template file
		# save the whole file to not open it every time
		# might take a lot of space :c
		self.template_netlist_lines = self.get_netlist_lines()
		self.template_line_indices = self.get_template_line_indices()

	def modify_netlist(self):

		new_netlist_lines = self.template_netlist_lines

		# for line in self.template_netlist_lines:
		# 	if line.startswith('Sub:TEMPLATE') or line.startswith('SPfile:TEMPLATE'):
		# 		new_netlist_lines[i] = self.component_variation[n].get_netlist_string(line)
		# 		n += 0
		# 	i += 1

		n = 0
		for index in self.template_line_indices:
			new_netlist_lines[index] = self.component_variation[n].get_netlist_string(self.template_netlist_lines[index])
			n+=1

		# # TODO: \n already included in line?
		return '\n'.join(self.new_netlist_lines)

	def get_template_line_indices(self):
		template_line_indices = []
		i = 0
		for line in self.template_netlist_lines:
			if line.startswith('Sub:TEMPLATE') or line.startswith('SPfile:TEMPLATE'):
				template_line_indices.append(i)
				i += 1
		return template_line_indices

	def get_netlist_lines(self):
		with open(self.template_netlist_file, 'r') as f:
			self.template_netlist_lines = f.readlines()

	# def remove_netlist_file(self):
	# 	'''
	# 	see Simulation.modify_netlist()
	# 	'''
	# 	netlists_folder_name = 'netlists'
	# 	filename = os.path.join(netlists_folder_name,'netlist_%s.txt' % self.name)
	# 	os.remove(filename)


# ------------------------------------------------------------------------------

class Component():
	def __init__(self, path):
		self.path = path
		self.filename = str(self.path.resolve())
		self.name = self.path.stem
		self.type = self._get_type()

	def _get_type(self):
		type = None
		ending = self.filename.split('.')[-1].lower()
		try:
			if ending == "s2p":
				type = C_type.spfile
			elif ending == "sp":
				type = C_type.spice
			else:
				raise TypeError('invalid file ending ' + ending)
		except Exception as exc:
			l.error(e)
		return type

	def get_netlist_string(self, netstring):
		'''
		netstring example:
			Sub:TEMPLATE_n _net0 _net1 ...
		'''
		#netstring_ident = netstring[netstring.find('_'):netstring.find()]
		netstring_ident = netstring.split(' ')
		netstring_ident = '%s %s %s' % (netstring_ident[0][-1], netstring_ident[1], netstring_ident[2])
		new_netstring = ''

		if self.type == C_type.spice:
			new_netstring = 'Sub:TEMPLATE_%s Type="%s"' % (netstring_ident, self.name)

		elif self.type == C_type.spfile:
			new_netstring = 'SPfile:TEMPLATE_%s gnd File="{%s}" Data="rectangular" Interpolator="linear" duringDC="open"' % (netstring_ident, self.filename)

		return new_netstring

# ------------------------------------------------------------------------------

class C_type(Enum):
	spfile  = "SPfile"
	spice  = "SPICE"

# ------------------------------------------------------------------------------

def shuffle (l, r):
	product = itertools.product(l, repeat=r)
	return list(product)

# ------------------------------------------------------------------------------

def get_component_files(dir):
	files = []
	for file in pathlib.Path(dir).glob('**/*'):
		fstr = str(file).lower()
		if fstr.endswith('.sp') or fstr.endswith('.s2p'):
			files.append(file)
	return files

# ------------------------------------------------------------------------------

def create_components(files):
	components = []
	for file in files:
		components.append(Component(file))

	return components

# ------------------------------------------------------------------------------

def qucs_command(qucspath):
	'''
	checks if qucs exists and if not returns qucspath/qucs.exe
	'''
	try:
		subprocess.run('qucs --help')
		return 'qucs'
	except:
		print('command qucs not found, please specify path')

	return pathlib.Path(qucspath + '\\qucs')

def qucsator_command(qucspath):
	'''
	checks if qucsator exists and if not returns qucspath/qucsator.exe
	'''
	try:
		subprocess.run('qucsator --help')
		return 'qucsator'
	except:
		print('command qucsator not found, please specify path')

	return pathlib.Path(qucspath + '\\qucsator')

# ------------------------------------------------------------------------------

def generate_netlist(infile, outfile = 'netlist.txt', qucscommand = 'qucs'):
	# TODO: error handling
	'''
	generates netlist from .sch
	using qucs -n
	'''
	#os.system('C:\\Users\\rg\\Desktop\\qucs-0.0.19-win32-mingw482-asco-freehdl-adms\\bin\\qucs.exe -n -i ' + str(infile) + ' -o ' + str(outfile))
	subprocess.run('%s -n -i %s -o %s' % (qucscommand, str(infile), str(outfile)))
	#os.system('C:\\Users\\rg\\Desktop\\qucs-0.0.19-win32-mingw482-asco-freehdl-adms\\bin\\qucs.exe -n -i ' + str(infile) + ' -o ' + str(outfile))

# ------------------------------------------------------------------------------

def component_to_spice_netlist(component, qucsconvcommand = 'qucsconv'):

	if not component.type == C_type.spice:
		return None
	command = str(qucsconvcommand) + ' -if spice -of qucs -i ' + component.filename

	output = str(bytes(subprocess.check_output(command)))
	start = '.Def:'
	end   = '.Def:End'
	def_only = output[output.find(start):output.rfind(end)+len(end)]
	print(str(def_only))

	return def_only

# ------------------------------------------------------------------------------

def spice_up_netlist(netlistfile, components, qucsconvcommand = 'qucsconv'):
	'''
	put all spice components into netlist template
	'''
	spice_components = []

	with open(netlistfile, 'r+') as f:
		old_stuff = f.readlines()
		f.seek(0, 0)
		for component in components:
			spice = component_to_spice_netlist(component, qucsconvcommand)
			if not spice:
				# ignore .s2p
				continue
			f.writelines(spice + '\n')
		f.writelines(old_stuff)

# ------------------------------------------------------------------------------

def variations_to_simulations(variations, netlist_template):
	i = 0
	sims = []
	for variation in variations:
		name = 'simulation_' + str(i)
		sim_description = MySimulationDescription(name, netlist_template)
		sims.append(qucssim.Simulation(sim_description))
		i += 1

	return sims

# ------------------------------------------------------------------------------

def sim_thread(sim, i):
	l.debug('simulation ' + str(i))
	os.remove(sim.netlist)
	os.remove(sim.out)

	res = 0

	return res

def main():

	component_dir = 'components/'
	templatefile  = 'template_rewrite.sch'
	netlistfile   = 'netlist_template.txt'
	# TODO: turn into command line argument
	qucspath      = 'C:\\Users\\rg\\Desktop\\qucs-0.0.19-win32-mingw482-asco-freehdl-adms\\bin'

	qucscommand     = qucs_command(qucspath)
	qucsatorcommand = qucsator_command(qucspath)
	qucsconvcommand = pathlib.Path(qucspath + '\\qucsconv')

	# get component files
	component_files = get_component_files(component_dir)

	# convert to component objects
	components = create_components(component_files)

	# convert template.sch to netlist_template.txt
	generate_netlist(templatefile, netlistfile, qucscommand)

	# paste all spice components into netlist
	# TODO: check impact on simulation speed
	spice_up_netlist(netlistfile, components, qucsconvcommand)

	# create all permutations of components
	# with length r
	# TODO: externally adjustable parameter r
	component_variations = shuffle(components, 3)

	# create an array of simulations (descriptions)
	# with each variation
	simulations = variations_to_simulations(component_variations, netlistfile)

	# create a thread for each simulation
	# make sure to delete all netlists and output files after the thread is done
	with concurrent.futures.ThreadPoolExecutor() as executor:
		future_to_simulation = []
		i = 0
		for simulation in simulations:
			future_to_simulation.append(executor.submit(sim_thread, simulation, i))
			i += 1

	# evaluate
		i = 0
		best_data = 0
		for future in concurrent.futures.as_completed(future_to_simulation):
			try:
				#data = future.result()[1]
				#variation = future.result()[0]
				# if data < best_data:
				# 	best_data = data
				# 	print(data)
				pass
			except Exception as exc:
				print("simulation generated an exception: %s" % exc)
			else:
				pass
			i += 1

if __name__ == "__main__":
    main()

# ------------------------------------------------------------------------------
