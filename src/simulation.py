
from trader import Trader, CEX, DEX, crypto_list

# Define the variables for the simulation
num_iterations = 100

# Define the trader strategy


def choose_exchange(trader):
    DEXoMeter = 0
    CEXoMeter = 0
    if any(x in trader.crypto_currency for x in crypto_list[4:10]):
        DEXoMeter += 1
    else:
        CEXoMeter += 1
    if trader.fees_concern < 50:
        DEXoMeter += 1
    else:
        CEXoMeter += 1
    if trader.speed_concern < 50:
        DEXoMeter += 1
    else:
        CEXoMeter += 1
    if trader.security_concern < 50:
        DEXoMeter += 1
    else:
        CEXoMeter += 1
    if trader.regulation_concern == "low":
        DEXoMeter += 1
    elif trader.regulation_concern == "medium":
        CEXoMeter += 1
    else:
        CEXoMeter += 1
    if DEXoMeter > CEXoMeter:
        return "DEX"
    else:
        return "CEX"


# Define the simulation function, where 1000 traders are created and they use choose_exchange to choose their exchange

def run_simulation():
    Dex = DEX()
    Cex = CEX()
    for i in range(num_iterations):
        trader = Trader(trader_id=i)
        exchange_choice = choose_exchange(trader)
        if exchange_choice == 'DEX':
            Dex.traders.append(trader)
        elif exchange_choice == 'CEX':
            Cex.traders.append(trader)
    print("DEX:", len(Dex.traders))
    print("CEX:", len(Cex.traders))


run_simulation()
