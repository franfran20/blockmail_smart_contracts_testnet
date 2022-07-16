//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
    @title BlockMail Contract
    @author Francis Egboluche
    @notice A contract for sending and receiving mails on a public data network like IPFS
 */
contract BlockMail {
    //state variables
    uint256 public blockMailFeeAmount;
    uint256 public mailId;

    mapping(address => mapping(address => bool)) public allowedMailers;
    mapping(uint256 => address) public mailIdToAddress;

    //events
    event MailSent(
        uint256 indexed mailID,
        string message,
        string title,
        address indexed receiver,
        address from,
        uint256 nativeAsset
    );

    //ERRORS
    error BlockMail__FailedToSendNativeAsset();

    //external fuctions

    /**
        @notice For sending mails with values from on user to another
        @dev updates the mailID and emits an appropriate event.
        @param _message Encrypted Message Link on a distributed storage system like IPFS.
        @param _title Title for message.
        @param _receiver The receiver of the mail. 
     */
    function sendBlockMail(
        string memory _message,
        string memory _title,
        address _receiver
    ) external payable {
        require(allowedToSendMail(_receiver), "Not allowed to mail user");

        mailId++;
        if (msg.value > 0) {
            (bool success, ) = _receiver.call{value: msg.value}("");
            if (!success) {
                revert BlockMail__FailedToSendNativeAsset();
            }
        }

        mailIdToAddress[mailId] = _receiver;
        emit MailSent(
            mailId,
            _message,
            _title,
            _receiver,
            msg.sender,
            msg.value
        );
    }

    /**
        @notice allows an address to send mail to the user.
        @dev A nice way of making a contacts list to avoid spamming.
        @param _addressToAllow The address the user wishes to receive mails from
     */
    function allowSender(address _addressToAllow) external {
        allowedMailers[msg.sender][_addressToAllow] = true;
    }

    /**
        @notice disallows an address from sending auser mail
        @dev Incase a user decides to no longer see mails from a user.
        @param _addressToDisallow The address the user wishes to stop receiving mails from
     */
    function disallowSender(address _addressToDisallow) external {
        allowedMailers[msg.sender][_addressToDisallow] = false;
    }

    /**
        @notice checks if a certain user is allowed to mail another user
        @param receiver the user being mailed.
        @return bool returns true or false
     */
    function allowedToSendMail(address receiver) private view returns (bool) {
        if (allowedMailers[receiver][msg.sender]) {
            return true;
        } else {
            return false;
        }
    }

    /**
        @notice fucntion for lit protocol to ascertain if the user can decrypt a message
        @param _mailId the user being mailed.
        @param _addressForMailId the address of the user trying to decrypt.
        @return bool returns true or false
     */
    function canUserDecrypt(uint256 _mailId, address _addressForMailId)
        public
        view
        returns (bool)
    {
        if (mailIdToAddress[_mailId] == _addressForMailId) {
            return true;
        } else {
            return false;
        }
    }

    /**
        @notice fucntion for lit protocol to ascertain if the user can decrypt a message
        @return mailId returns the current mail count
     */
    function getMailId() public view returns (uint256) {
        return mailId;
    }
}
