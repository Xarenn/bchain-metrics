from django.http import JsonResponse
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError

from django.views.generic import TemplateView
from rest_framework import generics
from rest_framework.utils import json

from metrics.models import Block, BlockChain, Transaction, Wallet
from metrics.serializers import BestBlockSerializer, BlockChainSerializer, TransactionSerializer, WalletSerializer


class BlockView(generics.ListAPIView):

    @staticmethod
    def get_chain_by_name(chain_name) -> BlockChain:
        return BlockChain.objects.get(name=chain_name)

    def get_queryset(self):
        return Block.objects.all()

    @staticmethod
    def get_queryset_by_pk(pk) -> Block:
        return Block.objects.get(pk=pk)

    @staticmethod
    def get_block_by_id(block_id) -> Block:
        return Block.objects.get(id=block_id)

    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
            queryset = self.get_queryset()
            serializer = BestBlockSerializer(queryset, many=True)
            try:
                if kwargs['id'] is not None:
                    try:
                        serializer = BestBlockSerializer(self.get_block_by_id(kwargs['id']))
                        return JsonResponse(serializer.data, safe=False, status=200)
                    except Block.DoesNotExist:
                        return JsonResponse("Block does not exist", status=404, safe=False)
            except KeyError:
                return JsonResponse(serializer.data, status=200, safe=False)

    def post(self, request) -> JsonResponse:
        if request.method == 'POST':
            try:
                b_hash = request.data['b_hash']
                p_hash = request.data['p_hash']
                b_chain_name = request.data['b_chain_name']
                b_chain = self.get_chain_by_name(b_chain_name)
                Block.objects.create(b_hash=b_hash, p_hash=p_hash, block_chain=b_chain)

                return JsonResponse("Successful", safe=False, status=200)
            except KeyError:
                return JsonResponse("Cannot find data", safe=False, status=400)


class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=({"user": "Userek"}))


class ChainView(generics.ListAPIView):

    def get_queryset(self):
        return BlockChain.objects.all()

    @staticmethod
    def get_chain_by_name(chain_name) -> BlockChain:
        return BlockChain.objects.get(name=chain_name)

    def return_block_chain_by_name(self, queryset, name) -> JsonResponse:
        try:
            b_chain = self.get_chain_by_name(name)
            block_chain_serializer = BlockChainSerializer(b_chain)
            chain_serializer = BestBlockSerializer(b_chain.block_set.all(), many=True)
        except BlockChain.DoesNotExist:
            return JsonResponse("BlockChain doesnt found", status=404, safe=False)

        return JsonResponse(({"BlockChain": block_chain_serializer.data,
                              "chain": chain_serializer.data}), status=200, safe=False)

    @staticmethod
    def default_return_block_chain(queryset) -> JsonResponse:
        try:
            b_chain = queryset[0]
            serializer = BlockChainSerializer(b_chain)
            chain = b_chain.block_set.all()
            chain_serializer = BestBlockSerializer(chain, many=True)

            return JsonResponse(({"BlockChain": serializer.data,
                                  "chain": chain_serializer.data}), status=200, safe=False)
        except IndexError:
            return JsonResponse("Cannot find any block chains ", status=404, safe=False)

    def get(self, request, *args, **kwargs) -> JsonResponse:
        if request.method == 'GET':
            queryset = self.get_queryset()
            try:
                chain_name = request.GET['name']
                return self.return_block_chain_by_name(queryset, chain_name)
            except MultiValueDictKeyError:
                return self.default_return_block_chain(queryset)

    def post(self, request, *args, **kwargs) -> JsonResponse:
        if request.method == 'POST':
            try:
                chain = self.get_chain_by_name(request.data['chain_name'])
                reward = request.data['reward']

                blocks_data = request.data['chain']
                blocks = chain.block_set.all()
                b_data = BestBlockSerializer(blocks, many=True).data
                if b_data == blocks_data and chain.reward == reward:
                    return JsonResponse("Valid chain", safe=False, status=200)
                else:
                    return JsonResponse("Chain is not valid", safe=False, status=200)

            except KeyError as exc:
                return JsonResponse("Bad request -> without " + str(exc), status=400, safe=False)


class TransactionView(generics.ListAPIView):

        def get_queryset(self):
            return Transaction.objects.all()

        def get(self, request, *args, **kwargs) -> JsonResponse:
            if request.method == 'GET':
                queryset = self.get_queryset()
                transactions = TransactionSerializer(queryset, many=True)

                return JsonResponse(transactions.data, safe=False, status=200)

        @staticmethod
        def create_transaction(request) -> JsonResponse:
            if request.method == 'POST':
                try:
                    t_hash = request.data['trx_hash']
                    Transaction.objects.create(t_hash=t_hash)
                except KeyError as exc:
                    return JsonResponse("Bad request -> without transaction hash " + str(exc))


class SynchronizeView(generics.ListAPIView):

    @staticmethod
    def parse_block(req_data, chain):
        try:
            block_data = dict(req_data)
            block = Block.create(b_hash=block_data['b_hash'],
                                 p_hash=block_data['p_hash'],
                                 block_chain=chain)
            return block
        except KeyError as exc:
            return None

    def get(self, request, *args, **kwargs) -> JsonResponse:
        if request.method == 'GET':
            return JsonResponse("OK", safe=False, status=200)

        return JsonResponse("OK", safe=False, status=200)

    # Last element -> the name of chain
    # { "name": "Chain_Name" }
    # if error occurs return None
    @staticmethod
    def filter_name(text):
        try:
            txt = text[len(text)-1]
            return txt['name']
        except KeyError as exc:
            return None

    def parse_blocks_from_data(self, chain, chain_data):
        return [self.parse_block(block, chain) for block in chain_data]

    def parse_blocks(self, chain, chain_data):
        return list(filter(lambda block: block is not None, self.parse_blocks_from_data(chain, chain_data)))

    def valid_blocks(self, blocks, chain):
        validated_blocks = chain.block_set.all()
        if any(block in validated_blocks for block in blocks):
            return JsonResponse("Chain validated", safe=False, status=200)
        else:
            self.update_blocks(blocks, chain)
            return JsonResponse("chain updated", safe=False, status=201)

    @staticmethod
    def update_blocks(blocks, chain):
        chain.block_set.all().delete()
        for block in reversed(blocks):
            block.save()

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            chain_data = json.loads(request.data)
            name = self.filter_name(chain_data)
            if name is not None:
                try:
                    chain = BlockChain.objects.get(name=name)
                    blocks = self.parse_blocks(chain, chain_data)
                    return self.valid_blocks(blocks, chain)
                except BlockChain.DoesNotExist as exc:
                    return JsonResponse("Chain not found", status=404, safe=False)
            else:
                return JsonResponse("Bad request, doesn't have name ", status=400, safe=False)


class WalletView(generics.ListAPIView):

    @staticmethod
    def get_wallet_by_address(address):
        try:
            return Wallet.objects.get(wallet_hash=address)
        except Wallet.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
            try:
                if kwargs['address'] is not None:
                    wallet = self.get_wallet_by_address(args['address'])
                    if wallet is not None:
                        wallet_data = WalletSerializer(wallet, many=False).data
                        return JsonResponse(wallet_data, safe=False, status=200)
                    else:
                        return JsonResponse("Wallet not found", safe=False, status=404)
                else:
                    return JsonResponse("Wallet not found", safe=False, status=400)
            except KeyError as exc:
                return JsonResponse("Address not found", safe=False, status=404)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            try:
                address = request.data['pub_key']
                Wallet.objects.create(wallet_hash=address, amount=0)
                return JsonResponse("Wallet created", safe=False, status=200)
            except KeyError as exc:
                return JsonResponse("Bad request"+str(exc), safe=False, status=400)
