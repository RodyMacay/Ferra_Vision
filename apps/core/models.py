from django.db import models
from ..security.models import User
from crum import get_current_user
# Create your models here.
class ModelBase(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    update_by = models.CharField(max_length=100, blank=True, null=True, editable=False)

    @property
    def created_at_format(self):
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S")

    @property
    def updated_at_format(self):
        return self.updated_at.strftime("%Y-%m-%d %H:%M:%S")

    def save(self, *args, **kwargs):
        try:
            user = get_current_user()
            if self._state.adding:
                self.created_by = user.username
            else:
                self.update_by = user.username
        except:
            pass

        models.Model.save(self)

    class Meta:
        abstract = True




class Emotion(ModelBase):
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class UserMood(ModelBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    emotion = models.ForeignKey(Emotion, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}-{self.emotion}"

