from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
#    path('users/',          views.UserList.as_view()),
#    path('users/<int:pk>/', views.UserDetail.as_view()),

    path('publication/',                views.PublicationRecent.as_view()),
    path('publication/top/',            views.PublicationTop.as_view()),
    path('publication/<int:pk>/',       views.PublicationDetail.as_view()),

    path('publication/vote/',           views.PublicationVoteList.as_view()),
    path('publication/vote/<int:pk>/',  views.PublicationVoteDetail.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)