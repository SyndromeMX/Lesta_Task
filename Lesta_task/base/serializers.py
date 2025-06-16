from rest_framework import serializers
from .models import Document, Collection


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'file', 'uploaded_at']


class CollectionSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = ['id', 'name', 'documents']


class WordStatSerializer(serializers.Serializer):
    word = serializers.CharField()
    tf = serializers.FloatField()
    idf = serializers.FloatField()
    count = serializers.IntegerField()


class HuffmanResponseSerializer(serializers.Serializer):
    encoded = serializers.CharField()
    codebook = serializers.DictField(
        child=serializers.CharField()
    )
