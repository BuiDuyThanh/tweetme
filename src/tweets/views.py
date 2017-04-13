from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import DetailView, DeleteView, ListView, CreateView, UpdateView

from .forms import TweetModelForm
from .mixins import FormUserNeededMixin, UserOwnerMixin
from .models import Tweet

#------------------Class-based View------------------#


# RETWEET

class RetweetView(View):
	def get(self, request, pk, *args, **kwargs):
		tweet = get_object_or_404(Tweet, pk=pk)
		if request.user.is_authenticated():
			new_tweet = Tweet.objects.retweet(request.user, tweet)
			return HttpResponseRedirect("/")
		return HttpResponseRedirect(tweet.get_absolute_url())

# CREATE

class TweetCreateView(FormUserNeededMixin, CreateView): # --> add LoginRequiredMixin if want to use
	#queryset = Tweet.objects.all()
	form_class = TweetModelForm
	template_name = "tweets/create_view.html"

	#success_url = "/tweet/create/"   				|---> use function 'get_absolute_url' in models.py instead
	#success_url = reverse_lazy("tweet:detail")		|		
	
	#login_url = "/admin/"
	#fields = ['user', 'content']

# UPDATE

class TweetUpdateView(LoginRequiredMixin, UserOwnerMixin, UpdateView):
	queryset = Tweet.objects.all()
	form_class = TweetModelForm
	template_name = "tweets/update_view.html"
	#success_url = "/tweet/"      					---> use function 'get_absolute_url' in models.py instead

# DELETE

class TweetDeleteView(LoginRequiredMixin, DeleteView):
	model = Tweet
	template_name = "tweets/delete_confirm.html"
	success_url = reverse_lazy("tweet:list") # reverse()

# RETRIEVE

class TweetDetailView(DetailView):
	# template_name = "tweets/detail_view.html"
	queryset = Tweet.objects.all()

	# def get_object(self):
	# 	print(self.kwargs)
	#	pk = self.kwargs.get("pk") # pk = self.kwargs["pk"]
	#	print(pk)
	#	return Tweet.objects.get(id=pk)

	# def get_object(self):
	# 	print(self.kwargs)
	#	pk = self.kwargs.get("pk") # pk = self.kwargs["pk"]
	#	obj = get_object_or_404(Tweet, pk=pk)
	#	return obj

# LIST

class TweetListView(LoginRequiredMixin, ListView):
	# template_name = "tweets/list_view.html"
	# queryset = Tweet.objects.all()

	def get_queryset(self, *args, **kwargs):
		qs = Tweet.objects.all()
		query = self.request.GET.get("q", None)
		if query is not None:
			qs = qs.filter(
				Q(content__icontains=query)|
				Q(user__username__icontains=query)
				)
		return qs

	def get_context_data(self, *args, **kwargs):
		context = super(TweetListView, self).get_context_data(*args, **kwargs)
		# context["another_list"] = Tweet.objects.all()
		# print(context)
		context["create_form"] = TweetModelForm
		context["create_url"] = reverse_lazy("tweet:create")
		return context

#-------------------Function-based views------------------

# RETRIEVE

def tweet_detail_view(request, pk=None): # pk == id
	# obj = Tweet.objects.get(pk=pk) # Cannot serve non-exist object # GET from database
	obj = get_object_or_404(Tweet, pk=pk)
	# print(obj)
	context = {
		"object": obj
	}
	return render(request, "tweets/detail_view.html", context)

# LIST

def tweet_list_view(request):
	queryset = Tweet.objects.all()
	# print(queryset)
	# for obj in queryset:
	# 	print(obj.content)
	context = {
		"object_list": queryset
	}
	return render(request, "tweets/list_view.html", context)

# CREATE

def tweet_create_view(request):
	form = TweetModelForm(request.POST or None)

	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
	context = {
		"form": form
	}
	return render(request, "tweets/create_view.html", context)	