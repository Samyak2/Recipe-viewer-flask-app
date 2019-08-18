from pickle import load
from numpy import array
from numpy import argmax
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
from nltk.translate.bleu_score import corpus_bleu

# load a clean dataset
def load_dataset(filename):
    data = []
    f = open(filename, "r")
    content = f.read()
    content = content.split("##")[1:]
    for datapoint in content:
        datapoint = datapoint[datapoint.find("\n")+1:]
        text = datapoint.split("#")[0]
        # for i in datapoint.split("#"):
        ing = datapoint[datapoint.find("#ingredients")+len("#ingredients"):datapoint.rfind("#steps")]
        step = datapoint[datapoint.find("#steps")+len("#steps"):datapoint.rfind("\n")]
        data.append([text, ing])
    return array(data)

# fit a tokenizer
def create_tokenizer(lines):
	tokenizer = Tokenizer()
	tokenizer.fit_on_texts(lines)
	return tokenizer

# max sentence length
def max_length(lines):
	return max(len(line.split()) for line in lines)

# encode and pad sequences
def encode_sequences(tokenizer, length, lines):
	# integer encode sequences
	X = tokenizer.texts_to_sequences(lines)
	# pad sequences with 0 values
	X = pad_sequences(X, maxlen=length, padding='post')
	return X

# map an integer to a word
def word_for_id(integer, tokenizer):
	for word, index in tokenizer.word_index.items():
		if index == integer:
			return word
	return None

# generate target given source sequence
def predict_sequence(model, tokenizer, source):
	prediction = model.predict(source, verbose=0)[0]
	integers = [argmax(vector) for vector in prediction]
	target = list()
	for i in integers:
		word = word_for_id(i, tokenizer)
		if word is None:
			break
		target.append(word)
	return ' '.join(target)

# evaluate the skill of the model
def evaluate_model(model, tokenizer, sources, raw_dataset):
	actual, predicted = list(), list()
	for i, source in enumerate(sources):
		# translate encoded source text
		source = source.reshape((1, source.shape[0]))
		translation = predict_sequence(model, eng_tokenizer, source)
		raw_target, raw_src = raw_dataset[i]
		if i < 10:
			print('src=[%s], target=[%s], predicted=[%s]' % (raw_src, raw_target, translation))
		actual.append([raw_target.split()])
		predicted.append(translation.split())
	# calculate BLEU score
	print('BLEU-1: %f' % corpus_bleu(actual, predicted, weights=(1.0, 0, 0, 0)))
	print('BLEU-2: %f' % corpus_bleu(actual, predicted, weights=(0.5, 0.5, 0, 0)))
	print('BLEU-3: %f' % corpus_bleu(actual, predicted, weights=(0.3, 0.3, 0.3, 0)))
	print('BLEU-4: %f' % corpus_bleu(actual, predicted, weights=(0.25, 0.25, 0.25, 0.25)))

# load datasets
dataset = load_dataset('dataset.txt')
# prepare english tokenizer
eng_tokenizer = create_tokenizer(dataset[:, 0])
eng_vocab_size = len(eng_tokenizer.word_index) + 1
eng_length = max_length(dataset[:, 0])
# prepare german tokenizer
ger_tokenizer = create_tokenizer(dataset[:, 1])
ger_vocab_size = len(ger_tokenizer.word_index) + 1
ger_length = max_length(dataset[:, 1])
# prepare data
trainX = encode_sequences(ger_tokenizer, ger_length, dataset[:, 1])
testX = encode_sequences(ger_tokenizer, ger_length, dataset[:, 1])

# load model
model = load_model('model3.h5')
# test on some training sequences
print('train')
evaluate_model(model, eng_tokenizer, trainX, dataset)
# test on some test sequences
print('test')
evaluate_model(model, eng_tokenizer, testX, dataset)

text = ["""3/4 cup milk

2 tablespoons white vinegar

1 cup all-purpose flour

1/2 teaspoon baking soda

2 tablespoons white sugar

1/2 teaspoon salt

1 teaspoon baking powder
legg

2 tablespoons butter, melted

cooking spray

Add all ingredients to list
Combine milk with vinegar in a medium bowl and set aside for 5 minutes
to'sour'

) Combine flour, sugar, baking powder, baking soda, and salt in a large
mixing bowl. Whisk egg and butter into soured milk. Pour the flour
mivture into the wet ingredients and whisk untillumps are gone,

Heat alarge skillet over medium heat, and coat with cooking spray, Pour
1/4 cupfuls of batter onto the skillet, and cook until bubbles appear on the
surface, Flip with a spatula, and cook until browned on the other sid,
"""]

text = encode_sequences(ger_tokenizer, ger_length, text)

print(predict_sequence(model, eng_tokenizer, text))