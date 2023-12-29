from rest_framework import serializers
from django.contrib.auth.models import User

from publications.models import Publication, PublicationVote


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class PublicationSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='user.username')
    publish_date = serializers.ReadOnlyField()
    rating = serializers.ReadOnlyField()
    votes = serializers.ReadOnlyField()
 
    class Meta:
        model = Publication
        fields = ['id','text', 'author','publish_date','rating','votes']

class PublicationVoteSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='user.username')
#    publication = serializers.ReadOnlyField(source='publication.text')

    class Meta:
        author = serializers.ReadOnlyField(source='user.username')
        model = PublicationVote
        fields = ['id', 'publication','author', 'vote' ]
