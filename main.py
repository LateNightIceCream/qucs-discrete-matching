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

import matching_sim

# ------------------------------------------------------------------------------

l.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

parser = argparse.ArgumentParser(description='Weird Simulation of Matching Networks for Discrete Component Files')
parser.add_argument('-q', '--qucspath',     type=str, help='path to qucs directory containing qucs, qucsconv and qucsator', default='')
parser.add_argument('-t', '--templatefile', type=str, help='qucs template .sch file to use', default='template.sch')
parser.add_argument('-u', '--netlistfile',  type=str, help='qucs output netlist file to use', default='netlist_template.txt')
parser.add_argument('-d', '--componentdir', type=str, help='path to component directory containing .sp or .s2p files (can be nested)', default='components/')
parser.add_argument('-n', '--nsimulations', type=int, help='max number of simulations', default=-1)
parser.add_argument('-o', '--outfile',      type=str, help='output schematic file name', default='results.sch')
parser.add_argument('-l', '--logfile',      type=str, help='log file name', default='results.log')

# ------------------------------------------------------------------------------

class MyEvaluator(matching_sim.Evaluator):
    def __init__(self):
        self.best_max_1 = 0
        self.best_max_2 = 0
        self.best_variation = None

    def evaluate(self, result):
        '''
        gets called on every simulation result
        return result if 'optimal'
        return None else
        result = [i, sim_data, variation]
        '''
        i         = result[0]
        sim_dat   = result[1]
        variation = result[2]
        goal = self.goal_function(sim_dat)
        self.goal = goal

        maxdb_1 = goal[0][0]
        mindb_1 = goal[0][1]
        maxdb_2 = goal[1][0]
        mindb_2 = goal[1][1]

        if (mindb_1 < -0 and maxdb_1 < -0 and mindb_2 < -0 and maxdb_2 < -0):
            if (maxdb_1 < self.best_max_1 and maxdb_2 < self.best_max_2):
                l.info('==============')
                l.info('NEW BEST')
                l.info('==============')
                self.best_max_1 = maxdb_1
                self.best_max_2 = maxdb_2
                self.best_variation = variation
            return result
        return None

    # --------------------------------------------------------------------------

    def goal_function(self, sim_dat):
        '''
        minimize the maximum value of s11
        inside the frequency range of interest
        '''
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

    # --------------------------------------------------------------------------

    def get_result_str(self, result):
        # TODO: implement im main / MyEvaluator
        i = result[0]
        variation = result[2]
        maxdb_1 = self.goal[0][0]
        mindb_1 = self.goal[0][1]
        maxdb_2 = self.goal[1][0]
        mindb_2 = self.goal[1][1] # hacky

        unit = 'dB'
        s = ''
        s += 'S11_max_1: %s %s\n' % (str(maxdb_1), unit)
        s += 'S11_min_1: %s %s\n' % (str(mindb_1), unit)
        s += 'S11_max_2: %s %s\n' % (str(maxdb_2), unit)
        s += 'S11_min_2: %s %s\n' % (str(mindb_2), unit)
        s += 'produced by\n'
        for component in variation:
            s += component.name + '\n'
        return s


# ------------------------------------------------------------------------------

def main():
    args = parser.parse_args()
    qucspath        = args.qucspath
    component_dir   = args.componentdir
    templ_schematic = args.templatefile
    templ_netlist   = args.netlistfile #'netlist_template.txt'
    outfile         = args.outfile
    logfile         = args.logfile
    nsimulations    = args.nsimulations

    if qucspath != '':
        sys.path.append(abs_path(qucspath))

    try:
        subprocess.call('qucs --help', stdout=subprocess.DEVNULL, shell=True)
    except Exception as exc:
        l.error('could not find qucs.' + str(exc))
        return -1

    evaluator = MyEvaluator()

    if os.path.exists(outfile):
        os.remove(outfile)

    # convert to component objects
    sim_manager = matching_sim.Manager(templ_schematic, outfile, templ_netlist, component_dir, logfile, evaluator, nsimulations)
    sim_manager.run()

if __name__ == "__main__":
    main()

