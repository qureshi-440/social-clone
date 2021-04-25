from django.shortcuts import render
from django.urls import reverse_lazy
from .models import *
from django.views import generic
from django.http import Http404
from braces.views import SelectRelatedMixin
from django.contrib.auth import get_user_model,mixins
from django.contrib import messages
from . import forms 
# Create your views here.

User = get_user_model()

class PostList(SelectRelatedMixin,generic.ListView):
    model = Post
    select_related = ('user','group')

class UserPost(generic.ListView):
    model = Post
    template_name = 'posts/user_post_list.html'

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related("posts").get(
                'username__iexact' == self.kwargs.get("username")
            )
        except User.DoesNotExist:
            raise Http404
        else:
            self.post_user.posts.all()

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context["post_user"] = self.post_user
        return context

class PostDetail( SelectRelatedMixin ,generic.DetailView):
    model = Post
    select_related = ('user','group')

    def get_queryset(self):
        quearyset = super().get_queryset()
        return quearyset.filter(
            user__username__iexact=self.kwargs.get('username')
        )

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['user_groups'] = Group.objects.filter(members__in=[self.request.user])
        context['other_groups'] = Group.objects.exclude(members__in= [self.request.user])
        return context

class Createpost(SelectRelatedMixin,mixins.LoginRequiredMixin,generic.CreateView):
    model = Post
    fields = ('message','group')


    def form_invalid(self,form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

class DeletePost(mixins.LoginRequiredMixin,SelectRelatedMixin,generic.DeleteView):
    model = Post
    select_related = ('user','group')
    success_url = 'posts:all'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self,*args,**kwargs):
        messages.success(self.request,"Post Deleted Successfully")
        return super().delete(*args,**kwargs)

        
