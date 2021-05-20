import sqlite3
from sqlite3.dbapi2 import Cursor
from config import *
from alpaca_trade_api.rest import TimeFrame
import alpaca_trade_api as tradeapi
from datetime import date

connection = sqlite3.connect(DB_FILE)
connection.row_factory = sqlite3.Row

cursor = connection.cursor()

cursor.execute("""
    SELECT id FROM strategy WHERE name = 'opening_range_breakout'
""")

strategy_id = cursor.fetchone()['id']

cursor.execute("""
    SELECT symbol, name
    FROM stock
    JOIN stock_strategy ON stock_strategy.stock_id = stock.id
    WHERE stock_strategy.strategy_id = ?
""", (strategy_id,))

stocks = cursor.fetchall()
symbols = [stock['symbol'] for stock in stocks]

print(symbols)

api = tradeapi.REST(API_KEY, SECRET_KEY, base_url=PAPER_URL)

current_date = '2021-05-19'# date.today().isoformat()
start_minute_bar = f"{current_date} 13:30:00+00:00"
end_minute_bar = f"{current_date} 13:45:00+00:00"

for symbol in symbols:
    #minute_bats = api.polygon.historic_agg_v2(symbol, 1, 'minute', _from='2021-5-19', to='2021-5-19')
    minute_bars = api.get_bars(symbol, TimeFrame.Minute, current_date, current_date).df
    
    print(symbol)
    
    opening_range_mask = (minute_bars.index >= start_minute_bar) & (minute_bars.index < end_minute_bar)
    opening_range_bar = minute_bars.loc[opening_range_mask]
    print(opening_range_bar)
    opening_range_low = opening_range_bar['low'].min()
    opening_range_high = opening_range_bar['high'].max()
    opening_range = opening_range_high - opening_range_low

    print(opening_range_low)
    print(opening_range_high)
    print(opening_range)