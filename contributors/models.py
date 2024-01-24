from django.db import models


class Contributor(models.Model):
    ROLE_CHOICES = [
        ('Administrator', 'Administrator'),
        ('Editor', 'Editor'),
        ('Viewer', 'Viewer'),
    ]
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.project.title}"
