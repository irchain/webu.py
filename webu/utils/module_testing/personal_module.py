from eth_utils import (
    is_checksum_address,
    is_list_like,
    is_same_address,
)

PRIVATE_KEY_HEX = '0x56ebb41875ceedd42e395f730e03b5c44989393c9f0484ee6bc05f933673458f'
PASSWORD = 'webu-testing'
ADDRESS = '0x844B417c0C58B02c2224306047B9fb0D3264fE8c'


PRIVATE_KEY_FOR_UNLOCK = '0x392f63a79b1ff8774845f3fa69de4a13800a59e7083f5187f1558f0797ad0f01'
ACCOUNT_FOR_UNLOCK = '0x12efDc31B1a8FA1A1e756DFD8A1601055C971E13'


class PersonalModuleTest:
    def test_personal_importRawKey(self, webu):
        actual = webu.personal.importRawKey(PRIVATE_KEY_HEX, PASSWORD)
        assert actual == ADDRESS

    def test_personal_listAccounts(self, webu):
        accounts = webu.personal.listAccounts
        assert is_list_like(accounts)
        assert len(accounts) > 0
        assert all((
            is_checksum_address(item)
            for item
            in accounts
        ))

    def test_personal_lockAccount(self, webu, unlocked_account):
        # TODO: how do we test this better?
        webu.personal.lockAccount(unlocked_account)

    def test_personal_unlockAccount_success(self,
                                            webu,
                                            unlockable_account,
                                            unlockable_account_pw):
        result = webu.personal.unlockAccount(unlockable_account, unlockable_account_pw)
        assert result is True

    def test_personal_unlockAccount_failure(self,
                                            webu,
                                            unlockable_account):
        result = webu.personal.unlockAccount(unlockable_account, 'bad-password')
        assert result is False

    def test_personal_newAccount(self, webu):
        new_account = webu.personal.newAccount(PASSWORD)
        assert is_checksum_address(new_account)

    def test_personal_sendTransaction(self,
                                      webu,
                                      unlockable_account,
                                      unlockable_account_pw):
        assert webu.eth.getBalance(unlockable_account) > webu.toWei(1, 'ether')
        txn_params = {
            'from': unlockable_account,
            'to': unlockable_account,
            'gas': 21000,
            'value': 1,
            'gasPrice': webu.toWei(1, 'gwei'),
        }
        txn_hash = webu.personal.sendTransaction(txn_params, unlockable_account_pw)
        assert txn_hash
        transaction = webu.eth.getTransaction(txn_hash)
        assert transaction['from'] == txn_params['from']
        assert transaction['to'] == txn_params['to']
        assert transaction['gas'] == txn_params['gas']
        assert transaction['value'] == txn_params['value']
        assert transaction['gasPrice'] == txn_params['gasPrice']

    def test_personal_sign_and_ecrecover(self,
                                         webu,
                                         unlockable_account,
                                         unlockable_account_pw):
        message = 'test-webu-personal-sign'
        signature = webu.personal.sign(message, unlockable_account, unlockable_account_pw)
        signer = webu.personal.ecRecover(message, signature)
        assert is_same_address(signer, unlockable_account)
