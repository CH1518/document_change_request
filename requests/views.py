from django.shortcuts import render
from django.contrib import messages
# Create your views here.
from django.contrib.auth.mixins import (LoginRequiredMixin,PermissionRequiredMixin)
from django.urls import reverse
from django.views import generic
from django.shortcuts import get_object_or_404
from requests.models import Request, Comment
from . import models
from django.http import HttpResponseRedirect, HttpResponse
from braces.views import SelectRelatedMixin
from .forms import CommentForm
from . import forms
from django.views.generic import TemplateView
from django.views.generic.edit import FormMixin

class CreateRequest(LoginRequiredMixin,generic.CreateView):
    fields = ('document_title', 'revision_number','area', 'priority', 'new_document_or_process','are_other_stakeholders_affected', 'requested_changes', 'reason_for_change', 'file_name', 'file')
    model = Request

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

class SingleRequest(generic.DetailView):
    model = Request

class Detail(LoginRequiredMixin, FormMixin, generic.DetailView):
    model = Request
    template_name = 'requests/requests_detail.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('requests:single', kwargs={"slug": self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(body=self.object)
        context['form'] = CommentForm()
        return context

    def post(self, request, slug, *args, **kwargs):
        self.object = self.get_object()
        post = get_object_or_404(Request, slug=slug)
        form = self.get_form()
        new_comment = None
        profile = CommentForm(self.request.user)
        if request.method == 'POST':
            form = CommentForm(data=request.POST)
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.post = post
                new_comment.name = request.user
                new_comment.save()
                return HttpResponseRedirect(reverse('requests:single', kwargs={"slug": self.object.slug}))

class DCRTable(generic.ListView):
    model = Request
    template_name = 'DCR_table.html'

class ListRequests(generic.ListView):
    model = Request

class DCRTable(generic.ListView):
    model = Request
    template_name = 'DCR_table.html'

class UserRequests(generic.ListView):
    model = models.Request
    template_name = 'posts/user_post_list.html'

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related('requests').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        return context
