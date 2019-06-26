
import math
import nltk 
from nltk import ngrams
from nltk.corpus import wordnet 
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize
import csv


def array_to_string(x):
    new=""
    for s in x:
        new += s
        new +=" "
    return new

def word_ngram(n,str1, str2):
    count=0
    n_grams1 = ngrams(str1.split(), n)
    for i in n_grams1:
        n_grams2 = ngrams(str2.split(), n)
        for j in n_grams2:
            if(array_to_string(i) == array_to_string(j)):
                count = count + 1
        
    return count

def char_ngram(n, str1, str2):
    count=0
    str1 = str1.replace(" ", "")
    str2 = str2.replace(" ", "")
    str1_char = []
    str2_char = []
    for i in range(len(str1)):
        ch = str1[i:i+2]
        str1_char.append(ch)
    for i in range(len(str2)):
        ch = str2[i:i+2]
        str2_char.append(ch)
    for i in str1_char:
        for j in str2_char:
            if(i==j):
                count = count + 1
    return count    

lemmatizer = WordNetLemmatizer()

def nltk_tag_to_wordnet_tag(nltk_tag):
    if(nltk_tag.startswith('J')):
        return wordnet.ADJ
    elif(nltk_tag.startswith('V')):
        return wordnet.VERB
    elif(nltk_tag.startswith('N')):
        return wordnet.NOUN
    elif(nltk_tag.startswith('R')):
        return wordnet.ADV
    else:
        return None
    
def lemmatize_sentence(sentence):
    nltk_tagged = nltk.pos_tag(nltk.word_tokenize(sentence))
    wordnet_tagged = map(lambda x: (x[0], nltk_tag_to_wordnet_tag(x[1])), nltk_tagged)
    lemmatized_sentence = []
    for word, tag in wordnet_tagged:
        if tag is None:
            lemmatized_sentence.append(word)
        else:
            lemmatized_sentence.append(lemmatizer.lemmatize(word, tag))
    return " ".join(lemmatized_sentence)


str1 = "I am going to watch movie"
str2 = "I am going to cinema hall"

str1_l = lemmatize_sentence(str1)
str1_tt = sent_tokenize(str1)
str2_l = lemmatize_sentence(str2)
str2_tt = sent_tokenize(str2)
str1_t = ' '.join(str1_tt)
str2_t = ' '.join(str2_tt)
feature_1 = min(len(str1), len(str2))
feature_2 = max(len(str1), len(str2))
e=word_ngram(1,str1_l, str2_t)
f=word_ngram(1,str1_l, str2)
g=word_ngram(1,str1, str2_t)
h=word_ngram(1,str1, str2)
feature_3 = min(e, f, g, h)
feature_4 = max(e, f, g, h)
feature_5 = (e + f + g + h) / 4
if((e*f*g + e*f*h + e*g*h + f*g*h) == 0):
    feature_6 = 0
else:
    feature_6 = e*f*g*h / (e*f*g + e*f*h + e*g*h + f*g*h)

e=word_ngram(2,str1_l, str2_t)
f=word_ngram(2,str1_l, str2)
g=word_ngram(2,str1, str2_t)
h=word_ngram(2,str1, str2)
feature_7 = min(e, f, g, h)
feature_8 = max(e, f, g, h)
feature_9 = (e + f + g + h) / 4
if((e*f*g + e*f*h + e*g*h + f*g*h) == 0):
    feature_10 = 0
else:
    feature_10 = e*f*g*h / (e*f*g + e*f*h + e*g*h + f*g*h)


print('Input first Statement : I am going to watch movie')
print('Input second Statement : I am going to cinema hall\n\nWord n-gram features\n')

print('Word 1-gram Overlap                            Word 2-gram Overlap')
print(str(feature_3) + '                                                       ' + str(feature_7))
print(str(feature_4) + '                                                       ' + str(feature_8))
print(str(feature_5) + '                                                     ' + str(feature_9))
print(str(feature_6) + '                                        ' + str(feature_10)+'\n')






str1_l = lemmatize_sentence(str1)
str1_tt = sent_tokenize(str1)
str2_l = lemmatize_sentence(str2)
str2_tt = sent_tokenize(str2)
str1_t = ' '.join(str1_tt)
str2_t = ' '.join(str2_tt)
e=word_ngram(3,str1_l, str2_t)
f=word_ngram(3,str1_l, str2)
g=word_ngram(3,str1, str2_t)
h=word_ngram(3,str1, str2)
feature_3 = min(e, f, g, h)
feature_4 = max(e, f, g, h)
feature_5 = (e + f + g + h) / 4
if((e*f*g + e*f*h + e*g*h + f*g*h) == 0):
    feature_6 = 0
else:
    feature_6 = e*f*g*h / (e*f*g + e*f*h + e*g*h + f*g*h)

e=word_ngram(4,str1_l, str2_t)
f=word_ngram(4,str1_l, str2)
g=word_ngram(4,str1, str2_t)
h=word_ngram(4,str1, str2)
feature_7 = min(e, f, g, h)
feature_8 = max(e, f, g, h)
feature_9 = (e + f + g + h) / 4
if((e*f*g + e*f*h + e*g*h + f*g*h) == 0):
    feature_10 = 0
else:
    feature_10 = e*f*g*h / (e*f*g + e*f*h + e*g*h + f*g*h)




print('Word 3-gram Overlap                            Word 4-gram Overlap')
print(str(feature_3) + '                                                       ' + str(feature_7))
print(str(feature_4) + '                                                       ' + str(feature_8))
print(str(feature_5) + '                                                     ' + str(feature_9))
print(str(feature_6) + '                                                       ' + str(feature_10))

























#print(feature_1/feature_2)
#print(feature_1 - feature_2)


