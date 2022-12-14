from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    second_id = models.IntegerField(null=True)


@receiver(post_save, sender=Employee)
def create_second_id(sender, instance, created, *args, **kwargs):
    if (not instance.second_id and instance.second_id != instance.id):   
        instance.second_id = instance.id
        instance.save()
    #print(instance.id)
