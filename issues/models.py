from django.db import models

from projects.models import Project
from users.models import CustomUser


# Create your models here.
class Issue(models.Model):
    """Issue model"""
    ISSUE_TYPE = [
        ('BUG', 'Bug'),
        ('TAS', 'Task'),
        ('FEA', 'Feature'),
    ]

    ISSUE_PRIORITY = [
        ('LOW', 'Low'),
        ('MED', 'Medium'),
        ('HIG', 'High'),
    ]

    ISSUE_STATUS = [
        ('TODO', 'To do'),
        ('PRO', 'In progress'),
        ('FIN', 'Finished'),
    ]

    title = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    creation_date = models.DateField(auto_now_add=True)
    last_update = models.DateField(auto_now=True)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='project_issues')
    status = models.CharField(max_length=4, choices=ISSUE_STATUS, default='TODO')
    priority = models.CharField(max_length=3, choices=ISSUE_PRIORITY)
    author = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='user_issues')

    def __str__(self):
        return self.title
