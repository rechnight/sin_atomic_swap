# from ontology.interop.System.Runtime import GetTime, CheckWitness, Log, Notify, Serialize, Deserialize
from ontology.interop.System.Storage import Put, Get, GetContext
from ontology.builtins import *
from LibUtils.ContractUtils import ConcatKey, Revert, Require, WitnessRequire

context = GetContext()

HASH = 'Hash'
ONT_TO_SELL =  'OntToSell'
ETH_TO_BUY = 'EthToBuy'
INITIATOR = "Initiator"


def Main(operation, args):
    if operation == 'intiate_order':
        ont_to_sell = args[0]
        eth_to_buy = args[1]
        hashlock = args[2]
        initiator = args[3]
        return intiate_order(ont_to_sell, eth_to_buy, hashlock, initiator)
    if operation == 'get_amount_of_ont_to_sell':
        hashlock = args[0]
        return get_amount_of_ont_to_sell(hashlock)
    if operation == 'get_amount_of_eth_to_buy':
        hashlock = args[0]
        return get_amount_of_eth_to_buy(hashlock)
    if operation == 'get_hashlock':
        hashlock = args[0]
        return get_hashlock(hashlock)
    if operation == 'get_initiator':
        hashlock = args[0]
        return get_initiator(hashlock)


def intiate_order(ont_to_sell, eth_to_buy, hashlock, initiator):
    WitnessRequire(initiator)
    order_id = hashlock
    if len(Get(context, ConcatKey(order_id, HASH))) != 0:
        Revert()
    Put(context, ConcatKey(order_id, HASH), hashlock)
    Put(context, ConcatKey(order_id, ETH_TO_BUY), eth_to_buy)
    Put(context, ConcatKey(order_id, ONT_TO_SELL), ont_to_sell)
    Put(context, ConcatKey(order_id, INITIATOR), initiator)

def get_amount_of_ont_to_sell(order_id):
    return Get(context, ConcatKey(order_id, ONT_TO_SELL))

def get_amount_of_eth_to_buy(order_id):
    return Get(context, ConcatKey(order_id, ETH_TO_BUY))

def get_hashlock(order_id):
    return Get(context, ConcatKey(order_id, HASH))

def get_initiator(order_id):
    return Get(context, ConcatKey(order_id, INITIATOR))
    
    