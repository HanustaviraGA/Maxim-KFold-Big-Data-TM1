# -*- coding: utf-8 -*-
"""Maxim.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Kkq0M-UcNz9nAvQGdu18CqnT89-S5-wN
"""

import string
from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np
seed = 1234
from google.colab import drive
drive.mount('/content/drive')

value=pd.read_csv('/content/drive/My Drive/UTS_BD/Maxim.csv', sep=';', encoding='utf-8')
value.content=value.content.astype(str)
value.head()

# Case - Proses konversi huruf yang ada menjadi huruf lowercase atau huruf kecil
import re
def casefolding(content):
    content = content.lower()
    content = content.strip(" ")
    content = re.sub(r'[?|$|.|!2_:")(-+,]','', content)
    return content
value['content'] = value['content'].apply(casefolding)
value.head(100)

# Tokenizing - Proses pengurutan kata
def token(content):
    nstr = content.split(' ')
    dat= []
    a = -1
    for hu in nstr:
        a = a + 1
    if hu == '':
        dat.append(a)
    p = 0
    b = 0
    for q in dat:
        b = q - p
        del nstr[b]
        p = p + 1
    return nstr
value['content'] = value['content'].apply(token)
value.head(10)

#Filtering - Proses penghilangan kata - kata yang tidak penting 
import nltk #Natural Language Toolkit
nltk.download('stopwords') # Menghapus kata kata yang tidak penting seperti yang, ia, nya, dsb
from nltk.corpus import stopwords

def stopword_removal(Neighbourhood):
    filtering = stopwords.words('indonesian','english')
    x= []
    value = []
    def myFunc(x):
        if x in filtering : 
            return False
        else:
            return True
    fit = filter(myFunc, Neighbourhood)
    for x in fit:
        value.append(x)
        return value
value['content'] = value['content'].apply(stopword_removal)
value.head()

#Steaming - Proses pengambilan kata dasar pada susunan kalimat
!pip install Sastrawi
from sklearn.pipeline import Pipeline
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

def stemming(content):
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    do = []
    for w in content:
        dt = stemmer.stem(w)
        do.append(dt)
    d_clean=[]
    d_clean= " ".join(do)
    print(d_clean)
    return d_clean
value['content'] = value['content'].apply(stemming)

value.to_csv('data_clean.csv',index=False)
value_clean = pd.read_csv('data_clean.csv', encoding='latin1')
value_clean.head()

value_clean = value_clean.astype({'Kategori': 'category'})
value_clean = value_clean.astype({'content': 'string'})
value_clean.dtypes

#Proses TF-IDF
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

tvec = CountVectorizer()
X_cVec = tvec.fit_transform(value_clean['content'].values.astype('U'))
print(X_cVec)
h_tfidf = TfidfTransformer()
x_tfidf = h_tfidf.fit_transform(X_cVec)
print(x_tfidf)
X = value_clean.content
Y = value_clean.Kategori

#Proses eksekusi algoritma KFold
from sklearn.model_selection import train_test_split

from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

kf = KFold(n_splits=10)
X_array = x_tfidf.toarray()
def cross_val(estimator):
  acc = []
  pcs = []
  rec = []

  for train_index, test_index in kf.split(X_array, Y):
    X_train, X_test = X_array[train_index], X_array[test_index]
    y_train, y_test = Y[train_index], Y[test_index]

    model = estimator.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    acc.append(accuracy_score(y_test, y_pred))
    pcs.append(precision_score(y_test, y_pred, average='macro', zero_division=0))
    rec.append(recall_score(y_test, y_pred, average='macro', zero_division=0))
    rec.append(f1_score(y_test, y_pred, average='macro', zero_division=0))

    print(classification_report(y_test, y_pred, zero_division=0))
    print(f'Confusion Matrix:\n {confusion_matrix(y_test, y_pred)}')
    print('=================================================\n')

  print(f'Average Akurasi: {np.mean(acc)}')
  print(f'Average Presisi: {np.mean(pcs)}')
  print(f'Average Recall: {np.mean(rec)}')
  print(f'Average F1-Score: {np.mean(rec)}')

from sklearn.naive_bayes import MultinomialNB
nb = MultinomialNB()
cross_val(nb)