from django.utils.timesince import timesince
from rest_framework import serializers
from newsapp.models import Article, Journalist
from datetime import date, datetime


class ArticleSerializer(serializers.ModelSerializer):

    time_since_publication = serializers.SerializerMethodField()
    # author = JournalistSerializer()
    # author = serializers.StringRelateedField()

    class Meta:
        model = Article
        # fields = "__all__" # we want all the fields of our model
        # fields = ('title', 'description', 'body') # choosing to serialize some of the fields
        exclude = ('id',)  # We only want to exclude one field.

    def get_time_since_publication(self, object):
        publication_date = object.publication_date
        now = datetime.now()
        time_delta = timesince(publication_date, now)
        return time_delta

    def validate(self, data):
        """Checks that description and title are different"""
        if data['title'] == data['description']:
            raise serializers.ValidationError(
                "Title and description must be different from one another!")
        else:
            return data

    def validate_title(self, value):
        """Checks that the title is shorter than 60 chars"""
        if len(value) < 30:
            raise serializers.ValidationError(
                "The title must at least be 60 characters long!")
        else:
            return value

    def validate_publication_date(self, value):
        """Checks that the publication date is later than the current date."""
        if value < date.today():
            raise serializers.ValidationError(
                'The publication date must be later than today!')
        else:
            return value


class JournalistSerializer(serializers.ModelSerializer):
    articles = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='article-detail')
    # articles = ArticleSerializer(many=True, read_only=True)

    class Meta:
        model = Journalist
        fields = "__all__"

# class ArticleSerializer(serializers.Serializer):
#     """Defining the fields that the serializer must have, coming from the model."""
#     id = serializers.IntegerField(read_only=True)
#     author = serializers.CharField()
#     title = serializers.CharField()
#     description = serializers.CharField()
#     body = serializers.CharField()
#     location = serializers.CharField()
#     publication_date = serializers.DateField()
#     active = serializers.BooleanField()
#     created_at = serializers.DateTimeField(read_only=True)
#     updated_at = serializers.DateTimeField(read_only=True)

#     def create(self, validated_data):
#         print(validated_data)
#         return Article.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.author = validated_data.get('author', instance.author)
#         instance.title = validated_data.get('title', instance.title)
#         instance.description = validated_data.get('description',
#                                                   instance.description)
#         instance.body = validated_data.get('body', instance.body)
#         instance.location = validated_data.get('location', instance.location)
#         instance.publication_date = validated_data.get('publication_date',
#                                                        instance.publication_date)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
