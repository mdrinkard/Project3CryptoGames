/*
Blackjack Tokens
*/

pragma solidity ^0.5.10;
/*Creating the fungible token along with the value and symbol*/
contract ChipToken {
    address payable owner = msg.sender;
    string public symbol = "WALE"; 
    uint public exchange_rate = 10;
    uint public totalSupply = 60000;

    mapping(address => uint) balances;
/*Owner holding all fixed tokens*/
    constructor() public {
        balances[owner] = totalSupply; 
    }

/* showing how many tokens the player currently has in their account*/
    function balance() public view returns(uint) {
        return balances[msg.sender];
    }

/*allows players to purchase tokens by sending Ether to the contract based on the exchange rate*/
    function purchaseTokens() public payable {
    uint amountOfTokens = msg.value * exchange_rate;
    balances[msg.sender] += amountOfTokens;
    owner.transfer(msg.value);
}
/*allows players to exchange their tokens back to the casino*/
function exchange(uint amount) public {
        require(amount <= balances[msg.sender], "Insufficient balance");
        balances[msg.sender] -= amount;
        balances[owner] += amount;
    }
}
