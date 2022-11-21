import json
from web3 import Web3


class Binance:
    web_conn: Web3

    def __init__(self, provider: str):
        self.web_conn = Web3(Web3.HTTPProvider(provider))

    def load_api(self):
        abi = open('abi.json')
        abi_load = json.load(abi)
        return abi_load
    
    def creat_contract(self):
        contract = self.web_conn.eth.contract("0x55d398326f99059fF775485246999027B3197955", abi=self.load_api())
        return contract

    def get_decimal(self, contract):
        decimals = contract.functions.decimals().call()
        DECIMALS = 10 ** decimals
        return DECIMALS

    def get_balance(self, address):
        contract = self.creat_contract()
        valid_Address = self.web_conn.toChecksumAddress(address)
        raw_balance = contract.functions.balanceOf(valid_Address).call()
        return raw_balance // self.get_decimal(contract)
