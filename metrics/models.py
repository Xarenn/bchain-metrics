from django.contrib import admin
from django.db import models


class BlockChain(models.Model):
    name = models.CharField('name', max_length=255, default='')
    reward = models.IntegerField('reward', default=20)

    def __str__(self):
        return self.name

    @classmethod
    def create(cls, name, reward):
        block_chain = cls(name=name, reward=reward)
        return block_chain

    class Meta:
        ordering = ('name',)


class Wallet(models.Model):
    wallet_hash = models.TextField("Wallet Address", max_length=2048, default='')
    amount = models.TextField("Wallet amount", default=0)

    def __str__(self):
        return self.wallet_hash[:24]

    @classmethod
    def create(cls, wallet_hash, amount):
        return cls(wallet_hash=wallet_hash, amount=amount)

    class Meta:
        ordering = ('wallet_hash',)


class Transaction(models.Model):
    t_hash = models.TextField('Transaction hash', max_length=2048, default='')
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.t_hash[:24]

    @classmethod
    def create(cls, t_hash):
        trx = cls(t_hash=t_hash)
        return trx


class Block(models.Model):
    b_hash = models.TextField('Block Hash', max_length=2048,default='')
    p_hash = models.TextField('Previous Hash', max_length=2048, default='')
    block_chain = models.ForeignKey(BlockChain, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.b_hash

    @classmethod
    def create(cls, b_hash, p_hash, block_chain):
        block = cls(b_hash=b_hash, p_hash=p_hash, block_chain=block_chain)
        return block

    class Meta:
        ordering = ('b_hash',)


class BlockAdmin(admin.ModelAdmin):
    search_fields = ['block_chain__name', 'b_hash']
