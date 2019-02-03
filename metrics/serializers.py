from rest_framework import serializers

from metrics.models import Block, BlockChain, Transaction, Wallet


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class BlockChainSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlockChain
        fields = '__all__'


class BestBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ('id', 'b_hash', 'p_hash')


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('__all__')
