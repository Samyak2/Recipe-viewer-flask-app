import ijson
import nltk
from nltk import sent_tokenize
from nltk.tag import pos_tag, map_tag, StanfordPOSTagger
import pickle
from nltk.classify import MaxentClassifier
from ingredient_parser.en import parse as ingparse
nltk.data.path.append('./nltk_data/')
# train = False

def get_features(text):
    words = []
    # Same steps to start as before
    sentences = nltk.sent_tokenize(text)
    for sentence in sentences:
        words = words + nltk.word_tokenize(sentence)

    # part of speech tag each of the words
    pos = pos_tag(words)
    # Sometimes it's helpful to simplify the tags NLTK returns by default.
    # I saw an increase in accuracy if I did this, but you may not
    # depending on the application.
    pos = [map_tag('en-ptb', 'universal', tag) for word, tag in pos]
    # Then, convert the words to lowercase like before
    words = [i.lower() for i in words]
    # Grab the trigrams
    trigrams = nltk.trigrams(words)
    # We need to concatinate the trigrams into a single string to process
    trigrams = ["%s/%s/%s" % (i[0], i[1], i[2]) for i in trigrams]

    bigrams = nltk.bigrams(words)
    bigrams = ["%s/%s" % (i[0], i[1]) for i in bigrams]

    # Get our final dict rolling
    features = words + trigrams + bigrams + pos
    # get our feature dict rolling
    features = dict([(i, True) for i in features])
    return features

import time
def classify_and_extract(i, output=[], train=False, lines=300):
    output = []
    start = time.time()
    if train:
        count = 0
        json_file_name = "recipes_raw_nosource_fn.json"
        training = {"steps": [], "ingredients": []}
        with open(json_file_name, 'rb') as input_file:
            for prefix, event, value in ijson.parse(input_file):
                if event == "string" and "instructions" in prefix:
                    training["steps"] += sent_tokenize(value)
                if event == "string" and "ingredients.item" in prefix:
                    training["ingredients"] += [value]
                count+=1
                if(count > lines):
                    break
            # ingredients = ijson.items(input_file, "item")
            # for i in ingredients:
            #     print(i)
            #     count+=1
            #     if(count>20):
            #         break
        # print(training)
        training["steps"] += ["Season with sugar basil fennel seeds Italian seasoning 1 tablespoon salt pepper and 2 tablespoons parsley"]
        # Set up a list that will contain all of our tagged examples,
        # which we will pass into the classifier at the end.
        training_set = []
        for key, val in training.items():
            for i in val:
                # Set up a list we can use for all of our features,
                # which are just individual words in this case.
                feats = get_features(i)
                # Before we can tokenize words, we need to break the
                # text out into sentences.
                # sentences = nltk.sent_tokenize(i)
                # for sentence in sentences:
                    # feats = feats + nltk.word_tokenize(sentence)
                # For this example, it's a good idea to normalize for case.
                # You may or may not need to do this.
                # feats = [i.lower() for i in feats]
                # Each feature needs a value. A typical use for a case like this
                # is to use True or 1, though you can use almost any value for
                # a more complicated application or analysis.
                # feats = dict([(i, True) for i in feats])
                # NLTK expects you to feed a classifier a list of tuples
                # where each tuple is (features, tag).
                training_set.append((feats, key))
        # for value in training_set:
        #     # for data, key in value:
        #     print(value[1])
        #     print(value[0])
        #     print("-----")

    # Train up our classifier

    # data = {'11/2 teaspoons salt': True}
    # print("Enter a string")
    # i = input()
    data = i#['11/2 teaspoons salt', "1 tablespoon olive oil", "3 carrots, peeled and diced", "half of an onion, diced", "3 cloves garlic, minced", "8-10 cups chicken broth"]
    inp = []
    for sent in data:
        # inp.append((get_features(i), True))
        # inp[get_features(i)] = True
        inp.append(get_features(sent))
    # print("Inp", inp)
    if train:
        classifier = MaxentClassifier.train(training_set)
        outfile = open('my_pickle.pickle', 'wb')
        pickle.dump(classifier, outfile)
        outfile.close()
    else:
        outfile = open('my_pickle.pickle', 'rb')
        classifier = pickle.load(outfile)
        outfile.close()


    import os
    home = os.path.dirname(os.path.abspath(__file__))
    _path_to_model = home + '/stanford-postagger/models/english-bidirectional-distsim.tagger'
    _path_to_jar = home + '/stanford-postagger/stanford-postagger.jar'
    # os.environ['STANFORD_PARSER'] = _path_to_jar
    # os.environ['STANFORD_MODELS'] = _path_to_jar
    st = StanfordPOSTagger(_path_to_model, path_to_jar=_path_to_jar)



    outs = [] 
    for i in inp:
        outs.append(classifier.classify(i))
    # print("Outs", outs)
    # output = []
    counter = 0
    # print("Input Data", data)
    for out in outs:
        if out == "ingredients":
            output.append([out, ingparse(data[counter], expanded=True)])

        else:
            sentences = nltk.sent_tokenize(data[counter].lower())
            # words = nltk.word_tokenize("They " + i.lower())[1:]
            words = []
            for sentence in sentences:
                sentence = "They " + sentence 
                words = words + nltk.word_tokenize(sentence)
            # pos = pos_tag(words)
            pos = st.tag(words)
            # st = StanfordPOSTagger("stanford-postagger/stanford-postagger.jar")
            # st.tag(words)
            # pos = [(word, map_tag('en-ptb', 'universal', tag)) for word, tag in pos]
            # words = [word for word, tag in pos if "VB" in tag]
            force_tags = dict()#{'bake': 'VB'}
            new_tagged_words = [(word, force_tags.get(word, tag)) for word, tag in pos]
            blacklist = ["is", "are"]
            words = [word for word,tag in new_tagged_words if "VB" in tag and word not in blacklist]
            # print(new_tagged_words)
            # print(words)
            output.append((out, words, data[counter]))
        counter+=1
    print("--------{} seconds-------".format(time.time()-start))
    return output

if __name__ == "__main__":
    # classify_and_extract("", train=True, lines=1000)
    # print(classify_and_extract("Bring a large pot of lightly salted water to a boil. Cook lasagna noodles in boiling water for 8 to 10 minutes. Drain noodles, and rinse with cold water. In a mixing bowl, combine ricotta cheese with egg, remaining parsley, and 1/2 teaspoon salt."))
    print(classify_and_extract(["2 cloves garlic, crushed", "3/4 pound mozzarella cheese, sliced", "12 lasagna noodles","Bring a large pot of lightly salted water to a boil"]))
    # print(classify_and_extract("3/4 pound mozzarella cheese, sliced"))
    # print(classify_and_extract("12 lasagna noodles"))