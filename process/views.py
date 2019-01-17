from django.shortcuts import render

# Create your views here.
from rest_framework import generics, views
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework import views, status

from process.serializers import TextSerializer

import warnings
import nltk
import numpy as np
import random
import string # to process standard python strings


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class Bot(views.APIView):

    def get(self, request, version, format=None):
        text = request.GET['text']
        # text = response(text)

        user_response = text.lower()
        if user_response != 'bye':
            if user_response == 'thanks' or user_response == 'thank you':
                flag = False
                text = "ROBO: You are welcome.."
            else:
                if greeting(user_response) != None:
                    text = "ROBO: " + greeting(user_response)
                else:
                    # print("ROBO: ", end="")
                    text = response(user_response)
                    sent_tokens.remove(user_response)
        else:
            flag = False
            text = "ROBO: Bye! take care.."
        # serializer = TextSerializer(text, many=True)
        return Response(text, status=status.HTTP_201_CREATED)

    def post(self, request, version, format=None):
        return Response(status=status.HTTP_400_BAD_REQUEST)

# coding: utf-8

# # Meet Robo: your friend


warnings.filterwarnings("ignore")

# nltk.download() # for downloading packages


f = open('/mnt/Work/NLP/process/chatbot.txt','r',errors = 'ignore')
raw = f.read()
raw = raw.lower()  # converts to lowercase
nltk.download('punkt')  # first-time use only
nltk.download('wordnet')  # first-time use only
sent_tokens = nltk.sent_tokenize(raw)  # converts to list of sentences
word_tokens = nltk.word_tokenize(raw)  # converts to list of words


sent_tokens[:2]


word_tokens[:5]


lemmer = nltk.stem.WordNetLemmatizer()


def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]


# Checking for greetings
def greeting(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


# Generating response
def response(user_response):
    robo_response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response


flag=True
print("ROBO: My name is Robo. I will answer your queries about Chatbots. If you want to exit, type Bye!")
