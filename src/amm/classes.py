###### Inactive ######
class Trader:
    def __init__(self, eth_balance, dai_balance):
        self.eth_balance = eth_balance
        self.dai_balance = dai_balance

    def buy_eth(self, eth_amount, dai_amount):
        if dai_amount <= self.dai_balance:
            self.dai_balance -= dai_amount
            self.eth_balance += eth_amount
            return True
        else:
            return False

    def sell_eth(self, eth_amount, dai_amount):
        if eth_amount <= self.eth_balance:
            self.eth_balance -= eth_amount
            self.dai_balance += dai_amount
            return True
        else:
            return False


class LiquidityPool:
    def __init__(self, eth_balance, dai_balance):
        self.eth_balance = eth_balance
        self.dai_balance = dai_balance
        self.k_value = self.eth_balance * self.dai_balance

    def calculate_dai_required_for_eth(self, eth_amount):
        return self.dai_balance - (self.eth_balance * self.dai_balance) / (self.eth_balance + eth_amount)

    def calculate_eth_required_for_dai(self, dai_amount):
        return self.eth_balance - (self.eth_balance * self.dai_balance) / (self.dai_balance + dai_amount)

    def execute_trade(self, eth_amount, dai_amount):
        self.eth_balance += eth_amount
        self.dai_balance += dai_amount
        return True


class LiquidityProvider:
    def __init__(self, eth_balance, dai_balance):
        self.eth_balance = eth_balance
        self.dai_balance = dai_balance

    def collect_fees(self, eth_fee, dai_fee):
        self.eth_balance += eth_fee
        self.dai_balance += dai_fee

# class for cryptocurrency, such as eth and dai
