# AY2324S1-Moving-Average-Crossover

A brief description of your project.

## Getting Started

The moving average crossover trading strategy sports many pair values, most famously the 50 and 200 simple moving average (SMA) pair values. But how would other pair values perform? How about Exponential moving averages (EMA) or Volume weighted moving averages (VWMA)? This project was designed to address these investment considerations.

The Repository contains two files "SMACO_optimised.py" which is the teams key deliverable as explained in the markdown below, and "Test.py", a work in progress of the adoption of our code to a paper trading account.

## Requirements

- Python 3.x
- `yfinance` library
- `pandas` library
- `concurrent.futures` module

Install the required libraries using:

```bash
pip install yfinance pandas
```

## Usage

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sma-crossover-optimization.git
cd sma-crossover-optimization
```

2. Run the script
```python
python sma_optimization.py
```

## Explanation
The script defines two main functions:

calculate_sma_crossover: Calculates the final cash position after executing an SMA crossover trading strategy.
optimise_sma: Takes a set of parameters (short SMA, long SMA, data, starting capital) and returns the corresponding final cash position.
The main function downloads historical stock data, initializes parameter ranges for short and long SMAs, and runs the optimization process using parallel processing for faster execution.

The best_pair_for_all function iterates over a list of stock tickers and time intervals, calling the main function for each combination.

## Results
The script prints the best SMA pair (short SMA, long SMA) and the final cash position for each specified stock ticker and time interval.

## Presentation Slides
[SMACO Presentation Slides](SMACO-Final-Presentation-Slides.pdf)

## Disclaimer
This script is for educational purposes only and does not constitute financial advice. Use the information at your own risk, and always conduct thorough research or consult with a financial advisor before making investment decisions.

## Acknowledgements

This project is made possible by the Simple Moving Average Crossover (SMACO) team for AY23/24 S1.
