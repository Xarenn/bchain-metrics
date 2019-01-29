from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError

from django.views.generic import TemplateView
from rest_framework import generics

from metrics.models import Block, BlockChain, Transaction
from metrics.serializers import BestBlockSerializer, BlockChainSerializer, TransactionSerializer


class BlockView(generics.ListAPIView):

    def get_queryset(self):
        return Block.objects.all()

    @staticmethod
    def get_queryset_by_pk(pk):
        return Block.objects.get(pk=pk)

    @staticmethod
    def get_block_by_id(block_id):
        return Block.objects.get(id=block_id)

    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
            queryset = self.get_queryset()
            serializer = BestBlockSerializer(queryset, many=True)
            try:
                if kwargs['pk'] is not None:
                    try:
                        serializer = BestBlockSerializer(self.get_block_by_id(kwargs['pk']))
                        return JsonResponse(serializer.data, safe=False, status=200)
                    except Block.DoesNotExist:
                        return JsonResponse("Block does not exist", status=404, safe=False)
            except KeyError:
                return JsonResponse(serializer.data, status=200, safe=False)


class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=({"user": "Userek"}))


class ChainView(generics.ListAPIView):

    def get_queryset(self):
        return BlockChain.objects.all()

    @staticmethod
    def return_block_chain_by_name(queryset, name):
        b_chain = queryset[str(name)]
        block_chain_serializer = BlockChainSerializer(b_chain)
        chain_serializer = BestBlockSerializer(b_chain.block_set.all(), many=False)

        return JsonResponse(({"BlockChain": block_chain_serializer.data,
                              "chain": chain_serializer}), status=200, safe=False)

    @staticmethod
    def default_return_block_chain(queryset):
        try:
            b_chain = queryset[0]
            serializer = BlockChainSerializer(b_chain)
            chain = b_chain.block_set.all()
            chain_serializer = BestBlockSerializer(chain, many=True)

            return JsonResponse(({"BlockChain": serializer.data,
                                  "chain": chain_serializer.data}), status=200, safe=False)
        except IndexError:
            return JsonResponse("Cannot find any block chains ", status=404, safe=False)

    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
            queryset = self.get_queryset()
            try:
                chain_name = request.GET['name']
                return self.return_block_chain_by_name(chain_name)
            except MultiValueDictKeyError:
                return self.default_return_block_chain(queryset)


class TransactionView(generics.ListAPIView):

        def get_queryset(self):
            return Transaction.objects.all()

        def get(self, request, *args, **kwargs):
            if request.method == 'GET':
                queryset = self.get_queryset()
                transactions = TransactionSerializer(queryset, many=True)

                return JsonResponse(transactions.data, safe=False, status=200)
