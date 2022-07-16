from brownie import accounts
import pytest

@pytest.fixture()
def block_mail(BlockMail):
    block_mail = BlockMail.deploy({"from": accounts[0]})
    return block_mail