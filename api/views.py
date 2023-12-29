from rest_framework import generics, permissions

from django.contrib.auth.models import User
from publications.models import Publication, PublicationVote


from . import serializers
from .permissions import IsOwnerOrReadOnly

#class UserList(generics.ListAPIView):
#    queryset = User.objects.all()
#    serializer_class = serializers.UserSerializer

#class UserDetail(generics.RetrieveAPIView):
#    queryset = User.objects.all()
#    serializer_class = serializers.UserSerializer




class PublicationRecent(generics.ListCreateAPIView):
    queryset = Publication.objects.order_by('-publish_date')[:10]
    serializer_class = serializers.PublicationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PublicationTop(PublicationRecent):
    queryset = Publication.objects.order_by('-rating')[:10]


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PublicationDetail(generics.RetrieveAPIView):
    queryset = Publication.objects.all()
    serializer_class = serializers.PublicationSerializer
    permission_classes = [
            permissions.IsAuthenticatedOrReadOnly,
            IsOwnerOrReadOnly
        ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



class PublicationVoteList(generics.ListCreateAPIView):
    queryset = PublicationVote.objects.all()
    serializer_class = serializers.PublicationVoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PublicationVoteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PublicationVote.objects.all()
    serializer_class = serializers.PublicationVoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
