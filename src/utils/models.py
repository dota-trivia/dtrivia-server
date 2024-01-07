from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserStampedModel(models.Model):
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='%(class)s_created')
    updated_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='%(class)s_updated')

    class Meta:
        abstract = True
