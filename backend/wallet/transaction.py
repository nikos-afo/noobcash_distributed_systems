import time
import uuid

from backend.wallet.wallet import Wallet
from backend.config import MINING_REWARD, MINING_REWARD_INPUT

class Transaction:
    
    #Katagrafi mias synallagis se nomisma apo kapoion se kapoion i kapoious allous

    def __init__(
        self,
        sender_wallet=None,
        recipient=None,
        amount=None,
        id=None,
        output=None,
        input=None
    ):
        self.id = id or str(uuid.uuid4())[0:8]
        self.output = output or self.create_output(
            sender_wallet,
            recipient,
            amount
        )
        self.input = input or self.create_input(sender_wallet, self.output)

    def create_output(self, sender_wallet, recipient, amount):
        
        #To paragomeno output autis tis synallagis
        
        if amount > sender_wallet.balance:
            raise Exception('Amount exceeds balance')

        output = {}
        output[recipient] = amount
        output[sender_wallet.address] = sender_wallet.balance - amount

        return output

    def create_input(self, sender_wallet, output):
        
        #To input autis tis synallagis
        #To stamping mias synallagis poy perilamvanei kai to dimosio kleidi kai tin dieuthinsi 
        
        return {
            'timestamp': time.time_ns(),
            'amount': sender_wallet.balance,
            'address': sender_wallet.address,
            'public_key': sender_wallet.public_key,
            'signature': sender_wallet.sign(output)
        }

    def update(self, sender_wallet, recipient, amount):
        """
        Update the transaction with an existing or new recipient.
        """
        if amount > self.output[sender_wallet.address]:
            raise Exception('Amount exceeds balance')

        if recipient in self.output:
            self.output[recipient] = self.output[recipient] + amount
        else:
            self.output[recipient] = amount

        self.output[sender_wallet.address] = \
            self.output[sender_wallet.address] - amount

        self.input = self.create_input(sender_wallet, self.output)

    def to_json(self):
        
        #H seiriseiopoiisi mias sinallagis 
    
        return self.__dict__

    @staticmethod
    def from_json(transaction_json):
        
        #H aposeiriopoiisi tou json arxeiou tis sinallagis piso se ena transaction instance   
        
        return Transaction(**transaction_json)

    @staticmethod
    def is_valid_transaction(transaction):
        
        #I epalitheusi mia sunallagis 
        #Exception xeirismou gia mi epalitheumenes synallages
        
        if transaction.input == MINING_REWARD_INPUT:
            if list(transaction.output.values()) != [MINING_REWARD]:
                raise Exception('Invalid mining reward')
            return

        output_total = sum(transaction.output.values())

        if transaction.input['amount'] != output_total:
            raise Exception('Invalid transaction output values')

        if not Wallet.verify(
            transaction.input['public_key'],
            transaction.output,
            transaction.input['signature']
        ):
            raise Exception('Invalid signature')

    @staticmethod
    def reward_transaction(miner_wallet):
        
        #Dimiourgia mias antamoivis gia ton miner
        
        output = {}
        output[miner_wallet.address] = MINING_REWARD

        return Transaction(input=MINING_REWARD_INPUT, output=output)

def main():
    transaction = Transaction(Wallet(), 'recipient', 15)
    print(f'transaction.__dict__: {transaction.__dict__}')

    transaction_json = transaction.to_json()
    restored_transaction = Transaction.from_json(transaction_json)
    print(f'restored_transaction.__dict__: {restored_transaction.__dict__}')

if __name__ == '__main__':
    main()