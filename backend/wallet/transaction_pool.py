
class TransactionPool:
    def __init__(self):
        self.transaction_map = {}

    def set_transaction(self, transaction):
        
        #Bazei tin sinallagi sto pool 
    
        self.transaction_map[transaction.id] = transaction


    def existing_transaction(self, address):
        
        #Vriskei mia synallagi poy dhmiourgithike apo mia dieythinsi sto pool 
        
        for transaction in self.transaction_map.values():
            if transaction.input['address'] == address:
                return transaction

    def transaction_data(self):
        
        #Epistrofi tis synallagis apo to pool se morfi seiriopoiisis json  
        
        return list(map(
            lambda transaction: transaction.to_json(),
            self.transaction_map.values()
        ))

    def clear_blockchain_transactions(self, blockchain):
        
        #Diagrafi ton synallagon poy katagrafikan sto blockcgain apo to pool
        
        for block in blockchain.chain:
            for transaction in block.data:
                try:
                    del self.transaction_map[transaction['id']]
                except KeyError:
                    pass