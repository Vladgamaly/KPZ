import numpy as np
import matplotlib.pyplot as plt

class Signal:
    def __init__(self, side: str, entry: float, take_profit: float, stop_loss: float):
        self.side = side
        self.entry = entry
        self.take_profit = take_profit
        self.stop_loss = stop_loss
        self.result = 0.0

class Strategy:
    def generate_fake_data(self):
        return np.random.random()

    def create_signal(self, df):
        if df > 0.5:
            return Signal("BUY", 100.0, 110.0, 90.0)
        else:
            return Signal("SELL", 100.0, 90.0, 110.0)

class Backtester:
    def __init__(self, strategy: Strategy, initial_balance: float = 10000.0):
        self.strategy = strategy
        self.signals = []
        self.profit = 0.0
        self.balance = initial_balance
        self.trades = []
        self.win_count = 0
        self.loss_count = 0

    def run_backtest(self, n_iterations: int = 100):
        balance_history = [self.balance] 
        for _ in range(n_iterations):
            df = self.strategy.generate_fake_data()
            signal = self.strategy.create_signal(df)
            if signal:
                self.signals.append(signal)
                result = self.simulate_trade(signal)
                self.balance += result  
                balance_history.append(self.balance) 
                signal.result = result
                if result > 0:
                    self.win_count += 1
                elif result < 0:
                    self.loss_count += 1
                self.trades.append(result)

        self.plot_balance(balance_history) 

    def simulate_trade(self, signal: Signal) -> float:
        if signal.side == "BUY":
            final_price = signal.entry * np.random.uniform(0.95, 1.05)
        else:  
            final_price = signal.entry * np.random.uniform(0.95, 1.05)

        if (signal.side == "BUY" and final_price >= signal.take_profit) or \
           (signal.side == "SELL" and final_price <= signal.take_profit):
            return abs(signal.take_profit - signal.entry)
        elif (signal.side == "BUY" and final_price <= signal.stop_loss) or \
             (signal.side == "SELL" and final_price >= signal.stop_loss):
            return -abs(signal.entry - signal.stop_loss)
        else:
            return 0.0

    def summary(self):
        print(f"Total signals: {len(self.signals)}")
        print(f"Total profit: {round(self.profit, 2)}")
        print(f"Win rate: {self.win_count / len(self.trades) * 100:.2f}%")
        print(f"Loss rate: {self.loss_count / len(self.trades) * 100:.2f}%")
        if self.loss_count > 0:
            profit_factor = sum([t for t in self.trades if t > 0]) / abs(sum([t for t in self.trades if t < 0]))
            print(f"Profit factor: {profit_factor:.2f}")

    def plot_balance(self, balance_history):
        plt.plot(balance_history)
        plt.xlabel('Iterations')
        plt.ylabel('Balance')
        plt.title('Balance Change During Backtesting')
        plt.show()

strategy = Strategy()
backtester = Backtester(strategy)
backtester.run_backtest(100)
backtester.summary()
