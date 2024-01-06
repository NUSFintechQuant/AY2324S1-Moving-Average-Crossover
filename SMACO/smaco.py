import yfinance as yf
import pandas as pd
from math import floor
from concurrent.futures import ProcessPoolExecutor

#stock_symbols = ['AAPL', 'MSFT', 'GOOGL']
#df = yf.download('GOOGL', period="6y")
def calculate_sma_crossover(df, short, long,starting_capital):

    # Calculate short-term and long-term SMAs
    long_sma = list(pd.Series(df).rolling(long).mean())
    short_sma = list(pd.Series(df).rolling(short).mean())
    
    # Initialize variables to track PNL and positions
    cash=starting_capital
    shares_bought=0
    position = None
    # Loop through the data to find SMA crossovers
    for i in range(1, len(df)):
        if short_sma[i] > long_sma[i] and short_sma[i - 1] <= long_sma[i - 1]:
            # Short-term SMA crosses above long-term SMA (Buy signal)
            position = df[i]
            shares_bought= floor(cash/position) #find out how many shares of stocks i can buy
            cash=cash-shares_bought*position #deduct from cash
        elif short_sma[i] < long_sma[i] and short_sma[i - 1] >= long_sma[i - 1]:
            # Short-term SMA crosses below long-term SMA (Sell signal)
            if position is not None:
                cash += (df[i])*shares_bought
            position = None # currenlty no position 
            shares_bought=0 #reset since i alr sell the shares
    # If there's an open position, calculate PNL assuming we hold until the latest date
    if position is not None:
        cash += (df[-1])*shares_bought
    
    return cash-starting_capital #return the pnl (final-start)

def optimise_sma(args):
    df, short_sma, long_sma, starting_capital = args
    cash = calculate_sma_crossover(df, short_sma, long_sma,starting_capital)
    return short_sma, long_sma, cash


def main(ticker, period, interval, starting_capital):
        #initialization
        df = list(yf.Ticker(ticker).history(period=period, interval=interval)['Close'])
        #start_time = time.time()

        short_sma_range = range(50, 201)
        long_sma_range = range(51, 201)
        
        
        num_processes = 4 # number of processes to run in parallel

        parameter_combinations = [(df, short, long, starting_capital) for short in short_sma_range for long in long_sma_range if short < long]

        with ProcessPoolExecutor(max_workers=num_processes) as pool:
            results = list(pool.map(optimise_sma, parameter_combinations))

        best_short_sma, best_long_sma, best_pnl = max(results, key=lambda x: x[2])

        #print(f"Timeframe: {interval}, Best SMA Pair: Short SMA = {best_short_sma}, Long SMA = {best_long_sma}, final_cash = {best_pnl}")
        #end_time = time.time()
        #elapsed_time = end_time - start_time
        #print(elapsed_time)
        return best_short_sma, best_long_sma, best_pnl

def best_pair_for_all(ticker, interval, capital):
    #ticker_list=['AAPL', 'MSFT', 'GOOGL']
    #interval_list = ['2m', '5m', '15m', '30m', '1h','1d'] #1 hour somehow doesnt work, check how it works
    starting_capital=100000
    #for interval in interval_list:
    period="6y" 
    if ("h" in interval): #yfinance cap to period
        period="730d"
    elif ("m" in interval): 
        period='60d'
            
        #main(ticker_list[2], period, interval, starting_capital)
    
    return main(ticker, period, interval, int(capital))
    
        
#best_pair_for_all('MSFT',1000000)