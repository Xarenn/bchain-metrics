from rest_framework import serializers

from metrics.models import Block, BlockChain, Transaction


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
