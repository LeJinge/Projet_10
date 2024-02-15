from django.db import models
from users.models import CustomUser


# Create your models here.
class Project(models.Model):
    PROJECT_TYPE = [
        ('BE', 'Back-end'),
        ('FE', 'Front-end'),
        ('IOS', 'iOS'),
        ('AND', 'Android'),
    ]
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    creation_date = models.DateField(auto_now_add=True)
    last_update = models.DateField(auto_now=True)
    author = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='authored_projects')
    contributors = models.ManyToManyField('users.CustomUser',
                                          through='contributors.Contributor',
                                          related_name='contributing_projects')
    type = models.CharField(max_length=3, choices=PROJECT_TYPE)

    def __str__(self):
        return self.title
