pragma solidity ^0.5.10;

contract EtherWallet {
    mapping(address => uint256) public balances;
    
    event Deposit(address indexed sender, uint256 amount);
    event Withdrawal(address indexed recipient, uint256 amount);
    
    function deposit() public payable {
        require(msg.value > 0, "Value must be greater than 0");
        
        balances[msg.sender] += msg.value;
        emit Deposit(msg.sender, msg.value);
    }
    
    function withdraw(uint256 _amount) public {
        require(balances[msg.sender] >= _amount, "Insufficient balance");
        require(_amount > 0, "Amount must be greater than 0");
        
        balances[msg.sender] -= _amount;
        msg.sender.transfer(_amount);
        emit Withdrawal(msg.sender, _amount);
    }
    
    function getBalance() public view returns (uint256) {
        return balances[msg.sender];
    }
}