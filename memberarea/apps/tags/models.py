from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=20, default='', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name', )
