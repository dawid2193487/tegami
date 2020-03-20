from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView
from django.shortcuts import redirect
from django.contrib import messages
from .models import *
from .forms import *

# Create your views here.
class BoardList(ListView):
    model = Board

class BoardView(DetailView):
    model = Board

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["threads"] = self.object.thread_set.all().order_by("-posted_at")
        context["thread_form"] = ResponseForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ResponseForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.cleaned_data["message"]
            t = Thread.objects.create(posted_by=request.user, message=message, board=self.object)
            form.save_attachements(t)
            return redirect("thread", board=self.object.slug, pk=t.pk)
        else:
            messages.add_message(request, messages.ERROR, "Invalid form.")
            return redirect("board", slug=self.object.slug)
        

class ThreadView(DetailView):
    model = Thread

    def get(self, request, *args, **kwargs):
        # the board slug is a non-essential part of the URL
        # this redirects to an URL with the correct board slug
        # if it's incorrect
        self.object = self.get_object()
        if kwargs["board"] != self.object.board.slug:
            return redirect("thread", board=self.object.board.slug, pk=self.object.pk)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["replies"] = self.object.reply_set.all().order_by("posted_at")
        context["reply_form"] = ResponseForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ResponseForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.cleaned_data["message"]
            r = Reply.objects.create(posted_by=request.user, message=message, reply_in=self.object)
            form.save_attachements(r)
        else:
            messages.add_message(request, messages.ERROR, "Invalid form.")
        
        return redirect("thread", board=self.object.board.slug, pk=self.object.pk)
        