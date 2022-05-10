'''
Erstellt eine s1p datei und ersetzt die werte in den entspr. frequenzbereichen
'''

INFILE  = 'Ausgangsmessung.s1p'
OUTFILE = 'bp_LTE.s1p'

F_LOWER_1 = 790e6
F_UPPER_1 = 960e6
F_LOWER_2 = 1710e6
F_UPPER_2 = 1880e6

LOW_MAG = -15 #dB

output = []
unit_line = ''
with open(INFILE, 'r') as f:
	for line in f:

		if line[0] == '!':
			continue
		if line[0] == '#':
			unit_line = line
			continue

		floats_list = []
		for item in line.split():
  			floats_list.append(float(item))

		ff = floats_list[0]

		phase = 0
		mag   = 0
		if (ff >= F_LOWER_1 and ff <= F_UPPER_1) or (ff >= F_LOWER_2 and ff <= F_UPPER_2):
			mag = LOW_MAG

		output.append(str(ff) + " " + str(mag) + " " + str(phase) + "\n")

with open(OUTFILE, 'w') as f:
	f.write(unit_line)

	for line in output:
		f.write(line)
