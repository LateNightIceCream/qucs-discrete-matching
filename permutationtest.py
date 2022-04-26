import itertools

c = list(range(1,37))
l = []

components = c + l

def shuffle (l, r):
	product = itertools.product(l, repeat=r)
	return product

def replace_template_components(templatefile, replacements):
	# read template file
	with open(templatefile, "r") as f:
	
		i = 0
		outlines = ""
	
		for line in f:
			if isTemplateComponent(line):
				pass

			outlines.append(line)

k = shuffle(components, 4)




#print(list(k))
print(len(list(k)))


# loop over all component combinations
for mapping in k:
	# create new file
	s = replace_template_components(k)
	
	# simulate file
	
	
	# store results
	
	# delete file
	
	# evaluate results
	
	pass