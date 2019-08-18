# from pickle import load
from numpy import array, argmax
# from numpy import argmax
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical, plot_model
from keras.layers import Input, Embedding, LSTM, RepeatVector, TimeDistributed, Dense
from keras.models import Model, load_model
from keras.callbacks import ModelCheckpoint
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
print(ingredient_tokenizer.word_index)

step_tokenizer = create_tokenizer(data[:, 2])
step_vocab_size = len(step_tokenizer.word_index) + 1
step_max_len = max_length(data[:, 2])
print("step Vocabulary Size : %d" % step_vocab_size)
print("step max length : %d" % step_max_len)
print(step_tokenizer.word_index)


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
# print(trainY1)
trainY2 = encode_sequences(step_tokenizer, step_max_len, data[:, 2])
trainY2 = encode_output(trainY2, step_vocab_size)

def define_model(text_vocab, ing_vocab, step_vocab, text_timesteps, ing_timesteps, step_timesteps, n_units):
    inputs = Input(shape = (text_timesteps,))

    ingredient_model = Embedding(text_vocab, n_units, input_length=text_timesteps, mask_zero=True)(inputs)
    ingredient_model = LSTM(n_units)(ingredient_model)
    ingredient_model = RepeatVector(ing_timesteps)(ingredient_model)
    ingredient_model = LSTM(n_units, return_sequences=True)(ingredient_model)
    ingredient_model = TimeDistributed(Dense(ing_vocab, activation="softmax"), name="ingredient_output")(ingredient_model)

    step_model = Embedding(text_vocab, n_units, input_length=text_timesteps, mask_zero=True)(inputs)
    step_model = LSTM(n_units)(step_model)
    step_model = RepeatVector(step_timesteps)(step_model)
    step_model = LSTM(n_units, return_sequences=True)(step_model)
    step_model = TimeDistributed(Dense(step_vocab, activation="softmax"), name="step_output")(step_model)

    model = Model(inputs=inputs, outputs=[ingredient_model, step_model], name="text_cleaner")
    return model

# model = define_model(text_vocab_size, ingredient_vocab_size, step_vocab_size, text_max_len, ingredient_max_len, step_max_len, 256)
# model.compile(optimizer='adam', loss='categorical_crossentropy')
# print(model.summary())
# plot_model(model, to_file='model.png', show_shapes=True)

# # fit model
# filename = 'model.h5'
# checkpoint = ModelCheckpoint(filename, monitor='loss', verbose=2, save_best_only=False, mode='min')
# model.fit(trainX, {"ingredient_output": trainY1, "step_output": trainY2}, epochs=25, callbacks=[checkpoint], verbose=2)

model = load_model('model.h5')
# map an integer to a word
def word_for_id(integer, tokenizer):
	for word, index in tokenizer.word_index.items():
		if index == integer:
			return word
	return None
# generate target given source sequence
# generate target given source sequence
def predict_sequence(model, ing_tokenizer, step_tokenizer, source):
    ing_prediction, step_prediction = model.predict(source, verbose=2)
    # print(ing_prediction, step_prediction)

    integers = [argmax(vector) for vector in ing_prediction]
    print(integers)
    target = list()
    for i in integers:
        word = word_for_id(i, ing_tokenizer)
        if word is None:
            break
        target.append(word)
    ing_output = ' '.join(target)

    integers = [argmax(vector) for vector in step_prediction]
    print(integers)
    target = list()
    for i in integers:
        word = word_for_id(i, step_tokenizer)
        if word is None:
            break
        target.append(word)
    step_output = ' '.join(target)

    return (ing_output, step_output)

# generate target given source sequence
def predict_sequence_0(model, tokenizer, source):
	prediction = model.predict(source, verbose=0)[0]
	integers = [argmax(vector) for vector in prediction]
	target = list()
	for i in integers:
		word = word_for_id(i, tokenizer)
		if word is None:
			break
		target.append(word)
	return ' '.join(target)

def prediction(model, ing_tokenizer, step_tokenizer, sources):
    for i, source in enumerate(sources):
        # translate encoded source text
        source = source.reshape((1, source.shape[0]))
        ing_output, step_output = predict_sequence(model, ing_tokenizer, step_tokenizer, source)
        print(ing_output, step_output)
        print(predict_sequence_0(model, ing_tokenizer, source))
        # ing_prediction, step_prediction = model.predict(source, verbose=2)
        # print(ing_prediction, step_prediction)

        # integers = [argmax(vector) for vector in ing_prediction]
        # target = list()
        # for i in integers:
        #     word = word_for_id(i, ing_tokenizer)
        #     if word is None:
        #         break
        #     target.append(word)
        # print(' '.join(target))
        # ing_output = ' '.join(target)

        # integers = [argmax(vector) for vector in step_prediction]
        # target = list()
        # for i in integers:
        #     word = word_for_id(i, step_tokenizer)
        #     if word is None:
        #         break
        #     target.append(word)
        # print(' '.join(target))
        # step_output = ' '.join(target)

        # integers = [argmax(vector) for vector in source]
        # target = list()
        # for i in source:
        #     word = word_for_id(i, text_tokenizer)
        #     if word is None:
        #         break
        #     target.append(word)
        # inputs = ' '.join(target)

        # print("Ingredients:", ing_output, "Steps:", step_output)

    # return ing_output, step_output

prediction(model, ingredient_tokenizer, step_tokenizer, trainX)

text = ["""3 tablespoons white wine vinegar
Kosher salt and freshly ground black pepper
1/4 cup extra-virgin olive oil
6 ears fresh corn
2 cups red or orange grape tomatoes, halved
8 ounces fresh mozzarella, cut into small cubes
1 bunch scallions (white and green), thinly sliced

1 1/2 cups fresh basil leaves
1 Whisk together the vinegar, 2 teaspoons salt
and some pepper in a small bowl. Gradually
whisk in the oil, starting with a few drops and then
adding the rest in a steady stream, to make a
Smooth dressing.

Shear off the corn kernels with a sharp knife

over a bowl (you should have about 4 cups).
Toss in the tomatoes, mozzarella and scallions.
Pour the vinaigrette over the salad and toss to coat.
Cover and let stand for at least 15 minutes and up
to 2 hours. Before serving, tear the basil over the
salad and stir."""]

# text = encode_sequences(text_tokenizer, text_max_len, text)

# predictions = model.predict(text)[0]
# print(predictions)
# reverse_word_map = dict(map(reversed, ingredient_tokenizer.word_index.items()))

# def sequence_to_text(list_of_indices):
#     # Looking up words in dictionary
#     words = [reverse_word_map.get(letter) for letter in list_of_indices]
#     return(words)

# # Creating texts 
# my_texts = list(map(sequence_to_text, predictions))
# print(my_texts)

# print(ingredient_tokenizer.sequences_to_texts(predictions))