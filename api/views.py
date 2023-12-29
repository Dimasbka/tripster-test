from rest_framework import generics, permissions

from django.contrib.auth.models import User
from publications.models import Publication, PublicationVote


from . import serializers
from .permissions import IsOwnerOrReadOnly


class PublicationRecent(generics.ListCreateAPIView):
    name = "Просмотр списка из 10 последних публикаций"
    queryset = Publication.objects.order_by('-publish_date')[:10]
    serializer_class = serializers.PublicationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PublicationTop(PublicationRecent):
    name = "Просмотр списка из 10 самых рейтинговых"
    queryset = Publication.objects.order_by('-rating')[:10]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PublicationDetail(generics.RetrieveAPIView):
    name = "Просмотр публикации"
    queryset = Publication.objects.all()
    serializer_class = serializers.PublicationSerializer
    permission_classes = [
            permissions.IsAuthenticatedOrReadOnly,
            IsOwnerOrReadOnly
        ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



class PublicationVoteList(generics.ListCreateAPIView):
    name = "Оценки пользователя"
    serializer_class = serializers.PublicationVoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        print('PublicationVoteList perform_create',serializer)

#            PublicationVote.vote_add_or_update( data['publication_id'], data['vote'], user_id:int, return_obj=False )

        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user is not None:
            queryset = PublicationVote.objects.filter(user=user)
        else:
            queryset = PublicationVote.objects.none()
        return queryset

class PublicationVoteDetail(generics.RetrieveUpdateDestroyAPIView):
    name = "Оценка пользователя"

    queryset = PublicationVote.objects.all()
    serializer_class = serializers.PublicationVoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        print('PublicationVoteDetail perform_create',serializer)
        
        serializer.save(user=self.request.user)
