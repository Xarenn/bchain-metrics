from django.contrib import admin
from django.db import models


class BlockChain(models.Model):
    name = models.CharField('name', max_length=255, default='')
    reward = models.IntegerField('reward', default=20)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Transaction(models.Model):
    t_hash = models.TextField('Transaction hash', max_length=2048, default='')

    def __str__(self):
        return self.t_hash[:24]


class Block(models.Model):
    b_hash = models.TextField('Block Hash', max_length=2048,default='')
    p_hash = models.TextField('Previous Hash', max_length=2048, default='')
    block_chain = models.ForeignKey(BlockChain, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.b_hash

    class Meta:
        ordering = ('b_hash',)


class BlockAdmin(admin.ModelAdmin):
    search_fields = ['block_chain__name', 'b_hash']
