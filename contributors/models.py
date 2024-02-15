from django.db import models


class Contributor(models.Model):

    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='contributions')
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='project_contributors')

    def __str__(self):
        return f"{self.user.username} - {self.project.title}"
