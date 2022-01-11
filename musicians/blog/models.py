from datetime import date

from django.db import models
from django.urls import reverse


class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("blog:entry_list", kwargs={"pk": self.pk})


class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField(default=date.today)
    authors = models.ManyToManyField(Author)
    number_of_comments = models.IntegerField(default=0)
    number_of_pingbacks = models.IntegerField(default=0)
    rating = models.IntegerField(default=5)

    class Meta:
        ordering = ["pub_date", "-mod_date"]

    def __str__(self):
        return self.headline

    def get_absolute_url(self):
        return reverse(
            "blog:entry_details", kwargs={"pk": self.pk, "blog_id": self.blog.pk}
        )
