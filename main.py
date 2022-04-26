#!/usr/bin/env python3

# QUCS component format
# <type name active x y xtext ytext mirrorX rotate "Value1" visible "Value2" visible ...>

TEMPLATE_FILE   = 'template.sch'
SPFILE_TEMPLATE = '\"rectangular\" 0 \"linear\" 0 \"open\" 0 \"1\" 0'

# -----------------------------------------------------------------------------

class Component:
    def __init__(self, type, name, props):
        self.type  = type
        self.name  = name
        self.bprops = props

class SPfile(Component):
    def __init__(self, name, props, file):
        Component.__init__(self, 'SPfile')
        self.name   = SPfile
        self.bprops = props
        self.file   = file

    def get_string(self):
        pass

# -----------------------------------------------------------------------------

def get_component_basic_properties(compstr):
    '''
    basic properties are first seven values after type and name:
    name active x y xtext ytext mirrorX rotate
    '''
    vals = compstr.split(' ')
    return ' '.join(vals[2:9])

# -----------------------------------------------------------------------------

def get_qucs_section_lines(filename, descriptor):
    # BUG: Section not found results in infinite loop
    with open(filename, 'r') as f:
        lines = []
        for line in iter(f.readline, '<{}>\n'.format(descriptor)):
            pass
        for line in iter(f.readline, '</{}>\n'.format(descriptor)):
            lines.append(line)
    return lines

# -----------------------------------------------------------------------------

def get_qucs_components(compstr, type):
    '''
    compstr: string to search in
    type:    component type, e.g. 'R'
    returns  list of lines with the component type
    '''
    lines = []
    for line in compstr:
        line = line.strip()
        if line.startswith('<{}'.format(type)):
            lines.append(line)

    return lines

# -----------------------------------------------------------------------------

def main():
    component_lines = get_qucs_section_lines(TEMPLATE_FILE, 'Components')
    matching_components = get_qucs_components(component_lines, 'R')
    print(get_component_basic_properties(matching_components[0]))


if __name__ == "__main__":
    main()
