'''
Functions to work with anagrams:
	char_freq:
		Returns dictionary with keys of characters in a string and values as their frequency.
	factorial:
		Computes factorial.
	anagram_freq:
		Computes frequency of anagrams for a string given character frequency and factorials.
'''
def char_freq(word):
	freq = {}	
	for letter in list(word):
		if letter not in freq:
			freq[letter] = 0
		freq[letter] += 1
	return freq

def factorial(n):
	f = 1
	for i in range(2, n + 1):
		f *= i
	return f
	
def anagram_freq(word):
	letters = char_freq(word)
	denom = 1
	for letter in letters.values():
		denom *= factorial(letter)
	return factorial(len(word)) // denom

def main():
	import sys
	if sys.argv[1] == 'f':
		print(anagram_freq(sys.argv[2]))

if __name__ == '__main__':
	main()
