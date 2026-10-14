from django.db import models

class Resume(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    score = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name
