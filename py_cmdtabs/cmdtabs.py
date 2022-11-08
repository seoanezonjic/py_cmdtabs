import sys

class CmdTabs:
	def load_input_data(input_path, sep="\t", limit=1):
		if input_path == '-':
			input_data = sys.stdin
		else:
			input_data = open(input_path, "r").readlines()
		input_data_arr = []
		for line in input_data:
			#print('---', file=sys.stderr)
			input_data_arr.append(line.rstrip().split(sep, limit))
		return input_data_arr
