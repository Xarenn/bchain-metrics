from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from django.views.generic import TemplateView
from rest_framework import generics

from metrics.models import Block
from metrics.serializers import BlockSerializer, BestBlockSerializer


class ListBlocksView(generics.ListAPIView):

    def get_queryset(self):
        return Block.objects.all()

    def get_queryset_withPK(self, pk):
        return Block.objects.get(pk=pk)

    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
            queryset = self.get_queryset()
            serializer = BlockSerializer(queryset, many=True)
            if kwargs['pk'] is not None:
                try:
                    serializer = BestBlockSerializer(self.get_queryset_withPK(kwargs['pk']))
                    return JsonResponse(serializer.data, safe=False, status=200)
                except Block.DoesNotExist:
                    return HttpResponse(status=404)

            return JsonResponse(serializer.data, status=200, safe=False)


class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=({"user": "Userek"}))

