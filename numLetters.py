
def numLetters(string_list):
	tokens_dict_dict = dict()
	for i in string_list:
		tokens = dict()
		for c in i:
			if c not in tokens:
				tokens[c] = 1
			elif c in tokens:
				tokens[c] += 1
		tokens_dict_dict[i] = tokens
	print(tokens_dict_dict)

def main():
	import sys
	args = sys.argv[1:]
	numLetters(args)

main()
