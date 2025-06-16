import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from django.shortcuts import render
from .models import FileMetric
from .forms import DocumentForm
from django.core.files.storage import FileSystemStorage
from collections import Counter
import math
import os
import string
import base64
from io import BytesIO
from django.http import JsonResponse
import time
from django.db.models import Avg, Max, Min
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import UserRegisterForm, PasswordChangeCustomForm



def home(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']

            # Проверка на .txt
            if not uploaded_file.name.endswith('.txt'):
                FileMetric.objects.create(
                    filename=uploaded_file.name,
                    file_size=uploaded_file.size,
                    processed=False,
                    error_count=1,
                )
                return render(request, 'base/home.html', {
                    'form': form,
                    'error': 'Ошибка: можно загружать только .txt файлы.'
                })

            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)
            file_path = fs.path(filename)

            start_time = time.time()

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read().lower()
            except Exception as e:
                FileMetric.objects.create(
                    filename=uploaded_file.name,
                    file_size=uploaded_file.size,
                    processed=False,
                    error_count=1,
                )
                return render(request, 'base/home.html', {
                    'form': form,
                    'error': 'Ошибка при чтении файла.'
                })
            finally:
                os.remove(file_path)

            processing_duration = round(time.time() - start_time, 3)

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

            # График TF
            plt.figure(figsize=(10, 6))
            plt.bar(top_words, tf_values, color='skyblue')
            plt.xlabel('Слова')
            plt.ylabel('TF (Частота термина)')
            plt.title('Топ-10 слов по TF')
            plt.xticks(rotation=45)
            tf_graph = get_graph()
            plt.close()

            # График IDF
            plt.figure(figsize=(10, 6))
            plt.bar(top_words, idf_values, color='lightgreen')
            plt.xlabel('Слова')
            plt.ylabel('IDF (Обратная частота документа)')
            plt.title('Топ-10 слов по IDF')
            plt.xticks(rotation=45)
            idf_graph = get_graph()
            plt.close()

            # График количества
            plt.figure(figsize=(10, 6))
            plt.bar(top_words, count_values, color='salmon')
            plt.xlabel('Слова')
            plt.ylabel('Количество упоминаний')
            plt.title('Топ-10 слов по количеству упоминаний')
            plt.xticks(rotation=45)
            count_graph = get_graph()
            plt.close()

            FileMetric.objects.create(
                filename=uploaded_file.name,
                file_size=uploaded_file.size,
                processed=True,
                error_count=0,
                processing_time=processing_duration
            )

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
    graph = base64.b64encode(image_png).decode('utf-8')
    buffer.close()
    return graph


def status_view(request):
    return JsonResponse({"status": "OK"})


def metrics_view(request):
    metrics = FileMetric.objects.filter(processed=True, error_count=0)
    count = metrics.count()
    min_time = metrics.aggregate(Min('processing_time'))['processing_time__min']
    max_time = metrics.aggregate(Max('processing_time'))['processing_time__max']
    avg_time = metrics.aggregate(Avg('processing_time'))['processing_time__avg']
    latest = metrics.order_by('-uploaded_at').first()

    return JsonResponse({
        "files_processed": count,
        "min_time_processed": round(min_time, 3) if min_time else None,
        "avg_time_processed": round(avg_time, 3) if avg_time else None,
        "max_time_processed": round(max_time, 3) if max_time else None,
        "latest_file_processed_timestamp": latest.uploaded_at.timestamp() if latest else None
    })


def version_view(request):
    return JsonResponse({
        "version": os.getenv("APP_VERSION", "unknown")
    })


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'base/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'base/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeCustomForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PasswordChangeCustomForm(user=request.user)
    return render(request, 'base/change_password.html', {'form': form})
