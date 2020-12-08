from django.db import models
from django.contrib.auth import models as django_models
from django.contrib.auth.models import User


#class User(models.Model):
 #   name = models.CharField(max_length=50)

  #  def __str__(self):
   #     return self.name

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	is_manager = models.BooleanField(default=False)

	def __str__(self):
		return str(self.user) + '->' + str(self.is_manager)



class Post(models.Model):
    #id=models.IntegerField(primary_key=True)
    title=models.CharField(max_length=200,unique=True)
    body=models.TextField()
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    image = models.ImageField(blank=True, null=True)
    like_count=models.IntegerField(default=0)
    comments=models.CharField(max_length=700)

    def __str__(self):
        return self.title


class Likes(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    blog=models.ForeignKey(Post,on_delete=models.CASCADE)

    def __str__(self):
        return self.blog.title + ' -->' + self.user.first_name

from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver  

@receiver(post_save, sender=Likes, dispatch_uid="post_save_blog_like")
def post_save_blog_like(sender, instance, **kwargs):
	if kwargs.get('created'):
		instance.blog.like_count += 1
		instance.blog.save()

@receiver(post_delete, sender=Likes, dispatch_uid="post_delete_blog_like")
def post_delete_blog_like(sender, instance, **kwargs):
	instance.blog.like_count -= 1
	instance.blog.save()
