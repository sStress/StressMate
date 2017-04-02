import stress_prediction
import tokenizer
import re
import json

def initialize_forms(filename):
	all_forms = {}
	with open(filename, encoding='utf-8') as all_forms_file:
		for form in all_forms_file:
			if "'" in form:
				form = form.strip('\n')
				unstressed_form = re.sub("['`]", '', form)
				if unstressed_form in all_forms:
					all_forms[unstressed_form].append(form.find("'"))
				else:
					all_forms[unstressed_form] = [form.find("'")]
	return all_forms

def is_small(word):
	counter = 0
	for letter in word:
		if letter in 'ёуеыаоэяиюЁУЕЫАОЭЯИЮ':
			counter = counter + 1
	if counter <= 1:
		return True

def is_in_dictionary(dictionary, word):
	if word.lower() in dictionary:
		return True
	else:
		return False

def dictionary_stress(dictionary, word):
	stressed_word = ''
	lword = word.lower()
	if len(dictionary[lword]) == 1:
		stressed_word = word[:dictionary[lword][0]] + "'" + word[dictionary[lword][0]:]
	else:
		temp_word = []
		for i, letter in enumerate(word):
			temp_word.append(letter)
			if i + 1 in dictionary[lword]:
				temp_word.append("'")
		stressed_word = ''.join(temp_word)
	return stressed_word

def load_text(filename):
	text = ''
	with open(filename, encoding='utf-8') as text_file:
		text = text_file.read()
	return text

def main():
	p = json.load(open('stress_probabilities.sm'), encoding='utf-8')
	sp = stress_prediction.StressPrediction(p)
	all_forms_filename = 'ruwiktionary_zalizniak.sm'
	all_forms = initialize_forms(all_forms_filename)
	text = ''
	while True:
		try:
			text_path = input('Введите имя файла, в котором нужно проставить ударения: ')
			text = load_text(text_path)
			break
		except FileNotFoundError:
			print('Такого файла не существует!')
	tokens = tokenizer.tokenize(text)
	stressed_text = ''
	for token in tokens:
		if is_small(token):
			stressed_text += token
		elif is_in_dictionary(all_forms, token):
			stressed_text += dictionary_stress(all_forms, token)
		else:
			stressed_text += sp.predict_stress(token)
	print(stressed_text)

if __name__ == '__main__':
	main()
