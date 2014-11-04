from nltk.corpus import wordnet as wn
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk import pos_tag
from pattern import en
from pattern.en import PAST,PRESENT,PROGRESSIVE,pluralize,singularize
import re

def lengthen(word, pos, lod):
	
	synonymList = [];
	wordNetSynset =  wn.synsets(word, pos=pos)

	if len(wordNetSynset) > 0 and len(wordNetSynset) < lod:
		for synWords in wordNetSynset[0].lemma_names:
			synonymList.append(synWords)

		longest = synonymList[0];
		for i in synonymList:
			if len(i) > len(longest):
				longest = i;
		if (len(longest)) == len(word):
			return word;
		return " ".join(longest.split("_"));
	else:
		return word;

# Open File
f = open("input_essay.txt")
lines = f.read();

first_length = len(lines);

# Tokenize
sentences = sent_tokenize(lines);

new_essay = ""

tokenizer = RegexpTokenizer(r'\w+')

for s in sentences:
	new_sentence = s;
	words = tokenizer.tokenize(s);

	tagged_words = pos_tag(words);

	for w in tagged_words:
		# Find the longest synonym

		pos = w[1];

		new_word = w[0];

		if pos == "NN":
			new_word = lengthen(w[0], wn.NOUN, 5)
			new_word = new_word;
		if pos == "NNS":
			new_word = lengthen(singularize(w[0]), wn.NOUN, 5)
			new_word = pluralize(new_word);
		elif pos[0] == "V":
			new_word = lengthen(w[0], wn.VERB, 5)

			if pos == "VBD":
				new_word = en.conjugate(new_word, tense=PAST);
			if pos == "VBG":
				new_word = en.conjugate(new_word, tense=PRESENT, aspect=PROGRESSIVE)
			if pos == "VBN":
				new_word = en.conjugate(new_word, tense=PAST, );
		elif pos == "RB" or pos == "RBR" or pos == "RBS":
			new_word = lengthen(w[0], wn.ADV,5)
		elif pos == "JJ" or pos == "JJR" or pos == "JJS":
			new_word = lengthen(w[0], wn.ADJ, 5)

		my_reg = '\\b' + w[0] + '\\b';
		new_sentence = re.sub(my_reg, new_word, new_sentence);
		# print(new_sentence)
		# new_sentence = new_sentence.replace(w[0] + " ", new_word + " ");
		# new_sentence = new_sentence.replace(" " + w[0], " " + new_word);
	new_essay += (" " + new_sentence[0].upper() + new_sentence[1: len(new_sentence)]);


# Output
second_length = len(new_essay);

print(first_length);
print(second_length);
print(str(int(float(second_length) / float(first_length) * 100) - 100) + "% increase in length");

f = open("output_essay.txt", 'w')
f.write(new_essay)
f.close()