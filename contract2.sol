pragma solidity ^0.5.1;

contract AccountTransfer {
    address public account1;
    address public account2;

    constructor(address _account1, address _account2) {
        account1 = _account1;
        account2 = _account2;
    }

    function transfer() public {
        uint balance1 = address(this).balance;
        address payable _account1 = payable(account1);
        address payable _account2 = payable(account2);

        // Transfer funds from account1 to account2
        _account1.transfer(balance1);
        // Log the transfer event
        emit Transfer(_account1, _account2, balance1);
    }

    event Transfer(address indexed from, address indexed to, uint amount);
}