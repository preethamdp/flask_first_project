from nltk import RegexpParser
from nltk import pos_tag
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.chunk import *
from nltk.chunk.util import *
from nltk import Tree
def ie_preprocess(document):
    sentences = sent_tokenize(document)
    sentences = [word_tokenize(sent) for sent in sentences]
    sentences = [pos_tag(sent) for sent in sentences]
    return sentences
def convert_to_noun(sen):
    sen = ie_preprocess(sen)
    grammar = r"""
    NP: {<DT|PP\$>?<JJ>*<NN>}   # chunk determiner/possessive, adjectives and noun
        {<NNP>+}                # chunk sequences of proper nouns
    """
    cp = RegexpParser(grammar)
    res=cp.parse(sen[0])
    print(res)
    ROOT = 'ROOT'
    tree = res
    output = []
    def getNodes(parent):
        for node in parent:
            if type(node) is Tree:
                print ("Label:", node.label())
                print ("Leaves:", node.leaves())
                if node.leaves()[0][1] in ("NN","JJ"):
                    if node.leaves()[0][0] not in output:
                        output.append(node.leaves()[0][0])
                    print(node.leaves()[0][0])

                getNodes(node)
            else:
                print ("Word:", node)
                if node[1] in ("NN","JJ"):
                    if node[0] not in output:
                        output.append(node[0])

    getNodes(tree)
    print(output)
    return " ".join(output)