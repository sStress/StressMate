class StressPrediction():
	def __init__(self, p):
		self.p = p

	def predict_stress(self, word):
		temp_word = '$' + word + '$$'
		stress_vector = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		final_vector = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		stressed_vowel = 0
		maximum = 0

		chuncks = []
		i = -1
		for letter in temp_word.lower():
			i += 1
			if letter in 'ёуеыаоэяию':
				chuncks.append(temp_word.lower()[i - 1:i + 3])

		counter = 0
		for chunck in chuncks:
			if chunck in self.p:
				if counter >= 0:
					stress_vector[counter] += self.p[chunck]
				counter += 1
			else:
				stress_vector[counter] = 0.001
				counter += 1

		for j in range(14):
			others_unstressed = 1
			for k in range(14):
				if k != j and k > 0:
					others_unstressed *= (1 - (stress_vector[k]))
			final_vector[j] = stress_vector[j] * others_unstressed

		for m in range(len(final_vector) - 1):
			if final_vector[m] > maximum:
				maximum = final_vector[m]
				stressed_vowel = m

		lc = -1
		lt = 0
		final = ''
		for c in word:
			lt += 1
			if c in 'ЁУЕЫАОЭЯИЮёуеыаоэяию':
				lc += 1
			if lc == stressed_vowel:
				final += word[:lt] + "'" + word[lt:]
				break

		#return word[:stressed_vowel] + "'" + word[stressed_vowel:] 
		#return final_vector
		return final