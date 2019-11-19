from rest_framework import serializers
from newsapp.models import Article
from datetime import date


class ArticleSerializer(serializers.Serializer):
    """Defining the fields that the serializer must have, coming from the model."""
    id = serializers.IntegerField(read_only=True)
    author = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    body = serializers.CharField()
    location = serializers.CharField()
    publication_date = serializers.DateField()
    active = serializers.BooleanField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        print(validated_data)
        return Article.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.author = validated_data.get('author', instance.author)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description',
                                                  instance.description)
        instance.body = validated_data.get('body', instance.body)
        instance.location = validated_data.get('location', instance.location)
        instance.publication_date = validated_data.get('publication_date',
                                                       instance.publication_date)
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance

    def validate(self, data):
        """Checks that description and title are different"""
        if data['title'] == data['description']:
            raise serializers.ValidationError(
                "Title and description must be different from one another!")
        else:
            return data

    def validate_title(self, value):
        if len(value) < 60:
            raise serializers.ValidationError(
                "The title must at least be 60 characters long!")
        else:
            return value

    def validate_publication_date(self, value):
        if value < date.today():
            raise serializers.ValidationError(
                'The publication date must be later than today')
        else:
            return value
