# streamlit-lightweight-charts-ntf

This streamlit plugin uses a fork [ntf](https://github.com/ntf/lightweight-charts) of `lightweight-charts`.
It augments the [lightweight-charts](https://tradingview.github.io/lightweight-charts/) with an effective multipane experience.

The [ntf](https://github.com/ntf/lightweight-charts) fork is frozen in an old version, there are no further developments, and no further updates - it is a `AS IT IS`situation.
Although it seems very stable and very useful for financial and trading Data Science. It has an extra option `pane` that:

 - Aligns panes - by width
 - synchronises panes mouse moves
 - synchronises the hair-cross cursor between charts

Documentation
- [Features Demo](https://www.tradingview.com/lightweight-charts/)
- [Documentation](https://tradingview.github.io/lightweight-charts/)
- [GitHub](https://github.com/tradingview/lightweight-charts)
- [Use example](https://jsfiddle.net/adrianntf/6qea5ytv/)

A nice example from DeKay on how to use:
- [GitHub](https://github.com/karthik947/PlotIndicators)
- [Youtube #1](https://www.youtube.com/watch?v=NlHjhmIe1EI)
- [Youtube #2](https://www.youtube.com/watch?v=2nxj4aLBhgo)

## How to install:
```
python -m pip install streamlit-lightweight-charts-ntf
```

## How to use:
```python
from streamlit_lightweight_charts_ntf import renderLightweightCharts

renderLightweightCharts(charts: <List of Dicts> , key: <str>)
```

### API
- charts: `<List of Dicts>`

    - [chart](https://tradingview.github.io/lightweight-charts/docs/api/interfaces/ChartOptions): `<Dict>`

    - [series](https://tradingview.github.io/lightweight-charts/docs/series-types): `<List of Dicts>`

        - [type](https://tradingview.github.io/lightweight-charts/docs/series-types): `<str-enum>`
            [ Area, Bar, Baseline, Candlestick, Histogram, Line ]

        - data: `<List of Dicts>` accordingly to series type

        - options: `<Dict>` with style options

        - priceScale: `<Dict>` optional

        - markers: `<List of Dicts>` optional

- key: `<str>` when creating multiple charts in one page

### The extra option: `pane`
In the example below you will notice the option `pane` that is used to group charts 

---
<br />

![Multi Pane Chart with Pandas](https://github.com/freyastreamlit/streamlit-lightweight-charts-ntf/blob/main/examples/MultiPaneChartsWithPandas.png?raw=true)

```python
import streamlit as st
from streamlit_lightweight_charts_ntf import renderLightweightCharts

import json
import numpy as np
import yfinance as yf
import pandas as pd
import pandas_ta as ta

COLOR_BULL = 'rgba(38,166,154,0.9)' # #26a69a
COLOR_BEAR = 'rgba(239,83,80,0.9)'  # #ef5350

def dataToJSON(df, column, slice=0, color=None):
    data = df[['time', column, 'color']].copy()
    data = data.rename(columns={column: "value"})
    if(color == None):
        data.drop('color', axis=1)
    elif(color != 'default'):
        data['color'] = color
    if(slice > 0):
        data = data.iloc[slice:,:]
    return json.loads(data.to_json(orient = "records"))

# Request historic pricing data via finance.yahoo.com API
df = yf.Ticker('AAPL').history(period='9mo')[['Open', 'High', 'Low', 'Close', 'Volume']]

# Some data wrangling to match required format
df = df.reset_index()
df.columns = ['time','open','high','low','close','volume']                  # rename columns
df['time'] = df['time'].dt.strftime('%Y-%m-%d')                             # Date to string

# indicators
df.ta.macd(close='close', fast=6, slow=12, signal=5, append=True)           # calculate macd
df.ta.ema(close='close', length=14, offset=None, append=True)               # EMA fast
df.ta.sma(close='close', length=60, offset=None, append=True)               # SMA slow
df.ta.rsi(close='close', length=14, offset=None, append=True)               # RSI - momentum oscillator
df['VOL_BID'] = -df['volume'].sample(frac=1).values                         # shuffle and negate volume values

# export to JSON format
df['color'] = np.where(  df['open'] > df['close'], COLOR_BEAR, COLOR_BULL)  # bull or bear
candles = json.loads(df.to_json(orient = "records"))
sma_slow = dataToJSON(df,"SMA_60", 60, 'blue')
ema_fast = dataToJSON(df, "EMA_14", 14, 'orange')
vol_ASK = dataToJSON(df,'volume', 0, COLOR_BULL)
vol_BID = dataToJSON(df,'VOL_BID', 0, COLOR_BEAR)
rsi = dataToJSON(df,'RSI_14', 14, 'purple')
macd_fast = dataToJSON(df, "MACDh_6_12_5", 0, 'orange')
macd_slow = dataToJSON(df, "MACDs_6_12_5", 0, 'blue')
df['color'] = np.where(  df['MACD_6_12_5'] > 0, COLOR_BULL, COLOR_BEAR)     # MACD histogram color
macd_hist = dataToJSON(df, "MACD_6_12_5")

chartMultipaneOptions = [
    {
        "width": 600,
        "height": 600,
        "layout": {
            "background": {
                "type": "solid",
                "color": 'white'
            },
            "textColor": "black"
        },
        "grid": {
            "vertLines": {
                "color": "rgba(197, 203, 206, 0.5)"
                },
            "horzLines": {
                "color": "rgba(197, 203, 206, 0.5)"
            }
        },
        "priceScale": {
            "borderColor": "rgba(197, 203, 206, 0.8)"
        },
        "timeScale": {
            "borderColor": "rgba(197, 203, 206, 0.8)",
            "barSpacing": 10,
            "minBarSpacing": 8
        }
    }
]

seriesMultipaneChart = [
    {
        "type": 'Candlestick',
        "data": candles,
        "options": {
            "upColor": COLOR_BULL,
            "downColor": COLOR_BEAR,
            "borderVisible": False,
            "wickUpColor": COLOR_BULL,
            "wickDownColor": COLOR_BEAR,
            "pane": 0
        }
    },
    {
        "type": 'Line',
        "data": sma_slow,
        "options": {
            "color": 'blue',
            "lineWidth": 2,
            "pane": 0
        }
    },
    {
        "type": 'Line',
        "data": ema_fast,
        "options": {
            "color": 'green',
            "lineWidth": 2,
            "pane": 0
        }
    },
    {
        "type": 'Histogram',
        "data": vol_ASK,
        "options": {
            "priceFormat": {
                "type": 'volume',
            },
            "pane": 1

        }
    },
    {
        "type": 'Histogram',
        "data": vol_BID,
        "options": {
            "priceFormat": {
                "type": 'volume',
            },
            "pane": 1

        }
    },
    {
        "type": 'Line',
        "data": rsi,
        "options": {
            "lineWidth": 2,
            "pane": 2
        }
    },
    {
        "type": 'Line',
        "data": macd_fast,
        "options": {
            "lineWidth": 2,
            "pane": 3
        }
    },
    {
        "type": 'Line',
        "data": macd_slow,
        "options": {
            "lineWidth": 2,
            "pane": 3
        }
    },
    {
        "type": 'Histogram',
        "data": macd_hist,
        "options": {
            "lineWidth": 1,
            "pane": 3
        }
    }
]

st.subheader("Multipane Chart with Pandas")

renderLightweightCharts([
    {
        "chart": chartMultipaneOptions[0],
        "series": seriesMultipaneChart
    }
], 'multipane')
```
