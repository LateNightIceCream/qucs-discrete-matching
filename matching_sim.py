#!/usr/bin/env python3

import os
import pathlib
import itertools
import subprocess
import numpy as np
import logging as l
import concurrent.futures
from enum import Enum
from random import shuffle

import python_qucs_lnic.qucs.simulate as qucssim

# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------

def _abs_path(path_string):
    return str(pathlib.Path(path_string).resolve())

# ------------------------------------------------------------------------------

class C_type(Enum):
    spfile  = "SPfile"
    spice  = "SPICE"

# ------------------------------------------------------------------------------

class Component():
    def __init__(self, path):
        self.path = path
        self.filename = str(self.path.resolve())
        self.name = self.path.stem
        self.type = self._get_type()

    # --------------------------------------------------------------------------

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

    # --------------------------------------------------------------------------

    def get_netlist_string(self, netstring):
        '''
        netstring example:
            Sub:TEMPLATE_n _net0 _net1 ...
        '''
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

    # --------------------------------------------------------------------------

    def get_schematic_string(self, schtring):
        pass

    # --------------------------------------------------------------------------

    def to_spice_netlist(self, i = 1): # TODO: rename: to_spice_def?

        if not self.type == C_type.spice:
            return None
        output = subprocess.check_output('qucsconv -if spice -of qucs -i ' + self.filename, shell=True, text=True)
        output = str(output)
        start  = '.Def:'
        end    = '.Def:End'
        def_only = output[output.find(start):output.rfind(end)+len(end)]
        # add additional .def for sub
        spice = '.Def:%s _net1 _net2\n%s\nSub:X%s _net1 _net2 Type="%s"\n.Def:End\n' % (self.name + '_sp', def_only, str(i), self.name.upper())

        return spice

# ------------------------------------------------------------------------------

class Schematic:
    def __init__(self, schfile):
        self.file = schfile
        self.lines = self.load_lines()

    def load_lines(self):
        with open(self.file, 'r') as f:
            self.lines = f.readlines()
        return self.lines

# ------------------------------------------------------------------------------

class ResultSchematic(Schematic):
    def __init__(self, schfile):
        super().__init__(schfile)

    def append(self, result):
        '''
        TODO:
        - copy:
          - Power Sources -> change numbers
          - Template Components -> change line, keep basic stuff
          - Wires

        - change y offset of EVERYTHING <<<---- maybe do this one first, so copy + change offset
        '''
        pass

# ------------------------------------------------------------------------------

class Netlist:
    def __init__(self, filepath):
        self.file = filepath
        self.lines = None
        self.template_line_indices = None

    # --------------------------------------------------------------------------

    def generate_from(self, schematic):
            '''
            generates netlist from .sch
            using qucs -n
            '''
            infile  = schematic.file
            outfile = self.file
            subprocess.run('qucs -n -i %s -o %s' % (str(infile), str(outfile)), shell=True)
            self.lines = self.get_lines()
            self.template_line_indices = self.get_template_line_indices()

    # --------------------------------------------------------------------------

    def spice_it_up(self, components):
        '''
        put all spice components into netlist template
        '''
        spice_components = []

        with open(self.file, 'r+') as f:
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
                spice = component.to_spice_netlist(i)
                if not spice: # ignore s2p
                    continue
                f.writelines(spice)
                i += 1
            f.writelines(old_stuff)

        self.lines = self.get_lines()
        self.template_line_indices = self.get_template_line_indices()

    # --------------------------------------------------------------------------

    def get_lines(self):
        l = []
        with open(self.file, 'r') as f:
            l = f.readlines()
        return l

    # --------------------------------------------------------------------------

    def get_template_line_indices(self):
        line_indices = []
        i = 0
        for line in self.lines:
            if line.startswith('Sub:TEMPLATE') or line.startswith('SPfile:TEMPLATE'):
                line_indices.append(i)
            i += 1
        return line_indices

# ------------------------------------------------------------------------------

class Evaluator:
    def __init__(self):
        pass

    def evaluate(self, result):
        pass

    def get_result_str(self, result, unit = 'dB'):
        return 'please implement the get_result_str() function in your Evaluator'

    def print_result(self, result):
        l.info(self.get_result_str(result))
        l.info('======================')

# ------------------------------------------------------------------------------

class Manager:
    def __init__(self, template_schematic, output_schematic, template_netlist, component_dir, logfile, evaluator, nsimulations = -1):
        self.template_schematic = Schematic(pathlib.Path(template_schematic))
        self.result_schematic   = ResultSchematic(pathlib.Path(output_schematic))
        self.template_netlist   = Netlist(pathlib.Path(template_netlist))
        self.component_dir      = pathlib.Path(component_dir)
        self.logfile            = pathlib.Path(logfile)
        self.nsimulations       = nsimulations
        self.components         = None
        self.ncomponents        = None
        self.component_variations = None
        self.simulations        = None
        self.evaluator          = evaluator

        self.started = False
        self.best_data = None
        self.best_variation = None

    # --------------------------------------------------------------------------

    def get_component_files(self):
        files = []
        for file in pathlib.Path(self.component_dir).glob('**/*'):
            fstr = str(file).lower()
            if fstr.endswith('.sp') or fstr.endswith('.s2p'):
                files.append(file)
        return files

    # --------------------------------------------------------------------------

    def print_summary(self):
        l.info('-------------------')
        l.info('MATCHING SIMULATION')
        l.info('-------------------')
        l.info('Template Schematic: %s' % str(_abs_path(self.template_schematic.file)))
        l.info('Template Netlist: %s' % str(_abs_path(self.template_netlist.file)))
        l.info('Component Directory: %s' % str(_abs_path(self.component_dir)))
        #l.info('Result Schematic %s' % str(_abs_path(self.result_schematic)))
        l.info('Log File: %s' % str(_abs_path(self.logfile)))
        l.info('Num. of template components: %s' % str(self.ncomponents))
        l.info('Num. of simulations: %s' % str(self.nsimulations))
        l.info('-------------------')

    # --------------------------------------------------------------------------

    def create_components(self, files):
        components = []
        for file in files:
            components.append(Component(file))
        self.components = components
        return components

    # --------------------------------------------------------------------------

    def generate_permutations(self):
        product = itertools.product(self.components, repeat=self.ncomponents)
        self.component_variations = list(product)
        return list(product)

    # --------------------------------------------------------------------------

    def generate_simulations(self):
        i = 0
        sims = []
        for variation in self.component_variations:
            name = 'simulation_' + str(i)
            sim_description = MySimulationDescription(name, self.template_netlist, variation)
            sims.append(qucssim.Simulation(sim_description))
            i += 1
        self.simulations = sims
        return sims

    # --------------------------------------------------------------------------

    def evaluate(self, result):
        return self.evaluator.evaluate(result)

    # --------------------------------------------------------------------------

    def sim_thread(self, sim, i):
        res = None
        try:
            sim.run_extract()
            #res = self.goal_function(sim.results)
        except Exception as exc:
            l.error('simulation failed to run: %s' % (str(exc)))

        # DELETE
        os.remove(sim.netlist)
        var = sim.simulation_description.component_variation
        return (i, sim.results, var)

    # --------------------------------------------------------------------------

    def thread_it(self):
        if not self.started:
            l.info('simulation started')
            self.started = True
        # spawn the simulation threads
        n_done = 0
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures_notdone = set()
            futures_done = set()
            maxf = 20

            for i, sim in enumerate(self.simulations):
                futures_notdone.add(executor.submit(self.sim_thread, sim, i))

                if len(futures_notdone) >= maxf:
                    done, futures_notdone = concurrent.futures.wait(futures_notdone, return_when=concurrent.futures.FIRST_COMPLETED)
                    futures_done.update(done)

                if len(futures_done) >= 1:
                    while futures_done:
                        result = futures_done.pop().result()
                        k = result[0]

                        ev_result = self.evaluate(result)
                        if ev_result:
                            self.evaluator.print_result(ev_result)
                            self.append_to_result_schematic(result)

                        # clear results from memory!
                        self.simulations[k].results = None
                        #del self.simulations[k].simulation_description # TODO: really delete this?
                        n_done += 1
                    if n_done % 100 == 0:
                        l.info('progress: %s / %s' % (str(n_done), str(self.nsimulations)))

        # check the rest that is not % maxf
        for future in concurrent.futures.as_completed(futures_notdone):
            result = future.result()
            ev_result = self.evaluate(result)
            if ev_result:
                self.evaluator.print_result(ev_result)
        for future in futures_done:
            result = future.result()
            ev_result = self.evaluate(result)
            if ev_result:
                self.evaluator.print_result(ev_result)

    # --------------------------------------------------------------------------

    def sim_init(self):
        # TODO: errors
        component_files = self.get_component_files()
        if len(component_files) == 0:
            raise FileNotFoundError('no component files found in %s' % _abs_path(self.component_dir))
            return

        self.create_components(component_files)
        self.template_netlist.generate_from(self.template_schematic)
        self.template_netlist.spice_it_up(self.components)
        self.ncomponents = len(self.template_netlist.template_line_indices)
        self.generate_permutations()
        if self.nsimulations < 0:
            self.nsimulations = len(self.component_variations)
        self.component_variations = self.component_variations[:(self.nsimulations)]
        shuffle(self.component_variations)
        self.generate_simulations()
        self.print_summary()

    # --------------------------------------------------------------------------

    def run(self):
        try:
            self.sim_init()
        except Exception as exc:
            l.error('Initialization error! ' + str(exc))

        self.thread_it()

    # --------------------------------------------------------------------------

    def append_to_result_schematic(self, result):
        self.result_schematic.append(result)

# ------------------------------------------------------------------------------

class MySimulationDescription(qucssim.SimulationDescription):
    def __init__(self, name, tmp_netlist, component_variation):
        self.name = name
        self.tmp_netlist = tmp_netlist # memory?
        self.component_variation = component_variation
        #self.component_names = self.get_component_names() # e.g. ['TEMPLATE_3', 'TEMPLATE_4', 'TEMPLATE_8']; TODO: not really needed
        #self.components = dict(zip(self.component_names, self.component_variation))

    def modify_netlist(self):
        # replace all template components in netlist lines
        self.component_names = []
        new_netlist_lines = self.tmp_netlist.lines
        n = 0
        for index in self.tmp_netlist.template_line_indices:
            new_netlist_lines[index] = self.component_variation[n].get_netlist_string(self.tmp_netlist.lines[index])
            n+=1
        # # TODO: \n already included in line?
        new_netlist_string = ''.join(new_netlist_lines)
        return new_netlist_string

    def get_component_names(self):
        comp_names = []
        n = 0
        for index in self.tmp_netlist.template_line_indices:
            #new_netlist_lines[index] = self.component_variation[n].get_netlist_string(self.tmp_netlist.lines[index])
            line = self.tmp_netlist.lines[index]
            lstrip = line.strip()
            comp_names.append(lstrip[lstrip.find(':'):lstrip.find(' ')])
            n += 1

        return comp_names
