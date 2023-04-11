import random
from classes import Trader, LiquidityProvider, LiquidityPool
import matplotlib.pyplot as plt
import numpy as np


def plot_lp_curve(lp, k):
    x_vals = np.linspace(0.01, lp.eth_balance * 2, 1000)
    y_vals = k / x_vals
    plt.plot(x_vals, y_vals)
    plt.scatter(lp.eth_balance, lp.dai_balance, color='red')
    plt.xlabel('ETH')
    plt.ylabel('DAI')
    plt.title(f'X * Y = {k}')
    plt.ylim(0, 10000)
    plt.show()


# Set initial balances
lp_initial_eth_balance = 100
lp_initial_dai_balance = 1000

lp = LiquidityProvider(lp_initial_eth_balance / 2, lp_initial_dai_balance / 2)
pool = LiquidityPool(lp_initial_eth_balance / 2, lp_initial_dai_balance / 2)

num_traders = 10
traders = []

for i in range(num_traders):
    traders.append(Trader(1, 1000))

# Set trading fee and liquidity provider fee
trading_fee = 0.003
lp_fee = 0.002

# Run simulation
for i in range(1000):
    # Determine current ETH price in DAI
    eth_reserve = pool.eth_balance
    dai_reserve = pool.dai_balance
    eth_price = dai_reserve / eth_reserve

    for j, trader in enumerate(traders):
        # Determine whether trader wants to buy or sell ETH
        buy_eth = random.choice([True, False])

        if buy_eth:
            # Determine amount of ETH to buy
            eth_amount = random.uniform(0.01, 0.1)
            dai_amount = eth_amount * eth_price / (1 - trading_fee)

            # Check if trader has enough DAI to buy ETH
            if trader.buy_eth(eth_amount, dai_amount):
                # Execute trade with liquidity pool
                pool.execute_trade(-eth_amount, dai_amount)

                # Calculate trading fees and liquidity provider fees
                trading_fees = dai_amount * trading_fee
                lp_fees = dai_amount * lp_fee
                trader.dai_balance -= trading_fees
                lp.collect_fees(eth_amount * lp_fee, lp_fees)
            else:
                # Trader does not have enough DAI, skip trade
                pass
        else:
            # Determine amount of ETH to sell
            eth_amount = random
            eth_amount = random.uniform(0.01, 0.1)
            dai_amount = eth_amount * eth_price * (1 - trading_fee)

        # Check if trader has enough ETH to sell
        if trader.sell_eth(eth_amount, dai_amount):
            # Execute trade with liquidity pool
            pool.execute_trade(eth_amount, -dai_amount)

            # Calculate trading fees and liquidity provider fees
            trading_fees = eth_amount * trading_fee
            lp_fees = eth_amount * lp_fee
            trader.eth_balance -= trading_fees / eth_price
            lp.collect_fees(lp_fees, dai_amount * lp_fee)
        else:
            # Trader does not have enough ETH, skip trade
            pass

# Check if liquidity pool is still in balance
required_dai = pool.calculate_dai_required_for_eth(
    lp.eth_balance - lp_initial_eth_balance / 2)
required_eth = pool.calculate_eth_required_for_dai(
    lp.dai_balance - lp_initial_dai_balance / 2)
if required_dai < 0:
    pool.execute_trade(required_eth, required_dai)
elif required_eth < 0:
    pool.execute_trade(required_eth, required_dai)

print("Liquidity pool ETH balance:", pool.eth_balance)
print("Liquidity pool DAI balance:", pool.dai_balance)
print("Liquidity provider ETH balance:", lp.eth_balance)
print("Liquidity provider DAI balance:", lp.dai_balance)
for j, trader in enumerate(traders):
    print("Trader", j + 1, "ETH balance:", trader.eth_balance)
    print("Trader", j + 1, "DAI balance:", trader.dai_balance)


plot_lp_curve(pool, lp_initial_eth_balance/2*lp_initial_dai_balance/2)
