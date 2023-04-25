import random

# import all classes from ./classes/index.py
from classes.index import *
import matplotlib.pyplot as plt
import numpy as np


def plot_lp_curve(lp, k):
    x_vals = np.linspace(0.01, lp.X_amount * 2, 1000)
    y_vals = k / x_vals
    plt.plot(x_vals, y_vals)
    plt.scatter(lp.X_amount, lp.Y_amount, color='red')
    plt.xlabel(lp.X_ticker)
    plt.ylabel(lp.Y_ticker)
    plt.title(f'X * Y = {k}')
    plt.ylim(0, 10000)
    plt.show()


# Define usd, eth and dai
usd = Usd()
eth = CryptoCurrency('Etherum', 'ETH', 2000)
dai = CryptoCurrency('Dai', 'DAI', 1)

# create a list of all currencies
currencies = [usd, eth, dai]

# Create a for loop that creates 4 traders with wallets for all currencies, where the first trader is a lp
traders = []
for i in range(100):
    wallets = []
    if i == 0:
        wallets.append(Wallet("usd0", usd, 1000))
        wallets.append(Wallet("eth0", eth, 1000))
        wallets.append(Wallet("dai0", dai, 1000))
        traders.append(LiquidityProvider(i, wallets))
    else:
        wallets.append(Wallet("usd"+str(i), usd, 1000))
        wallets.append(Wallet("eth"+str(i), eth, 1000))
        wallets.append(Wallet("dai"+str(i), dai,  1000))
        traders.append(Trader(i, wallets))

# Create a liquidity pool with 1000 ETH and 1000 DAI
lp = LiquidityPool(traders[0], 'ETH', 'DAI', 1000, 1000)

# Print the balances of all traders
for trader in traders:
    print(f"{trader}" + "Old")
    for wallet in trader.wallets:
        print(wallet.wallet_id, wallet.amount)
    print()

# Run a loop where trader without lp swaps either ETH or DAI for the other
for trader in traders[1:]:
    if trader.lp == False:
        if random.randint(0, 1) == 0:
            lp.trade(trader, 'ETH', random.randint(
                0, trader.wallets[1].amount))
        else:
            lp.trade(trader, 'DAI', random.randint(
                0, trader.wallets[2].amount))


# Print the balances of all traders
for trader in traders:
    print(trader)
    for wallet in trader.wallets:
        print(wallet.wallet_id, wallet.amount)
    print()

# print the liquidity pool
print(lp)
print("k value: ", lp.K_value)
# print liquidity pool fee_amount for x and y
print("fee_amount_x: ", lp.fee_amount_X)
print("fee_amount_y: ", lp.fee_amount_Y)

# Plot the lp curve
plot_lp_curve(lp, lp.K_value)

# liquidity provider widtraws 100% of the liquidity pool
lp.withdraw(traders[0], 1)

# Print the balances of liquidity provider
print(traders[0])
for wallet in traders[0].wallets:
    print(wallet.wallet_id, wallet.amount)
print()

# print the liquidity pool
print(lp)
print("k value: ", lp.K_value)
# print liquidity pool fee_amount for x and y
print("fee_amount_x: ", lp.fee_amount_X)
print("fee_amount_y: ", lp.fee_amount_Y)
