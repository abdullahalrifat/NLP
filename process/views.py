from django.shortcuts import render

# Create your views here.
from rest_framework import generics, views
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response


class Convert(views.APIView):
    parser_classes = (FileUploadParser,)

    def put(self, request, filename, format=None):
        file_obj = request.data['file']
        # ...
        # do some stuff with uploaded file
        # ...
        return Response(status=204)