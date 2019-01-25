from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from rest_framework import generics

from metrics.models import Block


class ListBlocksView(generics.ListAPIView):
    queryset = Block.objects.all()

class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=({"user": "Userek"}))
