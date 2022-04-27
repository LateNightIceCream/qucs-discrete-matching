#!/usr/bin/env python3

from enum import Enum
import pathlib
import sys


class C_type(Enum):
    spfile  = "SPfile"
    spice  = "SPICE"

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


subcomponent = Component(pathlib.Path("components/C/CSRF_0402_885392005002_0R4pF.sp"))
s2pcomponent = Component(pathlib.Path("components/L/7447840010.s2p"))

nettempline = 'SPfile:TEMPLATE_2 _net0 _net1 gnd File=\"{C:/Users/rg/Desktop/qucs-discrete-matching/components/L/74279271.s2p}\" Data=\"rectangular\" Interpolator=\"linear\" duringDC=\"open\"'

new_netstring1 = subcomponent.get_netlist_string(nettempline)
new_netstring2 = s2pcomponent.get_netlist_string(nettempline)

print(new_netstring1)
print(new_netstring2)
