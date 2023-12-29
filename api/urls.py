from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
#    path('users/',          views.UserList.as_view()),
#    path('users/<int:pk>/', views.UserDetail.as_view()),

    path('publications/',           views.PublicationRecent.as_view()),
    path('publications/top/',       views.PublicationTop.as_view()),
#    path('publications/<int:pk>/',  views.PublicationDetail.as_view()),

    path('votes/',                  views.PublicationVoteList.as_view()),
    path('votes/<int:pk>/',         views.PublicationVoteDetail.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)