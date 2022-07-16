from brownie import accounts, reverts

# This test will primarily use accounts 0 and 1 to test.

def test_send_block_mail_fails_if_not_approved(block_mail):
    with reverts("Not allowed to mail user"):
        block_mail.sendBlockMail("This is the message", "This is the title", accounts[1].address, {"from": accounts[0]})

def test_after_approval_user_can_send_mail(block_mail):
    block_mail.allowSender(accounts[0].address, {"from": accounts[1]})
    block_mail.sendBlockMail("This is the message", "This is the title", accounts[1].address, {"from": accounts[0]})

def test_user_can_disallow_sender_anytime(block_mail):
    block_mail.allowSender(accounts[0].address, {"from": accounts[1]})
    block_mail.sendBlockMail("This is the message", "This is the title", accounts[1].address, {"from": accounts[0]})
    block_mail.disallowSender(accounts[0].address, {"from": accounts[1]})
    with reverts("Not allowed to mail user"):
        block_mail.sendBlockMail("This is the message", "This is the title", accounts[1].address, {"from": accounts[0]})

def test_allow_sender_updates_allowed_mailers_mapping_to_true(block_mail):
    block_mail.allowSender(accounts[0].address, {"from": accounts[1]})
    assert block_mail.allowedMailers(accounts[1].address, accounts[0].address) == True

def test_disallow_sender_updates_allowed_mailers_mapping_to_false(block_mail):
    block_mail.allowSender(accounts[0].address, {"from": accounts[1]})
    assert block_mail.allowedMailers(accounts[1].address, accounts[0].address) == True

def test_events_emitted_properly_via_print(block_mail):
    block_mail.allowSender(accounts[0].address, {"from": accounts[1]})
    tx = block_mail.sendBlockMail("This is the message", "This is the title", accounts[1].address, {"from": accounts[0]})
    tx.wait(1)
    print(tx.events)

def test_mail_id_updates(block_mail):
    block_mail.allowSender(accounts[0].address, {"from": accounts[1]})
    block_mail.sendBlockMail("This is the message", "This is the title", accounts[1].address, {"from": accounts[0]})
    assert block_mail.getMailId() == 1

def test_mail_id_is_mapped_to_specific_address(block_mail):
    block_mail.allowSender(accounts[0].address, {"from": accounts[1]})
    tx = block_mail.sendBlockMail("This is the message", "This is the title", accounts[1].address, {"from": accounts[0]})
    tx.wait(1)
    assert block_mail.mailIdToAddress(1) == accounts[1].address

def tets_can_user_decrypt(block_mail):
    block_mail.allowSender(accounts[0].address, {"from": accounts[1]})
    tx = block_mail.sendBlockMail("This is the message", "This is the title", accounts[1].address, {"from": accounts[0]})
    tx.wait(1)
    assert block_mail.canUserDecrypt(1, accounts[0].address, {"from": accounts[0]})
