
from trader import Trader, CEX, DEX, crypto_list

# Define the variables for the simulation
num_iterations = 10000

# Define the trader strategy


def choose_exchange(trader):
    if any(x in trader.crypto_currency for x in crypto_list[4:10]):
        return "DEX"
    else:
        return "CEX"


# Define the simulation function, where 1000 traders are created and they use choose_exchange to choose their exchange

def run_simulation():
    Dex = 0
    Cex = 0
    for i in range(num_iterations):
        trader = Trader()
        exchange_choice = choose_exchange(trader)
        if exchange_choice == 'DEX':
            Dex += 1
        elif exchange_choice == 'CEX':
            Cex += 1
    print("DEX:", Dex)
    print("CEX:", Cex)


run_simulation()
