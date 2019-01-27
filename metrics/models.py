from django.db import models

class BlockChain(models.Model):

    blocks = models


class Block(models.Model):
    b_hash = models.TextField('Block Hash', max_length=2048,default='')
    p_hash = models.TextField('Previous Hash', max_length=2048, default='')
    block_chain = models.ForeignKey(BlockChain, on_delete=models.CASCADE)

    def __str__(self):
        return {"hash": self.b_hash, "prev_hash": self.p_hash}

    class Meta:
        ordering = ('b_hash',)
