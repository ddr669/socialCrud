from django.db import models

class PostIT(models.Model):
    username = models.CharField(auto_created=True,max_length=32)
    update_time = models.DateField(auto_now_add=True, null=True)
    created_datetime = models.DateField(auto_now=True)
    creator = models.CharField(default='Anon',max_length=320)
    title = models.CharField(max_length=32)
    content = models.CharField(max_length=320)
    ip_andress = models.GenericIPAddressField(auto_created=True ,null=True)

    def __getName__(self)->dict:
        return {"username":self.username}