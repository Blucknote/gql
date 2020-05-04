from django.db import models


class Category(models.Model):

    name = models.CharField(
        max_length=32
    )

    def __str__(self):
        return self.name


class Publish(models.Model):

    text = models.TextField(
        max_length=2048,
    )

    published = models.BooleanField(
        default=False
    )

    categories = models.ManyToManyField(
        Category,
        related_name='publishes',
    )

    def __str__(self):
        return ' '.join(
            [
                self.text[:16],
                '/'.join(
                    self.categories.values_list('name', flat=True)
                )
            ]
        )


class Comment(models.Model):
    text = models.TextField(
        max_length=2048
    )

    published = models.BooleanField(
        default=False
    )

    publish = models.ForeignKey(
        Publish,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    def __str__(self):
        return self.text[:32]



