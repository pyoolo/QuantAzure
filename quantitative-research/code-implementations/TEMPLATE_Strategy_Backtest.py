"""
Template: Quantitative Strategy Backtest Framework

This template provides a basic structure for implementing and backtesting
a quantitative trading strategy.

Author: [Your Name]
Date: [YYYY-MM-DD]
Description: [Brief description of the strategy]
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# 1. DATA LOADING AND PREPARATION
# =============================================================================

class DataManager:
    """Manage historical price data and prepare it for analysis."""

    def __init__(self, data_path=None):
        """
        Initialize DataManager.

        Parameters:
        -----------
        data_path : str
            Path to CSV file with historical data
        """
        self.data = None
        if data_path:
            self.load_data(data_path)

    def load_data(self, data_path):
        """Load data from CSV file."""
        self.data = pd.read_csv(data_path, parse_dates=['Date'], index_col='Date')
        self.data = self.data.sort_index()
        print(f"Data loaded: {len(self.data)} observations from {self.data.index[0]} to {self.data.index[-1]}")

    def prepare_features(self):
        """Calculate technical indicators and features for the strategy."""
        # Example: Calculate Simple Moving Averages
        self.data['SMA_20'] = self.data['Close'].rolling(window=20).mean()
        self.data['SMA_50'] = self.data['Close'].rolling(window=50).mean()

        # Example: Calculate momentum indicator
        self.data['Momentum'] = self.data['Close'] - self.data['Close'].shift(10)

        # Example: Calculate volatility (20-day rolling std)
        self.data['Volatility'] = self.data['Close'].rolling(window=20).std()

        # Add more features as needed for your strategy
        return self.data


# =============================================================================
# 2. STRATEGY LOGIC
# =============================================================================

class QuantitativeStrategy:
    """
    Base class for quantitative trading strategy.

    This template generates buy/sell signals based on a set of rules.
    """

    def __init__(self, data, initial_capital=100000, position_size=0.95):
        """
        Initialize the strategy.

        Parameters:
        -----------
        data : pd.DataFrame
            DataFrame with OHLCV data and calculated features
        initial_capital : float
            Starting capital in dollars
        position_size : float
            Fraction of capital to deploy per trade (0-1)
        """
        self.data = data.copy()
        self.initial_capital = initial_capital
        self.position_size = position_size
        self.signals = pd.DataFrame(index=data.index)
        self.trades = []
        self.performance = None

    def generate_signals(self):
        """
        Generate buy/sell signals based on strategy rules.

        Returns:
        --------
        signals : pd.Series
            1 = Buy signal, -1 = Sell signal, 0 = No signal
        """
        # Example Strategy: SMA Crossover
        # Buy when SMA20 crosses above SMA50
        # Sell when SMA20 crosses below SMA50

        self.signals['position'] = 0  # 0 = flat, 1 = long, -1 = short

        # Check if SMAs are available
        if 'SMA_20' not in self.data.columns or 'SMA_50' not in self.data.columns:
            print("Warning: Required moving averages not found. Generating signals anyway.")
            self.signals['position'] = 0
            return

        # SMA Crossover Logic
        sma_cross = (self.data['SMA_20'] > self.data['SMA_50']).astype(int)
        self.signals['position'] = sma_cross  # 1 if bullish, 0 if bearish

        # Identify signal changes
        self.signals['signal'] = self.signals['position'].diff()
        self.signals['signal'] = self.signals['signal'].fillna(0)

        print(f"Generated {len(self.signals[self.signals['signal'] != 0])} signals")

    def backtest(self, commission=0.001, slippage=0.0005):
        """
        Run backtest with the generated signals.

        Parameters:
        -----------
        commission : float
            Commission per trade (as decimal, e.g., 0.001 = 0.1%)
        slippage : float
            Slippage per trade (as decimal, e.g., 0.0005 = 0.05%)

        Returns:
        --------
        portfolio_value : pd.Series
            Daily portfolio values
        """
        self.data['returns'] = self.data['Close'].pct_change()

        portfolio_value = pd.Series(index=self.data.index, dtype=float)
        position = 0  # Current position (-1: short, 0: flat, 1: long)
        cash = self.initial_capital
        trades = []

        for date_idx, (idx, row) in enumerate(self.data.iterrows()):
            if date_idx == 0:
                portfolio_value.iloc[date_idx] = self.initial_capital
                continue

            # Check for signals
            if self.signals.loc[idx, 'signal'] != 0:
                signal = int(self.signals.loc[idx, 'signal'])

                # Exit current position if needed
                if position != 0:
                    exit_price = self.data.loc[idx, 'Close'] * (1 - slippage * np.sign(position))
                    cash += position * exit_price
                    trades.append({
                        'exit_date': idx,
                        'exit_price': exit_price,
                        'position': position
                    })
                    position = 0

                # Enter new position if signal is non-zero
                if signal != 0:
                    entry_price = self.data.loc[idx, 'Close'] * (1 + slippage * np.sign(signal))
                    position = int(cash * self.position_size / entry_price) * np.sign(signal)
                    cash -= position * entry_price
                    trades.append({
                        'entry_date': idx,
                        'entry_price': entry_price,
                        'position': position
                    })

            # Calculate daily portfolio value
            position_value = position * self.data.loc[idx, 'Close']
            portfolio_value.iloc[date_idx] = cash + position_value

        self.portfolio_value = portfolio_value
        self.position_history = position
        self.trades = trades

        return portfolio_value

    def calculate_metrics(self):
        """Calculate performance metrics."""
        returns = self.portfolio_value.pct_change()

        # Basic metrics
        total_return = (self.portfolio_value.iloc[-1] / self.portfolio_value.iloc[0]) - 1
        annual_return = (1 + total_return) ** (252 / len(self.portfolio_value)) - 1
        annual_volatility = returns.std() * np.sqrt(252)
        sharpe_ratio = annual_return / annual_volatility if annual_volatility > 0 else 0
        max_drawdown = (self.portfolio_value.cummax() - self.portfolio_value) / self.portfolio_value.cummax()
        max_drawdown = max_drawdown.max()

        self.metrics = {
            'Total Return': f"{total_return:.2%}",
            'Annual Return': f"{annual_return:.2%}",
            'Annual Volatility': f"{annual_volatility:.2%}",
            'Sharpe Ratio': f"{sharpe_ratio:.2f}",
            'Max Drawdown': f"{max_drawdown:.2%}",
            'Number of Trades': len([t for t in self.trades if 'entry_date' in t])
        }

        return self.metrics


# =============================================================================
# 3. VISUALIZATION
# =============================================================================

class StrategyVisualizer:
    """Visualize strategy performance and signals."""

    @staticmethod
    def plot_strategy_performance(data, portfolio_value, signals, figsize=(15, 8)):
        """
        Plot strategy performance with buy/sell signals.

        Parameters:
        -----------
        data : pd.DataFrame
            Original price data
        portfolio_value : pd.Series
            Daily portfolio values
        signals : pd.DataFrame
            Buy/sell signals
        figsize : tuple
            Figure size
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize, sharex=True)

        # Plot 1: Price and Signals
        ax1.plot(data.index, data['Close'], label='Close Price', linewidth=2)

        # Mark buy signals
        buy_signals = signals[signals['signal'] == 1]
        ax1.scatter(buy_signals.index, data.loc[buy_signals.index, 'Close'],
                   marker='^', color='green', s=100, label='Buy Signal', zorder=5)

        # Mark sell signals
        sell_signals = signals[signals['signal'] == -1]
        ax1.scatter(sell_signals.index, data.loc[sell_signals.index, 'Close'],
                   marker='v', color='red', s=100, label='Sell Signal', zorder=5)

        ax1.set_title('Strategy Signals', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Price ($)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Plot 2: Portfolio Value
        ax2.plot(portfolio_value.index, portfolio_value, label='Portfolio Value',
                linewidth=2, color='blue')
        ax2.fill_between(portfolio_value.index, portfolio_value, alpha=0.3)
        ax2.set_title('Portfolio Performance', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Portfolio Value ($)')
        ax2.set_xlabel('Date')
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        return fig


# =============================================================================
# 4. MAIN EXECUTION
# =============================================================================

def main():
    """Execute strategy backtest."""

    print("=" * 70)
    print("QUANTITATIVE STRATEGY BACKTEST")
    print("=" * 70)

    # Step 1: Load and prepare data
    print("\n[1] Loading data...")
    data_manager = DataManager()

    # Note: Replace with your actual data path
    # Example: data_manager.load_data('price_data.csv')
    print("   (Using sample data generation mode)")

    # Generate sample data for demonstration
    dates = pd.date_range('2020-01-01', '2023-12-31', freq='D')
    sample_data = pd.DataFrame({
        'Close': 100 + np.cumsum(np.random.randn(len(dates)) * 2),
        'High': 102 + np.cumsum(np.random.randn(len(dates)) * 2),
        'Low': 98 + np.cumsum(np.random.randn(len(dates)) * 2),
        'Volume': np.random.randint(1000000, 5000000, len(dates))
    }, index=dates)

    data_manager.data = sample_data
    print(f"   Loaded: {len(sample_data)} observations from {dates[0].date()} to {dates[-1].date()}")

    # Step 2: Prepare features
    print("\n[2] Preparing features...")
    data = data_manager.prepare_features()
    print(f"   Features calculated: {list(data.columns)}")

    # Step 3: Initialize and run strategy
    print("\n[3] Running backtest...")
    strategy = QuantitativeStrategy(data, initial_capital=100000, position_size=0.95)
    strategy.generate_signals()
    strategy.backtest(commission=0.001, slippage=0.0005)

    # Step 4: Calculate metrics
    print("\n[4] Calculating performance metrics...")
    metrics = strategy.calculate_metrics()
    print("\nStrategy Performance Metrics:")
    for key, value in metrics.items():
        print(f"   {key}: {value}")

    # Step 5: Visualize results
    print("\n[5] Visualizing results...")
    visualizer = StrategyVisualizer()
    fig = visualizer.plot_strategy_performance(
        data,
        strategy.portfolio_value,
        strategy.signals
    )
    plt.savefig('backtest_results.png', dpi=300, bbox_inches='tight')
    print("   Results saved to 'backtest_results.png'")

    print("\n" + "=" * 70)
    print("BACKTEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
