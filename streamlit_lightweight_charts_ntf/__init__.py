import os
from typing import Dict
from enum import Enum
import streamlit.components.v1 as components

_COMPONENT_NAME = "streamlit_lightweight_charts_ntf"
_RELEASE = True

class Chart(str, Enum):
    Area = 'addAreaSeries'
    Baseline = 'addBaselineSeries'
    Histogram = 'addHistogramSeries'
    Line = 'addLineSeries'
    Bar = 'addBarSeries'
    Candlestick = 'addCandlestickSeries'

parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "frontend","build")

if not _RELEASE:
    _component_func = components.declare_component(
        _COMPONENT_NAME,
        path=build_dir,
        # url="http://localhost:3001",
    )
else:
    _component_func = components.declare_component(
        _COMPONENT_NAME,
        path=build_dir
    )

# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.
def renderLightweightCharts(charts: Dict, key: str = None):
    """Create a new instance of "renderLightweightCharts".

    Parameters
    ----------
    charts: <List of Dicts>

        chart: <Dict>
        https://tradingview.github.io/lightweight-charts/docs/api/interfaces/ChartOptions

        series: <List of Dicts>
            https://tradingview.github.io/lightweight-charts/docs/series-types

            type: <str-enum>
                Area
                Bar
                Baseline
                Candlestick
                Histogram
                Line

            data: <List of Dicts> accordingly to series type

            options: <Dict> with style options

            priceScale: <Dict> optional
    
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    """

    return _component_func(
        charts=charts,
        key=key
    )


if not _RELEASE:
    import streamlit as st

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
    df['VOL_ASK'] = -df['volume'].sample(frac=1).values                         # shuffle and negate volume values

    # export to JSON format
    df['color'] = np.where(  df['open'] > df['close'], COLOR_BEAR, COLOR_BULL)  # bull or bear
    candles = json.loads(df.to_json(orient = "records"))
    sma_slow = dataToJSON(df,"SMA_60", 60, 'blue')
    ema_fast = dataToJSON(df, "EMA_14", 14, 'orange')
    vol_BID = dataToJSON(df,'volume', 0, COLOR_BULL)
    vol_ASK = dataToJSON(df,'VOL_ASK', 0, COLOR_BEAR)
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
            "data": vol_BID,
            "options": {
                "priceFormat": {
                    "type": 'volume',
                },
                "pane": 1

            }
        },
        {
            "type": 'Histogram',
            "data": vol_ASK,
            "options": {
                "priceFormat": {
                    "type": 'volume',
                },
                # "priceFormat": {
                #     "type": 'custom',
                #     "formatter": (price) => Math.abs(price / 1000000).toFixed(2),
                # },
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