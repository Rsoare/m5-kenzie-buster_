from django.db import models


class RatingChoices(models.Choices):
    G = "G"
    PG = "PG"
    PG_13 = "PG-13"
    R = "R"
    NC_17 = "NC-17"


class Movie(models.Model):
    title = models.CharField(max_length=127)
    duration = models.CharField(max_length=10, blank=True, default=None, null=True)
    rating = models.CharField(max_length=20, blank=True, choices=RatingChoices.choices, default=RatingChoices.G)
    synopsis = models.TextField(blank=True, default=None, null=True)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="movies")
    orders = models.ManyToManyField("users.User", through="movies.MovieOrder", related_name="orders_movies")


class MovieOrder(models.Model):
    movie = models.ForeignKey("movies.Movie", on_delete=models.CASCADE, related_name="movies")
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="user_order_movies")

    buyed_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
