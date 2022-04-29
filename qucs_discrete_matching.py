#!/usr/bin/env python3
import itertools
from enum import Enum
import pathlib
import os
import sys
import concurrent.futures
import subprocess
import numpy as np
import logging as l
import argparse
from random import shuffle

parser = argparse.ArgumentParser(description='Weird Simulation of Matching Networks for Discrete Component Files')
parser.add_argument('-q', '--qucspath', type=str, help='path to qucs directory containing qucs, qucsconv and qucsator', default='')
parser.add_argument('-t', '--templatefile', type=str, help='qucs template .sch file to use', default='template.sch')
parser.add_argument('-d', '--componentdir', type=str, help='path to component directory containing .sp or .s2p files (can be nested)', default='components/')
parser.add_argument('-n', '--nsimulations', type=int, help='max number of simulations', default=-1)

# TODO: make qucspath common, create SimulationManager class or similar
# TODO: clean up this mess with windows PATH
import python_qucs_lnic.qucs.simulate as qucssim

l.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

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

		n = 0
		for index in self.template_line_indices:
			new_netlist_lines[index] = self.component_variation[n].get_netlist_string(self.template_netlist_lines[index])
			n+=1
		# # TODO: \n already included in line?
		new_netlist_string = ''.join(new_netlist_lines)
		return new_netlist_string

	def get_template_line_indices(self):
		template_line_indices = []
		i = 0
		for line in self.template_netlist_lines:
			if line.startswith('Sub:TEMPLATE') or line.startswith('SPfile:TEMPLATE'):
				template_line_indices.append(i)
			i += 1
		return template_line_indices

	def get_netlist_lines(self):
		l = []
		with open(self.template_netlist_file, 'r') as f:
			l = f.readlines()

		return l

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
			# \n from experimentation, maybe not put it here
			#new_netstring = 'Sub:TEMPLATE_%s Type="%s"\n' % (netstring_ident, self.name.upper())
			new_netstring = 'Sub:TEMPLATE_%s Type="%s"\n' % (netstring_ident, self.name + '_sp')

		elif self.type == C_type.spfile:
			new_netstring = 'SPfile:TEMPLATE_%s gnd File="{%s}" Data="rectangular" Interpolator="linear" duringDC="open"\n' % (netstring_ident, self.filename)

		return new_netstring

# ------------------------------------------------------------------------------

class C_type(Enum):
	spfile  = "SPfile"
	spice  = "SPICE"

# ------------------------------------------------------------------------------

def generate_permutations(l, r):
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

def get_command(path, command):
	return os.path.join(path, command)

# ------------------------------------------------------------------------------

def generate_netlist(infile, outfile = 'netlist.txt', qucspath = ''):
	# TODO: error handling
	'''
	generates netlist from .sch
	using qucs -n
	'''
	qucscommand = get_command(qucspath, 'qucs')
	subprocess.run('%s -n -i %s -o %s' % (qucscommand, str(infile), str(outfile)))

# ------------------------------------------------------------------------------

def component_to_spice_netlist(component, qucspath = '', i = 1):

	if not component.type == C_type.spice:
		return None
	command = get_command(qucspath, 'qucsconv') + ' -if spice -of qucs -i ' + component.filename

	output = str(subprocess.check_output(command, text=True))
	start = '.Def:'
	end   = '.Def:End'
	def_only = output[output.find(start):output.rfind(end)+len(end)]

	# add additional .def for sub
	spice = '.Def:%s _net1 _net2\n%s\nSub:X%s _net1 _net2 Type="%s"\n.Def:End\n' % (component.name + '_sp', def_only, str(i), component.name.upper())

	return spice

# ------------------------------------------------------------------------------

def spice_up_netlist(netlistfile, components, qucspath = ''):
	'''
	put all spice components into netlist template
	'''
	spice_components = []

	with open(netlistfile, 'r+') as f:
		old_stuff = f.readlines()
		# remove old subcircuit definitions
		# (very crude)
		# TODO: find better way
		# BUG: should check if any .def exists
		def_indices = [i for i, s in enumerate(old_stuff) if '.Def:' in s]
		try:
			old_stuff = old_stuff[0:def_indices[0]] + old_stuff[def_indices[-1]+1:]
		except:
			pass

		f.seek(0, 0)
		i = 1
		for component in components:
			spice = component_to_spice_netlist(component, qucspath, i)
			if not spice: # ignore s2p
				continue
			f.writelines(spice)
			i += 1
		f.writelines(old_stuff)

# ------------------------------------------------------------------------------

def variations_to_simulations(variations, netlist_template, qucspath):
	i = 0
	sims = []
	for variation in variations:
		name = 'simulation_' + str(i)
		sim_description = MySimulationDescription(name, netlist_template, variation)
		sims.append(qucssim.Simulation(sim_description, qucspath))
		i += 1

	return sims

# ------------------------------------------------------------------------------

def evaluate_data(sim_dat):
	'''
	minimize the maximum value of s11
	inside the frequency range of interest
	'''
	f_1_l = 780e6
	f_1_h = 980e6
	f_2_l = 1710e6
	f_2_h = 1910e6

	freq = np.array(sim_dat["frequency"])
	s11_db = np.array(sim_dat["S11_dB"])
	freq_indices = [i for i, n in enumerate(freq) if (n > f_1_l and n < f_1_h) or (n > f_2_l and n < f_2_h)]
	s11_db = s11_db[freq_indices]
	#return min(s11_db)
	return max(s11_db)

# ------------------------------------------------------------------------------

def sim_thread(sim, i):
	l.debug('simulation ' + str(i))
	res = None
	try:
		sim.run()
		sim.extract_data()
		res = evaluate_data(sim.results)
	except:
		l.error('simulation failed to run')

	os.remove(sim.netlist)
	os.remove(sim.out)
	return (sim.simulation_description.component_variation, res)

# ------------------------------------------------------------------------------

def print_results(data, variation, unit = 'dB'):
	l.info('S11: %s %s' % (str(data), unit))
	l.info('produced by')
	for component in variation:
		l.info(component.name)
	l.info('============')

# ------------------------------------------------------------------------------

def thread_it(simulations, component_variations):
	with concurrent.futures.ThreadPoolExecutor() as executor:
		future_to_simulation = []
		i = 0
		for simulation in simulations:
			future_to_simulation.append(executor.submit(sim_thread, simulation, i))
			i += 1

		i = 0
		best_data = 0
		best_variation = None
		target = -1
		use_target = True
		dat = []
		for future in concurrent.futures.as_completed(future_to_simulation):
			try:
				res = future.result()
				data = res[1]
				variation = res[0]
				dat.append(data)
				datlen = len(dat)
				if datlen % 100 == 0:
					l.info("progress: " + str(datlen) + ' / ' + str(len(component_variations)))

				if data < best_data:
					best_data = data
					best_variation = variation
					print_results(data, variation)

				# there's still threads left over
				#if use_target and best_data < target:
				#	break

			except Exception as exc:
				l.error("simulation generated an exception: %s" % exc)
			else:
				pass
			i += 1

		return (best_data, best_variation)

# ------------------------------------------------------------------------------

def abs_path(path_string):
	return str(pathlib.Path(path_string).resolve())

def main():
	args = parser.parse_args()
	component_dir = args.componentdir
	templatefile  = args.templatefile
	nsimulations  = args.nsimulations
	qucspath      = args.qucspath
	netlistfile   = 'netlist_template.txt'
	# TODO: turn into command line argument

	# put qucs into PATH
	if qucspath != '':
		sys.path.insert(0, qucspath)

	try:
		subprocess.run(['qucs', '--help'], stdout=subprocess.DEVNULL)
	except Exception as exc:
		l.error('could not execute qucs ' + str(exc))
		return -1

	# get component files
	component_files = get_component_files(pathlib.Path(component_dir))
	if len(component_files) == 0:
		l.error('no component files found in ' + abs_path(component_dir))
		return -1

	# convert to component objects
	components = create_components(component_files)

	# convert template.sch to netlist_template.txt
	generate_netlist(templatefile, netlistfile, qucspath)

	# paste all spice components into netlist
	# TODO: check impact on simulation speed
	spice_up_netlist(netlistfile, components, qucspath)

	# determine number of template components
	# TODO: rework
	tmpsimdescr = MySimulationDescription('tmp', netlistfile, None)
	ncomponents = len(tmpsimdescr.template_line_indices)
	l.info('Number of detected Template Components: ' + str(ncomponents))

	# create all permutations of components
	# with length r
	# TODO: externally adjustable parameter r
	component_variations = generate_permutations(components, ncomponents)
	if nsimulations != -1:
		try:
			component_variations = component_variations[:nsimulations]
		except Exception as exc:
			l.error('nsimulations is higher than number of simulations. ' + str(exc))
			return -1

	# "Monte Carlo"
	shuffle(component_variations)

	# create an array of simulations (descriptions)
	# with each variation
	simulations = variations_to_simulations(component_variations, netlistfile, qucspath)

	l.error("just a test to make sure errors work")

	# create a thread for each simulation
	# make sure to delete all netlists and output files after the thread is done
	result = thread_it(simulations, component_variations)

	l.info("Done!")
	print_results(result[0], result[1])

if __name__ == "__main__":
    main()

# ------------------------------------------------------------------------------
