from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse_lazy
# Create your models here.

class UserProfileManager(models.Manager):
	use_for_related_fields = True	# this built-in attribute used only for OneToOne relationship. In this case, it is used to tell Django to use this manager for any relationship lookups
#	Read more about Manager and 'use_for_related_fields' attr here:
#	http://stackoverflow.com/questions/6067195/how-does-use-for-related-fields-work-in-django

	def all(self):
		qs = self.get_queryset().all()
	#	print(self)				# accounts.UserProfile.None
	#	print(dir(self))		# all methods in self
	#	print(self.instance)	# user/username

	#	use try block just in case user instance does not exist	
		try:
		#	try to remove my own user from followed_by list (in case follow myself)
			if self.instance:
				qs = qs.exclude(user=self.instance)
		except:
			pass
		return qs
	
	#	to remove or add the target user to the following list; meanwhile return boolean value	
	def toggle_follow(self, user, to_toggle_user):
		user_profile, created = UserProfile.objects.get_or_create(user=user)	# --> (user_obj, true) # the user that go following/unfollowing other users (thanhbui --> damvinhhung)
		if to_toggle_user in user_profile.following.all():
			user_profile.following.remove(to_toggle_user)
			added = False
		else:
			user_profile.following.add(to_toggle_user)
			added = True
		return added


	#	make boolean value for views.py
	def is_following(self, user, followed_by_user):
		user_profile, created = UserProfile.objects.get_or_create(user=user)
		if created:		# if the object is newly created, there will be no following
			return False
		if followed_by_user in user_profile.following.all():
			return True
		return False

	def recommended(self, user, limit_to=10):
		profile = user.profile
		following = profile.following.all()		# just for testing
		following = profile.get_following()
		qs = self.get_queryset().exclude(user__in=following).exclude(id=profile.id).order_by("?")[:limit_to]
		return qs

class UserProfile(models.Model):
	user 		= models.OneToOneField(settings.AUTH_USER_MODEL, related_name="profile")
		# user.profile  --> give me the profile of the user
	following 	= models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="followed_by") # blank is required because Field is required in admin site
		# user.profile.following --> users I follow    |___ this is the ManyToMany/Reverse relationship
		# user.followed_by --> users that follow me    |
	
	objects = UserProfileManager()	# assign the custom UserProfileManager to the 'objects' variables to this class/model to tell it to use. It replaces the default one. In reality, the default one should be the first one and can be used along side with custom one.  
#			<--->   UserProfile.objects.all()
#	damvinhhung = UserProfileManager() # UserProfile.damvinhhung.all()

	def __str__(self):
		return str(self.following.all().count())

	def get_following(self):
		users = self.following.all()	# User.objects.all().exclude(username=self.user.username)
		return users.exclude(username=self.user.username)

	def get_follow_url(self):
		return reverse_lazy("profiles:follow", kwargs={"username":self.user.username})

	def get_absolute_url(self):
		return reverse_lazy("profiles:detail", kwargs={"username":self.user.username})


#	thanhbui = User.objects.first()
#	User.objects.get_or_create()	#	(user_obj, true/false)
#	thanhbui.save()

#	sender/receiver/signals to automatically create profile for newly created user
def post_save_user_receiver(sender, instance, created, *args, **kwargs):
#	print(instance)
	if created:
		new_profile = UserProfile.objects.get_or_create(user=instance)

post_save.connect(post_save_user_receiver, sender=settings.AUTH_USER_MODEL)