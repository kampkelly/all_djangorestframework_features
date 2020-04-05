from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class CommonFieldsMixin(models.Model):
    """Add created_at and updated_at fields."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        """Define metadata options."""

        abstract = True


class Category(CommonFieldsMixin):
    name = models.CharField(max_length=250,null=False,unique=True)


class Notes(CommonFieldsMixin):
    title = models.CharField(max_length=250,null=False,unique=False)
    body = models.TextField(null=False)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default=None,related_name='notes')


class PersonManager(models.Manager):
    def get_queryset(self):
        return User.objects.all()

    def all_users(self):
        return [1,2,4]

class Person(User):
    objects = PersonManager()    

    class Meta:
        proxy = True
