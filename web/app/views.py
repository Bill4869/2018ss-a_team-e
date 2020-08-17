from datetime import date, datetime
from django.conf import settings
from django.shortcuts import render, redirect

from .forms import RegisterForm, TopUpForm, AnalysisForm
from .models import models, StudentCard, ICCharger, TopUpHistory
from .face_api import FaceAPI
from .text_api import TextAPI
from .similarity import Similarity


def register(request):
    if request.method == 'GET':
        return render(request, 'app/register.html', {'form': RegisterForm(),})

    elif request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if not form.is_valid():
            raise ValueError('Invalid form')

        StudentCard(
            id = form.cleaned_data['id'],
            name = form.cleaned_data['name'],
            balance = form.cleaned_data['balance'],
            icon = form.cleaned_data['icon'],
            bio = form.cleaned_data['bio']
        ).save()

        ICCharger(id = 1, last_charge_date = str(date.today())).save()

        return redirect('register')


def top_up(request):
    if request.method == 'GET':
        return render(request, 'app/top_up.html', {'form': TopUpForm(),})

    elif request.method == 'POST':
        form = TopUpForm(request.POST)
        if not form.is_valid():
            raise ValueError('Invalid form')

        card = StudentCard.objects.get(pk=form.cleaned_data['id'])
        card.balance += form.cleaned_data['top_up_money']
        card.save()

        TopUpHistory(
            student_id=card.id,
            date=datetime.now(),
            balance=card.balance,
            top_up_money=form.cleaned_data['top_up_money']
        ).save()

        return redirect('top_up')


def student_list(request):
    return render(request, 'app/students.html', {'cards': StudentCard.objects.all(),})


def student_info(request, id):
    card = StudentCard.objects.get(pk=id)
    face_api = FaceAPI(settings.BASE_DIR + card.icon.thumbnail.url)
    area = face_api.detect_face()
    face = face_api.get_face_attributes()
    icon_m = face_api.mosaic_filter(area)
    histories = TopUpHistory.objects.all().filter(student_id=id)

    return render(request, 'app/student_info.html', {'card': card, 'gender': face['gender'], 'age': face['age'], 'icon_m': icon_m, 'histories': histories})


def analysis(request):
    if request.method == 'GET':
        return render(request, 'app/analysis.html', {'form': AnalysisForm(),})

    elif request.method == 'POST':
        form = AnalysisForm(request.POST)
        if not form.is_valid():
            raise ValueError('Invalid form')
        
        cards = {'target': StudentCard.objects.get(pk=form.cleaned_data['id'])}

        similarity = Similarity()
        sim, ids = similarity.compare_all(cards['target'], StudentCard.objects.all())

        text_api = TextAPI(cards['target'].bio)
        face_api = FaceAPI(settings.BASE_DIR + cards['target'].icon.thumbnail.url)
        faces = {'target': face_api.get_face_attributes()}
        words = {}
        for key, id in ids.items():
            cards[key] = StudentCard.objects.get(pk=id)
            face_api = FaceAPI(settings.BASE_DIR + cards[key].icon.thumbnail.url)
            faces[key] = face_api.get_face_attributes()
            words[key] = text_api.get_suggest_words(cards[key].bio)

        parameter = {
            'cards': cards,
            'faces': faces,
            'words': words,
            'bio_sim_bio': sim['bio'][ids['bio']],
            'bio_sim_icon': sim['bio'][ids['icon']],
            'bio_sim_total': sim['bio'][ids['total']],
            'icon_sim_bio': sim['icon'][ids['bio']],
            'icon_sim_icon': sim['icon'][ids['icon']],
            'icon_sim_total': sim['icon'][ids['total']],
            'total_sim_bio': sim['total'][ids['bio']],
            'total_sim_icon': sim['total'][ids['icon']],
            'total_sim_total': sim['total'][ids['total']],
        }

        return render(request, 'app/result.html', parameter)
