/*
Blackjack
*/

pragma solidity ^0.5.10;

contract Casino{
    address payable public cashier;

    constructor(address payable _cashier) public  payable {
        cashier = _cashier;
   }
/* showing how many Eth the player currently has in their account*/
    function PurchaseChips() public payable {
        require(msg.value > 0, "must send non-zero Eth");
        // increase or decrease balance of cashier
        cashier.transfer(msg.value);
    }

/*allows players to purchase Eth by sending wei to the contract*/
    function exchange(uint amount) public {
        require(amount > 0, "amount must be greater than 0");
        require(msg.sender == cashier, "only cashier can exchange with players");
    }

/*allows players to exchange their tokens back to the casino*/
    function Cashout (uint amount) external payable {
        require(amount > 0, "amount must be more than 0");
        require(msg.sender != cashier, "cashier can");

        cashier.transfer(amount);
         // transfer ETH to Player
        //allows the contract to receieve ether
    }

}
