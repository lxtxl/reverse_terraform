
def save_file(file_name, sentence):
    f = open(file_name, 'w')
    f.write(sentence)
    f.close()