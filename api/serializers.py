from rest_framework import serializers
from django.contrib.auth.models import User

from publications.models import Publication, PublicationVote
import traceback


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class PublicationSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='user.username')
    publish_date = serializers.ReadOnlyField()
    rating = serializers.ReadOnlyField()
    votes = serializers.ReadOnlyField()
#    vote_set = serializers.PrimaryKeyRelatedField(source='publicationvote_set', many=True, read_only=True)

    class Meta:
        model = Publication
        fields = ['id','text', 'author','publish_date','rating','votes' ]


class PublicationVoteSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='user.username')
    text = serializers.ReadOnlyField(source='publication.text')
#    publication = serializers.SlugRelatedField(
#        queryset=Publication.objects.all(),
#        slug_field = 'text',
#    )

    class Meta:
        model = PublicationVote
        fields = ['id', 'publication', 'text', 'author', 'vote' ]

    def create(self, validated_data):
        """ переопределяю поведение чтобы не создавалась оценка если такая уже есть """
        print( 'PublicationVoteSerializer.create' )
        print( validated_data ) 

        instance = PublicationVote.vote_add_or_update( 
            validated_data['publication'].id, 
            validated_data['vote'], 
            validated_data['user'].id, 
        )

        return instance

