from django.shortcuts import render
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *

from django.db.models import Prefetch

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

from django.views.decorators.csrf import csrf_exempt
import json


def publications_listing( request, order='recent' ):
    res = { 'order' : order }

    # список пудликаций 
    object_list = Publication.objects 

    # для залогиненных пользователей подгружаю их оценки 
    if request.user.is_authenticated :
        user_id = request.user.id 
        object_list = object_list.prefetch_related(
            Prefetch("publicationvote_set", 
                     queryset=PublicationVote.objects.filter(user_id=user_id),
                     to_attr="user_vote"
                    )
        )

    # сортировка публикаций 
    match order:
       case "top":
           object_list = object_list.order_by('-rating')
           res = { 'title' : 'Cамые рейтинговые публикации' }
       case _:
           object_list = object_list.order_by('-publish_date')
           res = { 'title' : 'Последние Публикации' }


    res['object_list'] = object_list[:10]
    return render(request,  'publications/list.html', res  )



@login_required
def publication_add( request ):
    if request.POST:
        form = AddPublicationForm( request.POST, )
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user

            with transaction.atomic():
                instance.save()

            return HttpResponseRedirect( reverse( 'index',) ) 
    else:
        form = AddPublicationForm()

    res = { 'form' : form }
    return render(request,'publications/add.html',res )


def user_registration( request ):
    # Если уже авторизирован переходим на главную
    if request.user.is_authenticated :
        return HttpResponseRedirect( reverse( 'index',) ) 

    if request.POST:
        form = UserCreationForm( request.POST, )
        if form.is_valid():
            with transaction.atomic():
                user = form.save()

            # сразу логинимся после регистрации
            if user is not None:
                login(request, user)
            print( 'user', user )

            return HttpResponseRedirect( reverse( 'index',) ) 
    else:
        form = UserCreationForm()

    res = { 'form' : form }
    return render(request,'registration/user_registration.html',res )


@csrf_exempt
@login_required
def vote_add( request ):
    if request.method == 'POST':
        data = json.loads(request.body)

        # обновление оценки
        res = PublicationVote.vote_add_or_update( data['publication_id'], data['vote'], request.user.id )

        # полуление свежего рейтинга, для обновления на странице
        res.update( Publication.get_votes_rating_dict( data['publication_id']) )
        return JsonResponse(res) 

    return HttpResponseRedirect( reverse( 'index',) )


@csrf_exempt
@login_required
def vote_delete( request ):
    if request.method == 'DELETE':
        data = json.loads(request.body)

        # удаление оценки
        PublicationVote.vote_delete( data['publication_id'], request.user.id )
        res = { 'status': 'deleted' }

        # полуление свежего рейтинга, для обновления на странице
        res.update( Publication.get_votes_rating_dict( data['publication_id']) )
        return JsonResponse(res) 

    return render(request,  'publications/list.html', res  )

