########################################################################################################################################################################################
Proposal

Here at Project3Cyptogames we have a vision. A platform for the future of gambling on the internet free of centralized authority. In this utopia players would be free to bring their wealth of crypto and play casino games on our platform. Payments would be executed in smart contracts so as to make a completely fair and balanced gambling platform.

As this is a huge undertaking, our first attempt would be to create a decentralized app on streamlit to play blackjack and bet your etherium balance. The idea would be to create a solid foundation for our future casino by creating our first game online! Our team of four, Gino Petrosian, Ryan Stowers, Adrian Manlangit, and Michael Drinkard, worked tirelessly to create this app. Unfortunately due to time constraints we were not able to completely finish all the functionality of the app, we were able to create a smart contract, deploy the contract, and have the contract balance act as your balance in the blackjack game. Thus we were able to create our first step to creating our online casino.

########################################################################################################################################################################################
Files below are as follows

1) Blackjack Game PwrPnt.pptx - This is the Powerpoint for Group 3 Project 3
2) app.py - this is the python file our streamlit app operates
3) BlackjackFunctions.py - this is the python file we defined our dataclasses in.
4) contract.sol - this is the contract our solidity file is written as.
5) Archtecture_Project3.docx - this is the initial concept for the app functionality.
6) Compiled folder - this contains the compiled version of contract.sol
7) Resources folder - this contains all the .png files used to display cards on the app
8) pycache folder - I dunno what this contains, but I'm too afraid to delete it.

Below are the instructions required to deploy the app.
#########################################################################################################################################################################################
Step 1

Deploy the contract.sol file on remix, copy the contract address and paste it in the app.py file setting contract address to the correct address.

Step 2

Adjust the Path variable for the complied contract address to the correct path on your computer.

Step 3

Open Ganache

Step 4 

Run the app and play some Blackjack

##########################################################################################################################################################################################

Known bugs

1) Sometimes the card images don't path correctly in the blackjackfunctions.py file. Not sure why, but just adding Project3Cryptogames/ or removing it seems to fix the bug

2) There is a lag issue when running the app. Not sure whats causing it, but I believe it has something to do with the hashing our blockchain activities are doing.

##########################################################################################################################################################################################

Functionality to be added

1) There is no cashout feature at the moment

2) The contract balance is an int value of what your deposit, so its not changing the balance correctly at the moment.

##########################################################################################################################################################################################

References

1)  Michael Camdem-Smith at this url helped us create the functionality for this blackjack app. We adjusted the code to suit however, it was a fascinating look at how object oriented programming can be employed in game design

https://python.plainenglish.io/a-lesson-in-blackjack-and-python-hosted-by-streamlit-b927147bec8d
