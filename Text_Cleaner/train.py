# from pickle import load
from numpy import array
# from numpy import argmax
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
# from keras.models import load_model
# from nltk.translate.bleu_score import corpus_bleu

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
        data.append([text, ing, step])
    return data

data = load_dataset("dataset.txt")
data = array(data)
# print(data[2,1])

# fit a tokenizer
def create_tokenizer(lines):
	tokenizer = Tokenizer()
	tokenizer.fit_on_texts(lines)
	return tokenizer

# max sentence length
def max_length(lines):
	return max(len(line.split()) for line in lines)

text_tokenizer = create_tokenizer(data[:, 0])
text_vocab_size = len(text_tokenizer.word_index) + 1
text_max_len = max_length(data[:, 0])
print("Text Vocabulary Size : %d" % text_vocab_size)
print("Text max length : %d" % text_max_len)

ingredient_tokenizer = create_tokenizer(data[:, 1])
ingredient_vocab_size = len(ingredient_tokenizer.word_index) + 1
ingredient_max_len = max_length(data[:, 1])
print("ingredient Vocabulary Size : %d" % ingredient_vocab_size)
print("ingredient max length : %d" % ingredient_max_len)

step_tokenizer = create_tokenizer(data[:, 2])
step_vocab_size = len(step_tokenizer.word_index) + 1
step_max_len = max_length(data[:, 2])
print("step Vocabulary Size : %d" % step_vocab_size)
print("step max length : %d" % step_max_len)


# encode and pad sequences
def encode_sequences(tokenizer, length, lines):
	# integer encode sequences
	X = tokenizer.texts_to_sequences(lines)
	# pad sequences with 0 values
	X = pad_sequences(X, maxlen=length, padding='post')
	return X

# one hot encode target sequence
def encode_output(sequences, vocab_size):
	ylist = list()
	for sequence in sequences:
		encoded = to_categorical(sequence, num_classes=vocab_size)
		ylist.append(encoded)
	y = array(ylist)
	y = y.reshape(sequences.shape[0], sequences.shape[1], vocab_size)
	return y

trainX = encode_sequences(text_tokenizer, text_max_len, data[:, 0])
trainY1 = encode_sequences(ingredient_tokenizer, ingredient_max_len, data[:, 1])
trainY1 = encode_output(trainY1, ingredient_vocab_size)
trainY2 = encode_sequences(step_tokenizer, step_max_len, data[:, 2])
trainY2 = encode_output(trainY2, step_vocab_size)

def define_model():
    #TODO
    pass