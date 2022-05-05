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
import timeit
import time
import math
from datetime import datetime

# TODO for v2:
# keep track of component names
# automatically generate templates from results
# plot "best" solutions (filtered solutions) to be able to scroll through them
# print results without =============


parser = argparse.ArgumentParser(description='Weird Simulation of Matching Networks for Discrete Component Files')
parser.add_argument('-q', '--qucspath', type=str, help='path to qucs directory containing qucs, qucsconv and qucsator', default='')
parser.add_argument('-t', '--templatefile', type=str, help='qucs template .sch file to use', default='template.sch')
parser.add_argument('-u', '--netlistfile', type=str, help='qucs output netlist file to use', default='netlist_template.txt')
parser.add_argument('-d', '--componentdir', type=str, help='path to component directory containing .sp or .s2p files (can be nested)', default='components/')
parser.add_argument('-n', '--nsimulations', type=int, help='max number of simulations', default=-1)
parser.add_argument('-o', '--outfile', type=str, help='output file name', default='results.txt')
templatefile = None

# TODO: make qucspath common, create SimulationManager class or similar
# TODO: clean up this mess with windows PATH
import python_qucs_lnic.qucs.simulate as qucssim

l.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

def append_result_to_schematic(filename, variation):
    pass

def get_timestamp(verb = False):
    d = datetime.now()
    s = d.strftime('%Y-%m-%d')
    if verb:
        s += d.strftime('@%H:%M:%S')
    return s

def get_netlist_lines(file):
    l = []
    with open(file, 'r') as f:
        l = f.readlines()

    return l

def get_template_line_indices(lines):
    template_line_indices = []
    i = 0
    for line in lines:
        if line.startswith('Sub:TEMPLATE') or line.startswith('SPfile:TEMPLATE'):
            template_line_indices.append(i)
        i += 1
    return template_line_indices

template_netlist_lines = []
template_line_indices = []

class MySimulationDescription(qucssim.SimulationDescription):
    def __init__(self, name, template_netlist_file, component_variation):
        global template_netlist_lines
        global template_line_indices
        self.name = name
        self.component_variation = component_variation
        self.template_netlist_file = template_netlist_file # path to netlist.txt template file
        # save the whole file to not open it every time
        # might take a lot of space :c
        self.template_netlist_lines = template_netlist_lines
        self.template_line_indices = template_line_indices

    def modify_netlist(self):
        new_netlist_lines = template_netlist_lines

        n = 0
        for index in template_line_indices:
            new_netlist_lines[index] = self.component_variation[n].get_netlist_string(template_netlist_lines[index])
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

def generate_netlist(infile, outfile = 'netlist.txt'):
    # TODO: error handling
    '''
    generates netlist from .sch
    using qucs -n
    '''
    subprocess.run('qucs -n -i %s -o %s' % (str(infile), str(outfile)), shell=True)

# ------------------------------------------------------------------------------

def component_to_spice_netlist(component, i = 1):

    if not component.type == C_type.spice:
        return None
    #command = 'qucsconv' + ' -if spice -of qucs -i ' + component.filename

    output = subprocess.check_output('qucsconv -if spice -of qucs -i ' + component.filename, shell=True, text=True)
    output = str(output)
    start = '.Def:'
    end   = '.Def:End'
    def_only = output[output.find(start):output.rfind(end)+len(end)]

    # add additional .def for sub
    spice = '.Def:%s _net1 _net2\n%s\nSub:X%s _net1 _net2 Type="%s"\n.Def:End\n' % (component.name + '_sp', def_only, str(i), component.name.upper())

    return spice

# ------------------------------------------------------------------------------

def spice_up_netlist(netlistfile, components):
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
            spice = component_to_spice_netlist(component, i)
            if not spice: # ignore s2p
                continue
            f.writelines(spice)
            i += 1
        f.writelines(old_stuff)

# ------------------------------------------------------------------------------

def variations_to_simulations(variations, netlist_template):
    i = 0
    sims = []
    for variation in variations:
        name = 'simulation_' + str(i)
        sim_description = MySimulationDescription(name, netlist_template, variation)
        sims.append(qucssim.Simulation(sim_description))
        i += 1

    return sims

# ------------------------------------------------------------------------------

def evaluate_data(sim_dat):
    '''
    minimize the maximum value of s11
    inside the frequency range of interest
    '''
    #f_1_l = 780e6
    #f_1_h = 980e6
    #f_2_l = 1710e6
    #f_2_h = 1910e6

    f_1_l = 790e6
    f_1_h = 960e6
    f_2_l = 1710e6
    f_2_h = 1880e6

    freq = np.array(sim_dat["frequency"])

    s11_db = np.array(sim_dat["S11_dB"])
    freq_indices_1 = [i for i, n in enumerate(freq) if (n > f_1_l and n < f_1_h)]
    freq_indices_2 = [i for i, n in enumerate(freq) if (n > f_2_l and n < f_2_h)]
    s11_db_1 = s11_db[freq_indices_1]
    s11_db_2 = s11_db[freq_indices_2]

    #return min(s11_db)
    return ((max(s11_db_1), min(s11_db_1)), (max(s11_db_2), min(s11_db_2)))

# ------------------------------------------------------------------------------

sim_started = False
def sim_thread(sim, i):

    #if comp_vars[i] == sim.simulation_description.component_variation:
    #    l.info('equal!')
    #else:
    #    l.error('unequal!')

    global sim_started
    if not sim_started:
        l.info('simulation started')
        sim_started = True


    l.debug('simulation ' + str(i))
    res = None
    try:
        sim.run_extract()
        #sim.extract_data()
        res = evaluate_data(sim.results)
    except:
        l.error('simulation failed to run')

    # DELETE
    os.remove(sim.netlist)
    var = sim.simulation_description.component_variation
    #os.remove(sim.out)
    #return (sim.simulation_description.component_variation, res)
    # TODO: problem maybe?
    return (i, res, var)

# ------------------------------------------------------------------------------

def get_result_str(data, variation, unit = 'dB'):
    maxdb_1 = data[0][0]
    mindb_1 = data[0][1]
    maxdb_2 = data[1][0]
    mindb_2 = data[1][1]
    s = ''
    s += 'S11_max_1: %s %s\n' % (str(maxdb_1), unit)
    s += 'S11_min_1: %s %s\n' % (str(mindb_1), unit)
    s += 'S11_max_2: %s %s\n' % (str(maxdb_2), unit)
    s += 'S11_min_2: %s %s\n' % (str(mindb_2), unit)
    s += 'produced by\n'
    for component in variation:
        s += component.name + '\n'
    s+= '============\n'
    return s

def print_results(data, variation, unit = 'dB'):
    l.info(get_result_str(data, variation, unit))



best_data = 0
best_max_1 = 0
best_max_2 = 0
best_variation = None
def sim_evaluation(i, data, variation):
    global best_data
    global best_max_1
    global best_max_2
    global best_variation
    global templatefile

    data_1 = data[0]
    data_2 = data[1]
    maxdb_1 = data_1[0]
    mindb_1 = data_1[1]
    maxdb_2 = data_2[0]
    mindb_2 = data_2[1]

    if (mindb_1 < -10 and maxdb_1 < -3 and mindb_2 < -10 and maxdb_2 < -3):
        if (maxdb_1 < best_max_1 and maxdb_2 < best_max_2):
            l.info('==============')
            l.info('NEW BEST')
            l.info('==============')
            best_max_1 = maxdb_1
            best_max_2 = maxdb_2
            best_data = data
            best_variation = variation
            with open('results_opt.txt', 'w+') as f:
                f.write(get_result_str(data, best_variation))

        #append_result_to_schematic(templatefile, variation)

        print_results(data, variation)


# ------------------------------------------------------------------------------
def thread_it(simulations, component_variations):
    i = 0
    global best_data
    global best_variation
    tot = len(component_variations)
    n_done = 0

    with concurrent.futures.ThreadPoolExecutor() as executor:

        futures_notdone = set()
        futures_done = set()
        maxf = 2000

        for i, sim in enumerate(simulations):
            futures_notdone.add(executor.submit(sim_thread, sim, i))
            if len(futures_notdone) >= maxf:
                done, futures_notdone = concurrent.futures.wait(futures_notdone, return_when=concurrent.futures.FIRST_COMPLETED)
                futures_done.update(done)

            if len(futures_done) >= 1:
                while futures_done:
                    i, data, variation = futures_done.pop().result()

                    sim_evaluation(i, data, variation) 

                    # clear memory
                    simulations[i].results = None 
                    del simulations[i].simulation_description
                    n_done += 1
                if n_done % 100 == 0:
                    l.info('progress: %s / %s' % (str(n_done), str(tot)))

    # check the rest thats not % maxf
    for future in concurrent.futures.as_completed(futures_notdone):
        i, data, variation = future.result()
        sim_evaluation(i, data, variation)

    for future in futures_done:
        i, data, variation = future.result()
        sim_evaluation(i, data, variation)

    return (best_data, best_variation)

# ------------------------------------------------------------------------------

def abs_path(path_string):
    return str(pathlib.Path(path_string).resolve())

#@profile
def main():
    args = parser.parse_args()
    component_dir = args.componentdir
    global templatefile
    templatefile  = args.templatefile
    nsimulations  = args.nsimulations
    qucspath      = args.qucspath
    outputfile    = args.outfile
    netlistfile   = args.netlistfile #'netlist_template.txt'
    # TODO: turn into command line argument

    # put qucs into PATH
    env = ''
    if qucspath != '':
        env = sys.path.append(abs_path(qucspath))

    try:
        #subprocess.run(['qucs', '--help'], stdout=subprocess.DEVNULL, shell=True)
        subprocess.run('qucs --help', stdout=subprocess.DEVNULL, shell=True)
    except Exception as exc:
        l.error('could not execute qucs ' + str(exc))
        return -1

    # get component files
    component_files = get_component_files(pathlib.Path(component_dir))
    if len(component_files) == 0:
        l.error('no component files found in ' + abs_path(component_dir))
        return -1

    print("ok!")

    # convert to component objects
    components = create_components(component_files)

    # convert template.sch to netlist_template.txt
    generate_netlist(templatefile, netlistfile)

    # paste all spice components into netlist
    # TODO: check impact on simulation speed
    spice_up_netlist(netlistfile, components)

    # TODO: memory optimization, currently global variable
    global template_netlist_lines
    global template_line_indices
    template_netlist_lines = get_netlist_lines(netlistfile)
    template_line_indices  = get_template_line_indices(template_netlist_lines)

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
    simulations = variations_to_simulations(component_variations, netlistfile)

    l.info("Total number of simulations: %s" % (str(len(simulations))))
    l.error("just a test to make sure errors work")

    # create a thread for each simulation
    # make sure to delete all netlists and output files after the thread is done
    result = thread_it(simulations, component_variations)

    best_data = result[0]
    best_variation = result[1]
    l.info("Done!")
    print_results(best_data, best_variation)
    with open(outputfile, 'w+') as f:
        f.write('------------------\n')
        f.write(get_timestamp(True) + '\n')
        f.write('------------------\n')
        f.write(get_result_str(best_data, best_variation)+'\n')
        f.write('------------------\n')

    # remove netlistfile
    os.remove(netlistfile)

if __name__ == "__main__":
    main()

# ------------------------------------------------------------------------------
