import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy
import tflearn
import tensorflow
import random
import json
import pickle
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
import urllib.request
from bs4 import BeautifulSoup
import json
import re
#small_talk_ai_bot
with open("intents.json") as file:
    data = json.load(file)
try:
    with open("data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
except:
    words = []
    labels = []
    docs_x = []
    docs_y = []
    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])
        if intent["tag"] not in labels:
            labels.append(intent["tag"])
    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))
    labels = sorted(labels)
    training = []
    output = []
    out_empty = [0 for _ in range(len(labels))]
    for x, doc in enumerate(docs_x):
        bag = []
        wrds = [stemmer.stem(w.lower()) for w in doc]
        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)
        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1
        training.append(bag)
        output.append(output_row)
    training = numpy.array(training)
    output = numpy.array(output)
    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)
tensorflow.reset_default_graph()
net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)
model = tflearn.DNN(net)
try:
    print('model')
    model.load("model.tflearn")
except:
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")
def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]
    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]
    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1       
    return numpy.array(bag)
def jssate(search,search_keyword):
    output = {}
    try:
        temp_file = open("retrived_data.json","r")
        json_data = json.load(temp_file)
        temp_file.close()
        for each in json_data:
            if search_keyword.lower() in each.lower():
                output[each] = json_data[each] 
        if len(output)==0:
            raise Exception()
    except:
        links = {}
        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        headers={'User-Agent':user_agent,} 
        url = 'https://jssateb.ac.in/?s='
        request=urllib.request.Request(url+search,None,headers) 
        response = urllib.request.urlopen(request)
        data = response.read()
        soup = BeautifulSoup(data,'lxml')
        a_tag = soup.find_all("div",class_='full tabpublist')
        for i in range(0,len(a_tag)):
            if search_keyword.lower() in a_tag[i].text.lower():
                links[a_tag[i].a.text] = (a_tag[i].a['href'],a_tag[i].select('p')[1].get_text(strip=True))
        f = open("retrived_data.json","r")
        output.update(links)
        try:
            links.update(json.load(f))
        except:
            f1 = open("retrived_data.json","w")
            f1.write(json.dumps(links))
            f1.close()
        f.close()
        f = open("retrived_data.json","w")
        f.write(json.dumps(links,indent=4))
        f.close()
    return output     
def google(search,search_keyword):
    output = {}
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers={'User-Agent':user_agent,} 
    url = 'https://www.google.com/search?q='
    request=urllib.request.Request(url+search,None,headers) #The assembled request
    response = urllib.request.urlopen(request)
    data = response.read()
    soup = BeautifulSoup(data,'lxml')
    l = (soup.find_all("div",class_="s"))
    for i in range(len(l)):
        link = (re.findall("(https://[\w\.\/\d]*)",str(l[i].text)))
        link_desc = (l[i].text[l[i].text.find(" ")+1:])
        link.append(link_desc)
        l[i] = link
    output[search_keyword] = l
    return output
#web_scarping_Ai_bot
def web_scrap(inp):
    print("inside web")
    search_keyword = inp.strip()
    search = (search_keyword.split())
    search = str('+'.join(search))
    out = jssate(search,search_keyword)
    if len(out)==0:
        return google(search,search_keyword)
    else:
        return out
#where chatting takes place
def chat(inp):
    results = model.predict([bag_of_words(inp, words)])[0]
    results_index = numpy.argmax(results)
    tag = labels[results_index]
    if results[results_index]>0.8:
        for tg in data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']
        resp = {}
        resp[inp] = random.choice(responses)
        return resp
    else:
        return web_scrap(inp)


    

