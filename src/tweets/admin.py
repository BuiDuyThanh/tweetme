from django.contrib import admin

# Register your models here.
from .forms import TweetModelForm
from .models import Tweet

# admin.site.register(Tweet)

class TweetModelAdmin(admin.ModelAdmin):
	#form = TweetModelForm	# this is used for ModelForm (forms.py) validation  
	class Meta:				# this is used for validators
		model = Tweet 		# can use both of them

admin.site.register(Tweet, TweetModelAdmin)
