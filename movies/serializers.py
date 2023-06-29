from rest_framework import serializers
from movies.models import Movie, RatingChoices, MovieOrder
from rest_framework.validators import UniqueValidator


class MovieSerializers(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=127)
    duration = serializers.CharField(max_length=10, required=False, default=None)
    rating = serializers.ChoiceField(required=False, choices=RatingChoices.choices, default=RatingChoices.G)
    synopsis = serializers.CharField(max_length=None, required=False, default=None)
    added_by = serializers.EmailField(read_only=True, source="user.email")

    def save(self, user):
        return Movie.objects.create(**self.validated_data, user=user)


class MovieOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True, source="movie.title")
    buyed_at = serializers.DateTimeField(read_only=True)
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    buyed_by = serializers.EmailField(read_only=True, source="user.email")

    def save(self, user, movie):

        return MovieOrder.objects.create(**self.validated_data, user=user, movie=movie)
