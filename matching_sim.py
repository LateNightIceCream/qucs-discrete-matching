#!/usr/bin/env python3

import pathlib
import itertools
import subprocess
import logging as l
from enum import Enum
from random import shuffle

import python_qucs_lnic.qucs.simulate as qucssim

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

    def to_spice_netlist(self, i = 1):

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

class Manager:
    def __init__(self, template_schematic, template_netlist, component_dir, logfile, nsimulations = -1):
        self.template_schematic = Schematic(pathlib.Path(template_schematic))
        self.template_netlist   = Netlist(pathlib.Path(template_netlist))
        self.component_dir      = pathlib.Path(component_dir)
        self.logfile            = pathlib.Path(logfile)
        self.nsimulations       = nsimulations
        self.result_schematic   = None
        self.components         = None
        self.ncomponents        = None
        self.component_variations = None
        self.simulations        = None

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

    def get_component_variations(self, components, ncomponents):
        pass

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
            sim_description = MySimulationDescription(name, netlist_template, variation)
            sims.append(qucssim.Simulation(sim_description))
            i += 1
        self.simulations = sims
        return sims

    # --------------------------------------------------------------------------

    def thread_it(self):
        pass

    # --------------------------------------------------------------------------

    def sim_init(self):
        # get component files
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
        self.component_variations = self.component_variations[:(self.nsimulations - 1)]
        shuffle(self.component_variations)

        self.generate_simulations()
        self.print_summary()

    # --------------------------------------------------------------------------

    def run(self):
        #try:
        #    self.sim_init()
        #except Exception as exc:
        #    l.error('Initialization error! ' + str(exc))

        self.sim_init()

    # --------------------------------------------------------------------------

    def create_result_schematic(self, sch_file):
        pass
