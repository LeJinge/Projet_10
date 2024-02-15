from django.db import models

from issues.models import Issue
from users.models import CustomUser


class Comment(models.Model):
    description = models.TextField()
    issue = models.ForeignKey('issues.Issue', on_delete=models.CASCADE, related_name='issue_comments')
    author = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='user_comments')
    creation_date = models.DateField(auto_now_add=True)
    last_update = models.DateField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.issue.title}"
