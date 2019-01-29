from django.contrib import admin
from metrics.models import Block, BlockChain, BlockAdmin, Transaction

admin.site.register(Block, BlockAdmin)
admin.site.register(Transaction)
admin.site.register(BlockChain)
