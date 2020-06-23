import abc
import json
import logging

from web3 import Web3

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


class AbstractContract(abc.ABC):
    account: str or hex
    private_key: str or hex
    contract_name: str

    @abc.abstractmethod
    def deploy(self, params: dict, **kwargs):
        """deployed contracts"""
        raise NotImplementedError()

    @abc.abstractmethod
    def call_free_method(self, contract_address: str or hex, method_name, params: dict, **kwargs):
        """call free contract methods"""
        raise NotImplementedError()

    @abc.abstractmethod
    def call_payable_method(self, contract_address: str or hex, method_name: str, params: dict, **kwargs):
        """call payable contract methods"""
        raise NotImplementedError()

    @abc.abstractmethod
    def read_event(self, contract_address: str or hex, event_name: str, tx_hash: str, **kwargs):
        """read contract event"""
        raise NotImplementedError()

    @abc.abstractmethod
    def get_calldata(self, contract_address: str or hex, method_name: str, params: dict, **kwargs):
        """get calldata for call contract method"""
        raise NotImplementedError()

    @abc.abstractmethod
    def decode_input(self, contract_address: str or hex, input_data: str or hex, **kwargs):
        """get decode contract input data"""
        raise NotImplementedError()


class Contract(AbstractContract):
    contract_file_path: str

    def __init__(self, *, account: str, private_key: str,
                 contract_name: str, abi_file: str, bytecode_file: str, rpc_url: str):

        self.w3: Web3 = Web3(Web3.HTTPProvider(rpc_url))

        assert self.w3.isAddress(account), 'account is not address'

        self.account = account
        self.private_key = private_key
        self.contract_name = contract_name
        self._abi_file = abi_file
        self._bytecode_file = bytecode_file

    def get_pending_transaction_count(self, account: str or hex):
        return self.w3.eth.getTransactionCount(account, 'pending')

    def send_raw_transaction(self, raw_transaction):
        transaction_tx = self.w3.eth.sendRawTransaction(raw_transaction.rawTransaction.hex())
        logger.info(f"send raw transaction {raw_transaction}")
        return transaction_tx.hex()

    @property
    def abi(self):
        with open(self._abi_file, 'r') as f:
            abi = f.read()
        return json.loads(abi)

    @property
    def bytecode(self):
        with open(self._bytecode_file, 'r') as f:
            bytecode = f.read()
        return bytecode

    def get_contract(self, contract_address: str or hex = None):

        if contract_address:
            assert self.w3.isAddress(contract_address), 'contract_address is not address'
            contract = self.w3.eth.contract(address=self.w3.toChecksumAddress(contract_address), abi=self.abi)
        else:
            contract = self.w3.eth.contract(abi=self.abi, bytecode=self.bytecode)

        return contract

    def deploy(self, params: dict, **kwargs):

        contract = self.get_contract()
        nonce = self.get_pending_transaction_count(
            self.w3.toChecksumAddress(self.account))

        raw_tx = contract.constructor(*params.get('args', list()), **params.get('kwargs', dict())).buildTransaction(
            {'nonce': nonce, **kwargs})

        raw_tx = self.w3.eth.account.signTransaction(raw_tx, private_key=self.private_key)
        tx = self.send_raw_transaction(raw_tx)
        logger.info(f"send transaction ({tx}) deploy contract {self.contract_name}")

        return tx

    def call_free_method(self, contract_address: str or hex, method_name: str,
                         params: dict, decode_response: bool = True, **kwargs):

        assert self.w3.isAddress(contract_address), 'contract_address is not address'

        contract = self.get_contract(contract_address=contract_address)

        contract_method = getattr(contract.functions, method_name)
        data = contract_method(*params.get('args', list()), **params.get('kwargs', dict())).call()

        if isinstance(data, bytes) and decode_response:
            try:
                return data.decode("utf-8")
            except:
                return data
        elif not isinstance(data, bytes) or not decode_response:
            return data

    def call_payable_method(self, contract_address: str or hex, method_name: str, params: dict, **kwargs):

        assert self.w3.isAddress(contract_address), 'contract_address is not address'

        raw_tx = self._get_calldata(contract_address=contract_address, method_name=method_name, params=params, **kwargs)
        raw_tx = self.w3.eth.account.signTransaction(raw_tx, private_key=self.private_key)
        tx = self.send_raw_transaction(raw_tx)

        logger.info(f"send transaction ({tx}) {method_name} for contract {self.contract_name} ({contract_address})")

        return tx

    def read_event(self, contract_address: str or hex, event_name: str, tx_hash: str or hex, **kwargs):

        assert self.w3.isAddress(contract_address), 'contract_address is not address'

        receipt = self.w3.eth.getTransactionReceipt(tx_hash)
        data = []
        if receipt is None:
            return data

        contract = self.get_contract(contract_address=contract_address)
        contract_event = getattr(contract.events, event_name)

        for event in contract_event().processReceipt(receipt):
            data.append(event['args'])
        return data

    def _get_calldata(self, contract_address: str or hex, method_name: str, params: dict, **kwargs):

        assert self.w3.isAddress(contract_address), 'contract_address is not address'

        contract = self.get_contract(contract_address=contract_address)
        nonce = self.get_pending_transaction_count(
            self.w3.toChecksumAddress(self.account))

        contract_method = getattr(contract.functions, method_name)

        raw_tx = contract_method(*params.get('args', list()), **params.get('kwargs', dict())).buildTransaction(
            {'nonce': nonce, **kwargs})

        return raw_tx

    def get_calldata(self, contract_address: str or hex, method_name: str, params: dict, **kwargs):
        assert self.w3.isAddress(contract_address), 'contract_address is not address'

        return self._get_calldata(contract_address=contract_address, method_name=method_name, params=params, **kwargs)

    def decode_input(self, contract_address: str or hex, input_data: str or hex, **kwargs):

        assert self.w3.isAddress(contract_address), 'contract_address is not address'
        contract = self.get_contract(contract_address=contract_address)
        return contract.decode_function_input(input_data)
