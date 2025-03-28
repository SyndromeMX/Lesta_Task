import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
from django.shortcuts import render, redirect
from .models import Document
from .forms import DocumentForm
from django.core.files.storage import FileSystemStorage
from collections import Counter
import math
import os
import string
import base64
from io import BytesIO

def home(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)
            
            file_path = fs.path(filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read().lower()
            
            os.remove(file_path)
            
            translator = str.maketrans('', '', string.punctuation)
            words = text.translate(translator).split()
            word_count = len(words)
            tf = Counter(words)
            
            word_stats = []
            for word, count in tf.most_common(50):  
                word_tf = count / word_count
                word_idf = math.log(word_count / count)
                word_stats.append({
                    'word': word,
                    'tf': round(word_tf, 6),
                    'idf': round(word_idf, 6),
                    'count': count
                })
            
            word_stats_sorted = sorted(word_stats, key=lambda x: x['idf'], reverse=True)
            
            top_words = [word['word'] for word in word_stats_sorted[:10]]
            tf_values = [word['tf'] for word in word_stats_sorted[:10]]
            idf_values = [word['idf'] for word in word_stats_sorted[:10]]
            count_values = [word['count'] for word in word_stats_sorted[:10]]
            
            plt.figure(figsize=(10, 6))
            plt.bar(top_words, tf_values, color='skyblue')
            plt.xlabel('Слова')
            plt.ylabel('TF (Частота термина)')
            plt.title('Топ-10 слов по TF (Частоте термина)')
            plt.xticks(rotation=45)
            tf_graph = get_graph()
            plt.close()
            
            plt.figure(figsize=(10, 6))
            plt.bar(top_words, idf_values, color='lightgreen')
            plt.xlabel('Слова')
            plt.ylabel('IDF (Обратная частота документа)')
            plt.title('Топ-10 слов по IDF (Обратной частоте документа)')
            plt.xticks(rotation=45)
            idf_graph = get_graph()
            plt.close()
            
            plt.figure(figsize=(10, 6))
            plt.bar(top_words, count_values, color='salmon')
            plt.xlabel('Слова')
            plt.ylabel('Количество упоминаний')
            plt.title('Топ-10 слов по количеству упоминаний')
            plt.xticks(rotation=45)
            count_graph = get_graph()
            plt.close()
            
            return render(request, 'base/result.html', {
                'words': word_stats_sorted,
                'tf_graph': tf_graph,
                'idf_graph': idf_graph,
                'count_graph': count_graph
            })
    else:
        form = DocumentForm()
    return render(request, 'base/home.html', {'form': form})

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph