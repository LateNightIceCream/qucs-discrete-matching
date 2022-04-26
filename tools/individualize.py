import sys

INFILE      = sys.argv[1]

#ENDLINE = '.Def:End\n'
ENDLINE = ''
#STARTMARK = '.Def:'
STARTMARK = '.subckt'
ENDMARK = '.ends'

outnames = []
outlines = []
file_suffix = '.sp'

n = -1

def get_file_name (line):
    #return line.split()[0][line.find(':') + 1:]
    return line.split()[1] + file_suffix
    #return get_comp_type() + '_' + get_comp_size_from_line(line) + '_' + get_comp_value_from_line(line) + ".sch"

with open(INFILE, 'r') as f:

    started = False
    outstring = ''

    for line in f:

        if line.startswith(STARTMARK) and (line != ENDLINE or not line.startswith(ENDMARK)):
            outnames.append(get_file_name(line))
            started = True

        if started:
            outstring += line

        if line == ENDLINE or line.startswith(ENDMARK):
            started = False
            outlines.append(outstring)
            outstring = ''


i = 0
for element in outlines:

    print(element)

    with open(outnames[i], 'w') as f:
        f.write(element)
        f.write('.END')

    i += 1

#input("enter to exit")
