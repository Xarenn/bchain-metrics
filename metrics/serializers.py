from rest_framework import serializers

from metrics.models import Block

class BestBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ('id', 'b_hash', 'p_hash')

class BlockSerializer(serializers.Serializer):
    b_hash = serializers.CharField(read_only=True)
    p_hash = serializers.CharField(read_only=True)


    def create(self, validated_block_data):
        """
        Create and return a new `Block` instance, given the validated data.
        """
        return Block.objects.create(**validated_block_data)

    def update(self, instance, validated_block_data):
        """
        Update and return an existing `Block` instance, given the validated data.
        """
        instance.b_hash = validated_block_data.get('Block Hash', instance.b_hash)
        instance.p_hash = validated_block_data.get('Previous Hash', instance.p_hash)

        instance.save()
        return instance