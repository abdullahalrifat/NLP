from django.shortcuts import render

# Create your views here.
from rest_framework import generics, views
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework import views, status
from chatterbot.trainers import ChatterBotCorpusTrainer

from process.serializers import TextSerializer
import json
import sys
import warnings
import nltk
import numpy as np
import random
import string # to process standard python strings
import requests

from chatterbot import ChatBot
from django.http import JsonResponse, HttpResponse
# from chatterbot.trainers import ChatterBotCorpusTrainer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ACCESS_TOKEN ="EAADbAKIlGVIBALXHqFaTZAPQV3C4KhSJjAlzDmfQnZAeuiTmEOtuvpyHFm8NdmzAmqNdFOlZARm1J98q9JWah9sjCIS1MOqLzKELqWHZA1vtlZBrZCar3Tq1kMSpG9wHbYZBZBZBcdBdKlPP13ZBIbq7XqDOxTrB1g4AQnw8N7Y4LiLNjHCUVd80Os"

VERIFY_TOKEN = 'my_voice_is_my_password_verify_me'


chatterbot = ChatBot("NLP")

# Create a new trainer for the chatbot
trainer = ChatterBotCorpusTrainer(chatterbot)

# Train based on the english corpus
trainer.train("chatterbot.corpus.english")

# Train based on english greetings corpus
trainer.train("chatterbot.corpus.english.greetings")

# Train based on the english conversations corpus
trainer.train("chatterbot.corpus.english.conversations")


class Bot(views.APIView):

    def get(self, request, version, format=None):
        text = request.GET['text']
        # text = response(text)
        # chatbot = ChatBot('Ron Obvious')

        # Create a new trainer for the chatbot
        # trainer = ChatterBotCorpusTrainer(chatbot)

        # Train the chatbot based on the english corpus
        # trainer.train("chatterbot.corpus.english")

        # Get a response to an input statement

        response = chatterbot.get_response(text)
        response_data = response.serialize()
        # serializer = TextSerializer(text, many=True)
        return Response(response_data, status=status.HTTP_201_CREATED)

    def post(self, request, version, format=None):
        text = request.POST['text']
        response = chatterbot.get_response(text)
        response_data = response.serialize()
        # serializer = TextSerializer(text, many=True)
        return Response(response_data, status=status.HTTP_201_CREATED)


class Verify(views.APIView):

    def get(self, request, version, format=None):
        # text = request.GET['text']
        # text = response(text)
        # chatbot = ChatBot('Ron Obvious')

        # Create a new trainer for the chatbot
        # trainer = ChatterBotCorpusTrainer(chatbot)

        # Train the chatbot based on the english corpus
        # trainer.train("chatterbot.corpus.english")

        # Get a response to an input statement

        token_sent = request.GET['hub.verify_token']
        return verify_fb_token(token_sent, request)
        # serializer = TextSerializer(text, many=True)
        # return Response(response_data, status=status.HTTP_201_CREATED)

    def post(self, request, version, format=None):
        data = json.loads(self.request.body.decode('utf-8'))
        # log(data)  # you may not want to log every incoming message in production, but it's good for testing
        if data["object"] == "page":
            for entry in data.get("entry"):
                if "messaging" in entry:
                    for event in entry.get("messaging"):
                        #   print(event.get('sender'))
                        #   print(event.get('sender').get('id'))
                        #   sender_id = event.get('sender').get('id')
                        if event.get("message"):  # delivery confirmation
                            recipient_id = event.get('recipient').get('id')
                            sender_id = event.get('sender').get('id')
                            text = event.get("message")
                            response = chatterbot.get_response(text)
                            response_data = response.serialize()
                            send_message(request, sender_id, response_data)

                        if event.get("delivery"):
                            pass

                        if event.get("optin"):  # optin confirmation
                            user_ref = event.get('optin').get("user_ref")
                            send_message(user_ref,
                                         "Good to see you",
                                         category="user_ref")
                        if event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                            pass
        return request.args.text("ok")


def verify_fb_token(token_sent, request):
    if request.GET["hub.mode"] == "subscribe" and request.GET["hub.challenge"]:
        if not request.GET["hub.verify_token"] == VERIFY_TOKEN:
            return HttpResponse("Verification token mismatch", status=403)
        return HttpResponse(request.GET["hub.challenge"])

    return HttpResponse("Hello world")


def send_message(request,
                 recipient_id,
                 message_text,
                 category="id",
                 message_type="UPDATE"):

    # log("sending message to {recipient}: {text}".format(
        # recipient=recipient_id, text=message_text))

    params = {
        "access_token": ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            category: recipient_id
        },
        "message": {
            "text": message_text
        },
        "messaging_type": message_type
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params=params, headers=headers, data=data)
    log(r.text)
    if r.status_code != 200:
        log(r.status_code)


def log(message):  # simple wrapper for logging to stdout on heroku
    print(str(message))
    sys.stdout.flush()
