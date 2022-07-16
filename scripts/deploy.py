from brownie import BlockMail, accounts

def main():
    account = accounts.load("francis-test")
    block_mail = BlockMail.deploy({"from": account, "required_confs": 6}, publish_source=True)
    
