from rest_framework import serializers


class TextSerializer(serializers.Serializer):
    Text = serializers.CharField(max_length=250)
