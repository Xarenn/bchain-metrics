from django.db import IntegrityError
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework.utils import json

from metrics.models import Block, BlockChain, Transaction
from metrics.serializers import BestBlockSerializer, BlockChainSerializer


class BlockModelTest(TestCase):

    def setUp(self):
        block_chain = BlockChain.objects.create(name="TestBlockChain", reward=30)
        Block.objects.create(b_hash="test_block_hash", p_hash="test_prev_hash", block_chain=block_chain)

    def test_validate_block(self):
        with self.assertRaises(IntegrityError):
            Block.objects.create(b_hash="failed", p_hash="failed", block_chain=None)

    def test_check_length_in_db(self):
        self.assertEqual(len(Block.objects.all()), 1)

    def test_block_from_db(self):
        block_chain = BlockChain.objects.get(name="TestBlockChain")
        block_tested = Block.objects.get(block_chain=block_chain)
        block = Block(b_hash="test_block_hash", p_hash="test_prev_hash", block_chain=block_chain)

        self.assertEqual(block_tested.b_hash, block.b_hash)
        self.assertEqual(block_tested.p_hash, block.p_hash)
        self.assertEqual(block_tested.block_chain, block.block_chain)


class BlockChainModelTest(TestCase):

    def setUp(self):
        block_chain = BlockChain.objects.create(reward=30, name="TestBlockChain")
        Block.objects.create(b_hash="test_hash", p_hash="test_hash", block_chain=block_chain)

    def test_save_block_chain_null(self):
        with self.assertRaises(IntegrityError):
            BlockChain.objects.create(reward=None, name=None)

    def test_check_length_objects(self):
        self.assertEqual(len(BlockChain.objects.all()), 1)

        BlockChain.objects.create(reward=30, name="TestBlockChain")

        self.assertEqual(len(BlockChain.objects.all()), 2)

    def test_get_block_chain_from_db(self):
        block_chain = BlockChain.create("TestBlockChain", reward=30)
        block_chain_test = BlockChain.objects.get(name="TestBlockChain")

        self.assertEqual(block_chain_test.reward, block_chain.reward)
        self.assertEqual(block_chain_test.name, block_chain.name)

    def test_get_chain_from_object_db(self):
        block_chain = BlockChain.objects.get(name="TestBlockChain")
        block_test = block_chain.block_set.all()
        block = Block.create(b_hash="test_hash", p_hash="test_hash", block_chain=block_chain)

        self.assertEqual(len(block_test), 1)
        self.assertEqual(block_test[0].b_hash, block.b_hash)
        self.assertEqual(block_test[0].p_hash, block.p_hash)


class TransactionModelTest(TestCase):

    def setUp(self):
        Transaction.objects.create(t_hash="test_transaction_hash")

    def test_transaction_from_db(self):
        transaction = Transaction.create(t_hash="test_transaction_hash")
        trx_from_db = Transaction.objects.all()

        self.assertEqual(len(trx_from_db), 1)
        self.assertEqual(trx_from_db[0].t_hash, transaction.t_hash)


class BlockRestTest(APITestCase):

    def setUp(self):
        block_chain = BlockChain.objects.create(name="TestBlockChain", reward=15)
        Block.objects.create(b_hash="test_hash", p_hash="test_hash", block_chain=block_chain)

    def test_get_blocks(self):
        url = "/api/v1/blocks/"
        response = self.client.get(url, format='json')

        block = Block.objects.all()
        self.assertEqual(len(block), 1)

        block_tested_json = json.loads(response.content.decode('utf-8'))
        self.assertNotEqual(len(block_tested_json), 0)

        block_db_json = BestBlockSerializer(block, many=True).data

        self.assertEqual(len(block_db_json), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(block_tested_json[0]['b_hash'], block_db_json[0]['b_hash'])
        self.assertEqual(block_tested_json[0]['p_hash'], block_db_json[0]['p_hash'])

    def test_get_one_block(self):
        url = "/api/v1/blocks/"

        block = Block.objects.all()
        self.assertEqual(len(block), 1)

        block_id = block[0].id
        response = self.client.get(url+str(block_id), format='json')

        block_db_json = BestBlockSerializer(block[0]).data
        block_response_json = json.loads(response.content)

        self.assertNotEqual(len(block_response_json), 0)
        self.assertEqual(block_db_json['b_hash'], block_response_json['p_hash'])
        self.assertEqual(block_db_json['p_hash'], block_response_json['p_hash'])


class BlockChainRestTest(APITestCase):

    def setUp(self):
        block_chain = BlockChain.objects.create(name="TestBlockChain", reward=25)
        for n in range(0,5):
            Block.objects.create(b_hash="Test_hash_+"+str(n), p_hash="Test_hash"+str(n), block_chain=block_chain)

    def test_get_block_chain_by_name(self):
        url = "/api/v2/chain/?name="
        name = "TestBlockChain"

        block_chain = BlockChain.objects.get(name=name)
        block_chain_response = json.loads(self.client.get(url+name, format='json').content)
        block_chain_db = BlockChainSerializer(block_chain).data

        self.assertNotEqual(len(block_chain_response), 0)

        self.assertEqual(block_chain_db['name'], block_chain_response['BlockChain']['name'])
        self.assertEqual(block_chain_db['reward'], block_chain_response['BlockChain']['reward'])

    def test_get_default_chain(self):
        url = "/api/v2/chain/"

        block_chain_set = BlockChain.objects.all()
        response = self.client.get(url, format='json')

        self.assertNotEqual(len(response.content), 0)
        self.assertEqual(len(block_chain_set), 1)

        block_chain_db = BlockChainSerializer(block_chain_set[0]).data
        block_chain_response = json.loads(response.content)

        self.assertEqual(block_chain_db['name'], block_chain_response['BlockChain']['name'])
        self.assertEqual(block_chain_db['reward'], block_chain_response['BlockChain']['reward'])

    def test_get_blocks_from_chain(self):
        url = "/api/v2/chain/"

        response = self.client.get(url, format='json')
        name_chain = json.loads(response.content)['BlockChain']['name']
        chain = BlockChain.objects.get(name=name_chain)

        blocks_db = Block.objects.all()
        self.assertEqual(len(blocks_db), 5)

        blocks_response = chain.block_set.all()
        self.assertEqual(len(blocks_response), 5)

        for i in range(0, len(blocks_db)):
            self.assertEqual(blocks_db[i].b_hash, blocks_response[i].b_hash)
            self.assertEqual(blocks_db[i].p_hash, blocks_response[i].p_hash)
