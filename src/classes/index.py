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
    def __init__(self, trader_id, wallets=[], lp=False):
        self.trader_id = trader_id
        self.wallets = wallets
        self.lp = lp
        # need to add preferences towards CEX or DEX

    def __repr__(self):
        return f"{self.trader_id}:"


class LiquidityProvider(Trader):
    def __init__(self, trader_id, wallets=[]):
        super().__init__(trader_id, wallets, lp=True)

    def __repr__(self):
        return f"{self.trader_id}:"


class LiquidityPool:
    def __init__(self, trader, X_ticker, Y_ticker, X_amount, Y_amount, fee=0.003):
        self.X_ticker = X_ticker
        self.Y_ticker = Y_ticker
        self.X_amount = X_amount
        # withdraw x_amount from trader wallet
        for wallet in trader.wallets:
            if wallet.crypto_currency.ticker == X_ticker:
                wallet.amount -= X_amount
        self.Y_amount = Y_amount
        # withdraw y_amount from trader wallet
        for wallet in trader.wallets:
            if wallet.crypto_currency.ticker == Y_ticker:
                wallet.amount -= Y_amount
        self.K_value = X_amount * Y_amount  # K_value is a constant
        # Could make it easier to calculate by using X_value = y_amount / x_amount
        self.X_value = Y_amount/X_amount
        # Could make it easier to calculate by using y_value = x_amount / y_amount
        self.Y_value = X_amount/Y_amount
        self.fee = fee  # fee is a constant, and will be a precentage of swap_inn_amount
        self.fee_amount_X = 0
        self.fee_amount_Y = 0

    def trade(self, trader, swap_inn_ticker, inn_amount):
        # Check if trader has enough of swap_inn_ticker
        for wallet in trader.wallets:
            if wallet.crypto_currency.ticker == swap_inn_ticker:
                if wallet.amount < inn_amount:
                    return False

        # Find fee amount
        fee_amount = inn_amount * self.fee

        # Find amount of swap_out_ticker
        if swap_inn_ticker == self.X_ticker:
            swap_out_ticker = self.Y_ticker
            swap_out_amount = self.Y_amount - \
                (self.K_value / (self.X_amount + inn_amount - fee_amount))
        else:
            swap_out_ticker = self.X_ticker
            swap_out_amount = self.X_amount - (
                self.K_value / (self.Y_amount + inn_amount - fee_amount))

        # Update liquidity pool X and Y amounts
        if swap_inn_ticker == self.X_ticker:
            self.X_amount += inn_amount
            self.Y_amount -= swap_out_amount

        else:
            self.X_amount -= swap_out_amount
            self.Y_amount += inn_amount

        # Update liquidity pool x and y values
        self.X_value = self.Y_amount / self.X_amount
        self.Y_value = self.X_amount / self.Y_amount

        # Update liquidity pool k value
        self.K_value = self.X_amount * self.Y_amount

        # Update fee amounts
        if swap_inn_ticker == self.X_ticker:
            self.fee_amount_X += fee_amount
        else:
            self.fee_amount_Y += fee_amount

        # Update trader wallet
        for wallet in trader.wallets:
            if wallet.crypto_currency.ticker == swap_inn_ticker:
                wallet.amount -= inn_amount
            elif wallet.crypto_currency.ticker == swap_out_ticker:
                wallet.amount += swap_out_amount

    # Function for lp to withdraw X and Y from liquidity pool
    def withdraw(self, trader, percent):
        # Check if trader is lp
        if trader.lp == False:
            return False

        # Find amount to withdraw
        withdraw_X_amount = self.X_amount * percent
        withdraw_Y_amount = self.Y_amount * percent

        # Update liquidity pool X and Y amounts
        self.X_amount -= withdraw_X_amount
        self.Y_amount -= withdraw_Y_amount

        if percent == 1:
            self.fee_amount_X = 0
            self.fee_amount_Y = 0
            # Update liquidity pool x and y values to 0
            self.X_value = 0
            self.Y_value = 0
            self.K_value = 0

        else:
            self.fee_amount_X -= self.fee_amount_X * percent
            self.fee_amount_Y -= self.fee_amount_Y * percent
            # Update liquidity pool x and y values
            self.X_value = self.Y_amount / self.X_amount
            self.Y_value = self.X_amount / self.Y_amount

            # Update liquidity pool k value
            self.K_value = self.X_amount * self.Y_amount

        # Update trader wallet
        for wallet in trader.wallets:
            if wallet.crypto_currency.ticker == self.X_ticker:
                wallet.amount += withdraw_X_amount
            elif wallet.crypto_currency.ticker == self.Y_ticker:
                wallet.amount += withdraw_Y_amount

    def __repr__(self):
        return f"{self.X_ticker}/{self.Y_ticker}: {self.X_amount} {self.X_ticker} and {self.Y_amount} {self.Y_ticker}"
