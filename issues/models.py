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

    ISSUE_STATUS = [
        ('LOW', 'Low'),
        ('MED', 'Medium'),
        ('HIG', 'High'),
    ]

    ISSUE_PRIORITY = [
        ('TODO', 'To do'),
        ('PRO', 'In progress'),
        ('FIN', 'Finished'),
    ]

    title = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    creation_date = models.DateField(auto_now_add=True)
    last_update = models.DateField(auto_now=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=3, choices=ISSUE_STATUS)
    priority = models.CharField(max_length=4, choices=ISSUE_PRIORITY, default='TODO')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    assignee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assignee', null=True, blank=True)

    def __str__(self):
        return self.title
