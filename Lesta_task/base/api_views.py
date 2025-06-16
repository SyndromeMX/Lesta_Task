from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from collections import Counter
import math
import string

from .models import Collection, Document
from .serializers import CollectionSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import WordStatSerializer, HuffmanResponseSerializer



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def collection_list(request):
    collections = Collection.objects.filter(user=request.user)
    serializer = CollectionSerializer(collections, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def collection_detail(request, collection_id):
    try:
        collection = Collection.objects.get(id=collection_id, user=request.user)
    except Collection.DoesNotExist:
        return Response({'error': 'Коллекция не найдена'}, status=404)

    documents = collection.documents.all()
    doc_ids = [doc.id for doc in documents]
    return Response({'collection_id': collection.id, 'document_ids': doc_ids})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def collection_add_doc(request, collection_id, document_id):
    try:
        collection = Collection.objects.get(id=collection_id, user=request.user)
        document = Document.objects.get(id=document_id, user=request.user)
    except (Collection.DoesNotExist, Document.DoesNotExist):
        return Response({'error': 'Документ или коллекция не найдены'}, status=404)

    collection.documents.add(document)
    return Response({'success': True})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def collection_remove_doc(request, collection_id, document_id):
    try:
        collection = Collection.objects.get(id=collection_id, user=request.user)
        document = Document.objects.get(id=document_id, user=request.user)
    except (Collection.DoesNotExist, Document.DoesNotExist):
        return Response({'error': 'Документ или коллекция не найдены'}, status=404)

    collection.documents.remove(document)
    return Response({'success': True})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def collection_statistics(request, collection_id):
    try:
        collection = Collection.objects.get(id=collection_id, user=request.user)
    except Collection.DoesNotExist:
        return Response({'error': 'Коллекция не найдена'}, status=404)

    all_words = []
    for doc in collection.documents.all():
        try:
            text = doc.file.read().decode('utf-8').lower()
            translator = str.maketrans('', '', string.punctuation)
            words = text.translate(translator).split()
            all_words.extend(words)
        except Exception:
            continue

    word_count = len(all_words)
    if word_count == 0:
        return Response({'error': 'Невозможно построить статистику'})

    tf = Counter(all_words)
    result = []

    for word, count in tf.most_common(50):
        word_tf = count / word_count
        word_idf = math.log(word_count / count)
        result.append({
            'word': word,
            'tf': round(word_tf, 6),
            'idf': round(word_idf, 6),
            'count': count
        })

    return Response(result)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def document_list(request):
    documents = Document.objects.filter(user=request.user)
    data = [{'id': doc.id, 'name': doc.file.name} for doc in documents]
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def document_content(request, document_id):
    try:
        document = Document.objects.get(id=document_id, user=request.user)
        content = document.file.read().decode('utf-8')
        return Response({'content': content})
    except Document.DoesNotExist:
        return Response({'error': 'Документ не найден'}, status=404)
    except Exception:
        return Response({'error': 'Ошибка чтения файла'}, status=500)


@swagger_auto_schema(
    method='get',
    operation_description="Получить TF/IDF статистику по документу",
    responses={200: WordStatSerializer(many=True)},
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def document_statistics(request, document_id):
    try:
        document = Document.objects.get(id=document_id, user=request.user)
        text = document.file.read().decode('utf-8').lower()
    except Document.DoesNotExist:
        return Response({'error': 'Документ не найден'}, status=404)
    except Exception:
        return Response({'error': 'Ошибка чтения файла'}, status=500)

    translator = str.maketrans('', '', string.punctuation)
    words = text.translate(translator).split()
    word_count = len(words)
    tf = Counter(words)
    result = []

    for word, count in tf.most_common(50):
        word_tf = count / word_count
        word_idf = math.log(word_count / count)
        result.append({
            'word': word,
            'tf': round(word_tf, 6),
            'idf': round(word_idf, 6),
            'count': count
        })

    return Response(result)


# 📦 Хаффман-кодирование
class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):  # Для heapq
        return self.freq < other.freq


def build_huffman_tree(text):
    freq = Counter(text)
    heap = [Node(char, freq) for char, freq in freq.items()]
    import heapq
    heapq.heapify(heap)

    while len(heap) > 1:
        a = heapq.heappop(heap)
        b = heapq.heappop(heap)
        parent = Node(None, a.freq + b.freq)
        parent.left = a
        parent.right = b
        heapq.heappush(heap, parent)

    return heap[0] if heap else None


def generate_codes(node, prefix="", codebook=None):
    if codebook is None:
        codebook = {}

    if node:
        if node.char is not None:
            codebook[node.char] = prefix
        generate_codes(node.left, prefix + "0", codebook)
        generate_codes(node.right, prefix + "1", codebook)

    return codebook


@swagger_auto_schema(
    method='get',
    operation_description="Получить закодированное содержимое документа (код Хаффмана)",
    responses={200: HuffmanResponseSerializer},
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def document_huffman(request, document_id):
    try:
        document = Document.objects.get(id=document_id, user=request.user)
        text = document.file.read().decode('utf-8')
    except Document.DoesNotExist:
        return Response({'error': 'Документ не найден'}, status=404)
    except Exception:
        return Response({'error': 'Ошибка чтения файла'}, status=500)

    tree = build_huffman_tree(text)
    codebook = generate_codes(tree)
    encoded = ''.join(codebook[char] for char in text)

    return Response({
        'encoded': encoded,
        'codebook': codebook,
    })
