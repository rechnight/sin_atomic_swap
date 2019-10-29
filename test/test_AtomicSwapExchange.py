#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import AtomicSwapExchangeWrapper
import WalletWrapper
import SdkUtils
import random
import string
import time
from ontology.util import Address
import hashlib

addr = Address(bytes.fromhex('8f651d459b4f146380dab28e7cfb9d4bb9c3fcd1'))

alice = WalletWrapper.Alice()
aliceAddress = WalletWrapper.AliceAddress()
bob = WalletWrapper.Bob()
bobAddress = WalletWrapper.BobAddress()
eve = WalletWrapper.Eve()
eveAddress = WalletWrapper.EveAddress

def randomSecret(stringLength=20):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase + string.ascii_uppercase
    return bytes(str(time.time()) + ''.join(random.choice(letters) for i in range(stringLength)), 'utf-8')

def getHashlock(secret):
    m = hashlib.sha256()
    m.update(secret)
    return m.digest()


class TestCompiler(unittest.TestCase):
    # def test_initiate_order_new_hashlock(self):
    #     hashlock = randomSecret()
    #     amountOfOntToSell = 100
    #     amountOfEthToBuy = 2
    #     try:
    #         AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock)
    #     except Exception as e:
    #         self.fail(e)

    # def test_initiate_order_as_other_user(self):
    #     hashlock = randomSecret()
    #     amountOfOntToSell = 100
    #     amountOfEthToBuy = 2
    #     with self.assertRaises(Exception):
    #         AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock, initiator=bobAddress)

    # def test_initiate_order_existing_hashlock(self):
    #     hashlock = randomSecret()
    #     amountOfOntToSellInitial = 100
    #     amountOfEthToBuyInitial = 2
    #     AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSellInitial, amountOfEthToBuyInitial, hashlock)
    #     SdkUtils.WaitNextBlock()
    #     amountOfOntToSellUpdated = 200
    #     amountOfEthToBuyUpdated = 3
    #     with self.assertRaises(Exception):
    #         AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSellUpdated, amountOfEthToBuyUpdated, hashlock)

    # def test_initiate_order_data_is_saved(self):
    #     hashlock = randomSecret()
    #     amountOfOntToSell = 100
    #     amountOfEthToBuy = 2
    #     initiator = aliceAddress
    #     AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock)
    #     savedAmountOfOntToSell = AtomicSwapExchangeWrapper.get_amount_of_ont_to_sell(hashlock)
    #     savedAmountOfEthToBuy = AtomicSwapExchangeWrapper.get_amount_of_eth_to_buy(hashlock)
    #     savedHashlock = AtomicSwapExchangeWrapper.get_hashlock(hashlock)

    #     savedAddress = Address(bytes.fromhex(AtomicSwapExchangeWrapper.get_initiator(hashlock)))
    #     savedInitiator = savedAddress.b58encode()

    #     self.assertEqual(savedAmountOfOntToSell, amountOfOntToSell)
    #     self.assertEqual(savedAmountOfEthToBuy, amountOfEthToBuy)
    #     self.assertEqual(savedHashlock, hashlock)
    #     self.assertEqual(savedInitiator, initiator)

    def test_set_buyer_address_as_initiator(self):
        secret = randomSecret()
        hashlock = getHashlock(secret)
        amountOfOntToSell = 100
        amountOfEthToBuy = 2

        AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock, sender=alice)
        SdkUtils.WaitNextBlock()
        buyerAddress = bobAddress
        txHash = AtomicSwapExchangeWrapper.set_buyer_address(hashlock, buyerAddress, sender=alice)
        self.assertTrue(len(txHash))
        
        savedAddress = Address(bytes.fromhex(AtomicSwapExchangeWrapper.get_buyer(hashlock)))
        savedBuyer = savedAddress.b58encode()
        print(savedBuyer)
        self.assertEqual(savedBuyer, buyerAddress)

    def test_set_buyer_address_as_buyer(self):
        secret = randomSecret()
        hashlock = getHashlock(secret)
        amountOfOntToSell = 100
        amountOfEthToBuy = 2

        AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock, sender=alice)

        SdkUtils.WaitNextBlock()
        savedAddress = Address(bytes.fromhex(AtomicSwapExchangeWrapper.get_initiator(hashlock)))
        savedInitiator = savedAddress.b58encode()
        buyerAddress = WalletWrapper.BobAddress()
        print("initiator: ", savedInitiator)
        print("buyer: ", buyerAddress)
        # with self.assertRaises(Exception):
        tx = AtomicSwapExchangeWrapper.set_buyer_address(hashlock, buyer=buyerAddress, sender=bob)
        print(tx)
        
        savedAddress = Address(bytes.fromhex(AtomicSwapExchangeWrapper.get_buyer(hashlock)))
        savedBuyer = savedAddress.b58encode()
        print("{{" + savedBuyer + "}}")
        # self.assertNotEqual(savedBuyer, buyerAddress)

    # def test_set_buyer_address_as_random_user(self):
    #     secret = randomSecret()
    #     hashlock = getHashlock(secret)
    #     amountOfOntToSell = 100
    #     amountOfEthToBuy = 2

    #     AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock, sender=alice)
    #     SdkUtils.WaitNextBlock()
    #     buyerAddress = bobAddress
    #     with self.assertRaises(Exception):
    #         AtomicSwapExchangeWrapper.set_buyer_address(hashlock, buyerAddress, sender=eve)
    #     savedAddress = Address(bytes.fromhex(AtomicSwapExchangeWrapper.get_buyer(hashlock)))
    #     savedBuyer = savedAddress.b58encode()
    #     self.assertNotEqual(savedBuyer, buyerAddress)

    # def test_claim_correct_hashlock(self):
    #     secret = randomSecret()
    #     hashlock = getHashlock(secret)
    #     amountOfOntToSell = 100
    #     amountOfEthToBuy = 2

    #     AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock)
    #     SdkUtils.WaitNextBlock()
    #     # todo set buyer address and claim as buyer
    #     txHash = AtomicSwapExchangeWrapper.claim(hashlock, secret)
    #     self.assertTrue(len(txHash))

    # def test_claim_correct_hashlock_claim_twice(self):
    #     secret = randomSecret()
    #     hashlock = getHashlock(secret)
    #     amountOfOntToSell = 100
    #     amountOfEthToBuy = 2

    #     AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock)
    #     SdkUtils.WaitNextBlock()
    #     # todo set buyer address and claim as buyer
    #     txHash = AtomicSwapExchangeWrapper.claim(hashlock, secret)
    #     self.assertTrue(len(txHash))

    #     SdkUtils.WaitNextBlock()
    #     with self.assertRaises(Exception):
    #         AtomicSwapExchangeWrapper.claim(hashlock, secret)


    # def test_claim_wrong_secret(self):
    #     secret = randomSecret()
    #     hashlock = getHashlock(getHashlock(secret)) + b"blah"
    #     amountOfOntToSell = 100
    #     amountOfEthToBuy = 2

    #     AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock)
    #     SdkUtils.WaitNextBlock()
    #     # todo set buyer address and claim as buyer
    #     with self.assertRaises(Exception):
    #         AtomicSwapExchangeWrapper.claim(hashlock, secret)

    # def test_claim_buyer_not_set(self):
    #     self.assertTrue(False)

    # def test_claim_wrong_buyer_address(self):
    #     self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
