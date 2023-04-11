class CryptoCurrency:
    def __init__(self, name, ticker, market_price):
        self.name = name
        self.ticker = ticker
        self.market_price = market_price


class Usd(CryptoCurrency):
    def __init__(self):
        super().__init__("USD", "USD", 1)


class Wallet:
    def __init__(self, wallet_id, crypto_currency, amount):
        self.wallet_id = wallet_id
        self.crypto_currency = crypto_currency
        self.amount = amount

    def __repr__(self):
        return f"{self.wallet_id}: {self.crypto_currency}"


class Trader:
    def _init_(self, trader_id, wallets=[Wallet], lp=False):
        self.trader_id = trader_id
        self.wallets = wallets
        self.lp = lp
        # need to add preferences towards CEX or DEX


class liquidityProvider(Trader):
    def _init_(self, trader_id, wallets=[Wallet]):
        super()._init_(trader_id, wallets, lp=True)


class liquidityPool:
    def _init_(self, X_ticker, Y_ticker, X_amount, Y_amount, X_value, Y_value):
        self.X_ticker = X_ticker
        self.Y_ticker = Y_ticker
        self.X_amount = X_amount
        self.Y_amount = Y_amount
        self.K_value = X_amount * Y_amount  # K_value is a constant
        # When initalized, X_value is the market price of X_ticker or what the lp is willing to pay for X_ticker
        self.X_value = X_value
        # When initalized, Y_value is the market price of Y_ticker or what the lp is willing to pay for Y_ticker
        self.Y_value = Y_value

    def trade(self, trader, buy_ticker, sell_ticker, trade_amount):
        # Find the current market price of the buy and sell tickers
        if buy_ticker == self.X_ticker:
            buy_price = self.X_value
            sell_price = self.Y_value
        else:
            buy_price = self.Y_value
            sell_price = self.X_value

        # Determine the amount of buy and sell tickers the trader has in their wallet
        for wallet in trader.wallets:
            if wallet.crypto_currency.ticker == buy_ticker:
                buy_wallet = wallet
            elif wallet.crypto_currency.ticker == sell_ticker:
                sell_wallet = wallet

        # Calculate the new amounts of buy and sell tickers in the liquidity pool after the trade
        new_buy_amount = self.X_amount if buy_ticker == self.X_ticker else self.Y_amount
        new_sell_amount = self.Y_amount if buy_ticker == self.X_ticker else self.X_amount
        new_buy_amount += trade_amount
        new_sell_amount = self.K_value / new_buy_amount

        # Calculate the new amounts of buy and sell tickers in the trader's wallet after the trade
        new_buy_wallet_amount = buy_wallet.amount - trade_amount
        new_sell_wallet_amount = sell_wallet.amount + \
            (sell_wallet.crypto_currency.market_price * trade_amount / sell_price)

        # Update the liquidity pool and trader's wallet with the new amounts
        if buy_ticker == self.X_ticker:
            self.X_amount = new_buy_amount
            self.Y_amount = new_sell_amount
            buy_wallet.amount = new_buy_wallet_amount
            sell_wallet.amount = new_sell_wallet_amount
