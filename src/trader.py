###### Inactive ######


import random

# create a list of top 10 cryptocurrencies
crypto_list = ['BTC', 'ETH', 'XRP', 'BCH',
               'LTC', 'EOS', 'XLM', 'ADA', 'TRX', 'XMR']


class Trader:
    def __init__(self, trader_id):
        self.trader_id = trader_id
        self.crypto_currency = [random.choice(
            crypto_list)]
        # self.capital = random.randint(1000, 10000)
        self.regulation_concern = ["low", "medium", "high"]
        self.security_concern = random.randint(0, 100)
        self.speed_concern = random.randint(0, 100)
        self.fees_concern = random.randint(0, 100)


class CEX:
    def __init__(self):
        self.crypto_currency = crypto_list[0:3]
        self.fees = 25
        self.speed = 75
        self.security = 25
        self.regulation = 90
        self.traders = []


class DEX:
    def __init__(self):
        self.crypto_currency = crypto_list
        self.fees = 75
        self.speed = 25
        self.security = 75
        self.regulation = 10
        self.traders = []
