from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from .models import Group,GroupMember
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin
from django.views.generic import CreateView,DeleteView,UpdateView,DetailView,ListView,RedirectView
from django.contrib import messages
# Create your views here.

class CreateGroup(LoginRequiredMixin,CreateView):
    fields = ('name','description')
    model = Group

class SingleGroup(DetailView):
    model = Group


class ListGroup(ListView):
    model = Group
    
class leaveGroup(LoginRequiredMixin,RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get("slug")})

    def get(self,request,*args,**kwargs):
        try:
            membership = GroupMember.objects.filter(
            user=self.request.user,
            group__slug = self.kwargs.get("slug").get()
            )
        except:
            messages.warning(self.request,'You are not joined as a member in this group')
        else:
            membership.delete()
            messages.success(self.request,"You left the group")
        return super().get(self,request,*args,**kwargs)

class Joingroup(RedirectView,LoginRequiredMixin):

    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single',kwargs={"slug":self.kwargs.get("slug")})
    
    def get(self,request,*args,**kwargs):
        group = get_object_or_404(Group,slug=self.kwargs.get("slug"))

        try:
            GroupMember.objects.create(user=self.request.user,group=group)

        except IntegrityError:
            messages.warning(self.request,("Warning, already a member of {}".format(group.name)))

        else:
            messages.success(self.request,"You are now a member of the {} group.".format(group.name))

        return super().get(request, *args, **kwargs)
        