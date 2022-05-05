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
#import python_qucs_lnic.qucs.simulate as qucssim

# TODO for v2:
# keep track of component names
# automatically generate templates from results
# plot "best" solutions (filtered solutions) to be able to scroll through them
# print results without =============

# ------------------------------------------------------------------------------

l.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

parser = argparse.ArgumentParser(description='Weird Simulation of Matching Networks for Discrete Component Files')
parser.add_argument('-q', '--qucspath',     type=str, help='path to qucs directory containing qucs, qucsconv and qucsator', default='')
parser.add_argument('-t', '--templatefile', type=str, help='qucs template .sch file to use', default='template.sch')
parser.add_argument('-u', '--netlistfile',  type=str, help='qucs output netlist file to use', default='netlist_template.txt')
parser.add_argument('-d', '--componentdir', type=str, help='path to component directory containing .sp or .s2p files (can be nested)', default='components/')
parser.add_argument('-n', '--nsimulations', type=int, help='max number of simulations', default=-1)
parser.add_argument('-o', '--outfile',      type=str, help='output schematic file name', default='results.txt')
parser.add_argument('-l', '--logfile',      type=str, help='log file name', default='results.log')

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

    # convert to component objects
    sim_manager = matching_sim.Manager(templ_schematic, templ_netlist, component_dir, logfile, nsimulations)
    sim_manager.run()
    sim_manager.create_result_schematic(outfile)

if __name__ == "__main__":
    main()

