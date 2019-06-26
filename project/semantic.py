
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
    
            





def word_semantic_similarity(w1,w2):
	w1_syn = wordnet.synsets(w1)
	w2_syn = wordnet.synsets(w2)
	word_sim = []
	if len(w1_syn) != 0 and len(w2_syn) != 0:
		for a in w1_syn:
			for b in w2_syn:
				w1_pos = wordnet.synset(a.name()) 
				w2_pos = wordnet.synset(b.name())
				similarity = w1_pos.wup_similarity(w2_pos)	
				if similarity is not None:
					word_sim.append(similarity)	
		if(len(word_sim) is not 0):
			return max(word_sim)
		else:
			return 0
	else:
		return 0

def word_string_similarity(X, Y):
	m = len(X) 
	n = len(Y) 
	L = [[0 for k in range(n+1)] for l in range(m+1)] 
	for i in range(m+1): 
		for j in range(n+1): 
			if i == 0 or j == 0 : 
				L[i][j] = 0
			elif X[i-1] == Y[j-1]: 
				L[i][j] = L[i-1][j-1]+1
			else: 
				L[i][j] = max(L[i-1][j] , L[i][j-1])
	
	LCSuff = [[0 for k in range(n+1)] for l in range(m+1)] 
	result = 0 
	for i in range(m + 1): 
		for j in range(n + 1): 
			if (i == 0 or j == 0): 
				LCSuff[i][j] = 0
			elif (X[i-1] == Y[j-1]): 
				LCSuff[i][j] = LCSuff[i-1][j-1] + 1
				result = max(result, LCSuff[i][j]) 
			else: 
				LCSuff[i][j] = 0
	prefix = 0
	for i in range(min(m,n)):
		if(X[i] is Y[i]):
			prefix = prefix + 1
		else:
			break;
	return (L[m][n] + result + prefix) / (3 * min(len(X), len(Y)) )

def frequency(w, corpus):
	count = 0
	for a in corpus:
		if w is a:
			count += 1
	return count


def final_word_similarity(X, Y):
	return max(word_semantic_similarity(X, Y), word_string_similarity(X, Y))
	#return word_semantic_similarity(X, Y)


str1 = "he man is slicing a potato."
str2 = "A man is slicing potato"

str1_word = str1.split(' ')
str2_word = str2.split(' ')
sum = 0
for a in str1_word:
    temp = []
    for b in str2_word:
            temp.append(final_word_similarity(a, b))
    sum = sum + max(temp)
cov_str1_by_str2 = sum / len(str1_word)
sum = 0


for a in str2_word:
    temp = []
    for b in str1_word:
        temp.append(final_word_similarity(a, b))
    sum = sum + max(temp)

cov_str2_by_str1 = sum / len(str2_word)
feature_1 = min(cov_str1_by_str2, cov_str2_by_str1)
feature_2 = max(cov_str1_by_str2, cov_str2_by_str1)
feature_3 = (cov_str1_by_str2 + cov_str2_by_str1 ) / 2
feature_4 = (cov_str1_by_str2 * cov_str2_by_str1 ) / (cov_str1_by_str2 + cov_str2_by_str1 )
str1_word_freq_sum = 0

for a in str1_word:
    str1_word_freq_sum = str1_word_freq_sum + frequency(a, str1_word)

    str2_word_freq_sum = 0
for a in str2_word:
    str2_word_freq_sum = str2_word_freq_sum + frequency(a, str2_word)
    sum = 0
    
for a in str1_word:
    ic = math.log(str1_word_freq_sum / frequency(a, str1_word))
    temp = []
    for b in str2_word:
        temp.append(ic * final_word_similarity(a,b))
    sum = sum + max(temp)

weight_cov_str1_by_str2 = sum / len(str1_word)
sum = 0
for a in str2_word:
    ic = math.log(str2_word_freq_sum / frequency(a, str2_word))
    temp = []
    for b in str1_word:
        temp.append(ic * final_word_similarity(a, b))
    sum = sum + max(temp)

weight_cov_str2_by_str1 = sum / len(str2_word)
feature_5 = min(weight_cov_str2_by_str1, weight_cov_str1_by_str2)
feature_6 = max(weight_cov_str2_by_str1, weight_cov_str1_by_str2)
feature_7 = (weight_cov_str2_by_str1 + weight_cov_str1_by_str2) / 2
feature_8 = (weight_cov_str2_by_str1 * weight_cov_str1_by_str2) / (weight_cov_str2_by_str1 + weight_cov_str1_by_str2)


print(feature_1)
print(feature_2)
print(feature_3)
print(feature_4)
print(feature_5)
print(feature_6)
print(feature_7)
print(feature_8)
