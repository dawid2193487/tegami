from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import *

# Create your views here.
class BoardList(ListView):
    model = Board

class Board(DetailView):
    model = Board

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["threads"] = self.object.thread_set.all()
        return context
    