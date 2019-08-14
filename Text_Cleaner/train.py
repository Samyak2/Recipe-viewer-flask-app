def load_dataset(filename):
    data = []
    f = open("dataset.txt", "r")
    content = f.read()
    content = content.split("##")[1:]
    for datapoint in content:
        
        for 