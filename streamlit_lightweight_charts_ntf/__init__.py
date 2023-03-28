import os
from typing import Dict
from enum import Enum
import streamlit.components.v1 as components

_COMPONENT_NAME = "streamlit_lightweight_charts_ntf"
_RELEASE = False

class Chart(str, Enum):
    Area = 'addAreaSeries'
    Baseline = 'addBaselineSeries'
    Histogram = 'addHistogramSeries'
    Line = 'addLineSeries'
    Bar = 'addBarSeries'
    Candlestick = 'addCandlestickSeries'

if not _RELEASE:
    _component_func = components.declare_component(
        _COMPONENT_NAME,
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend","build")
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

    # Request historic pricing data via finance.yahoo.com API
    df = yf.Ticker('AAPL').history(period='4mo')[['Open', 'High', 'Low', 'Close', 'Volume']]

    # Some data wrangling to match required format
    df = df.reset_index()
    df.columns = ['time','open','high','low','close','volume']                  # rename columns
    df['time'] = df['time'].dt.strftime('%Y-%m-%d')                             # Date to string
    df['color'] = np.where(  df['open'] > df['close'], COLOR_BEAR, COLOR_BULL)  # bull or bear
    df.ta.macd(close='close', fast=6, slow=12, signal=5, append=True)           # calculate macd

    # extract to JSON format
    candles = json.loads(df.to_json(orient = "records"))
    volume = json.loads(df.rename(columns={"volume": "value",}).to_json(orient = "records"))
    macd_fast = json.loads(df.rename(columns={"MACDh_6_12_5": "value"}).to_json(orient = "records"))
    macd_slow = json.loads(df.rename(columns={"MACDs_6_12_5": "value"}).to_json(orient = "records"))
    df['color'] = np.where(  df['MACD_6_12_5'] > 0, COLOR_BULL, COLOR_BEAR)  # MACD histogram color
    macd_hist = json.loads(df.rename(columns={"MACD_6_12_5": "value"}).to_json(orient = "records"))


    chartMultipaneOptions = [
        {
            "width": 600,
            "height": 400,
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
            "crosshair": {
                "mode": 0
            },
            "priceScale": {
                "borderColor": "rgba(197, 203, 206, 0.8)"
            },
            "timeScale": {
                "borderColor": "rgba(197, 203, 206, 0.8)",
                "barSpacing": 10,
                "minBarSpacing": 8
            },
            "watermark": {
                "visible": True,
                "fontSize": 48,
                "horzAlign": 'center',
                "vertAlign": 'center',
                "color": 'rgba(171, 71, 188, 0.3)',
                "text": 'AAPL - D1',
            }
        },
        {
            "width": 600,
            "height": 100,
            # "crosshair": {
            #     "mode": 0
            # },
            "layout": {
                "background": {
                    "type": 'solid',
                    "color": 'transparent'
                },
                "textColor": 'black',
            },
            "grid": {
                "vertLines": {
                    "color": 'rgba(42, 46, 57, 0)',
                },
                "horzLines": {
                    "color": 'rgba(42, 46, 57, 0.6)',
                }
            },
            "timeScale": {
                "visible": False,
            },
            "watermark": {
                "visible": True,
                "fontSize": 18,
                "horzAlign": 'left',
                "vertAlign": 'top',
                "color": 'rgba(171, 71, 188, 0.7)',
                "text": 'Volume',
            }
        },
        {
            "width": 600,
            "height": 200,
            "layout": {
                "background": {
                    "type": "solid",
                    "color": 'white'
                },
                "textColor": "black"
            },
            "timeScale": {
                "visible": False,
            },
            "watermark": {
                "visible": True,
                "fontSize": 18,
                "horzAlign": 'left',
                "vertAlign": 'center',
                "color": 'rgba(171, 71, 188, 0.7)',
                "text": 'MACD',
            }
        }
    ]

    seriesCandlestickChart = [
        {
            "type": 'Candlestick',
            "data": candles,
            "options": {
                "upColor": COLOR_BULL,
                "downColor": COLOR_BEAR,
                "borderVisible": False,
                "wickUpColor": COLOR_BULL,
                "wickDownColor": COLOR_BEAR
            }
        }
    ]

    seriesVolumeChart = [
        {
            "type": 'Histogram',
            "data": volume,
            "options": {
                "priceFormat": {
                    "type": 'volume',
                },
                "priceScaleId": "" # set as an overlay setting,
            },
            "priceScale": {
                "scaleMargins": {
                    "top": 0,
                    "bottom": 0,
                },
                "alignLabels": False
            }
        }
    ]

    seriesMACDchart = [
        {
            "type": 'Line',
            "data": macd_fast,
            "options": {
                "color": 'blue',
                "lineWidth": 2
            }
        },
        {
            "type": 'Line',
            "data": macd_slow,
            "options": {
                "color": 'green',
                "lineWidth": 2
            }
        },
        {
            "type": 'Histogram',
            "data": macd_hist,
            "options": {
                "color": 'red',
                "lineWidth": 1
            }
        }
    ]

    st.subheader("Multipane Chart with Pandas")

    renderLightweightCharts([
        {
            "chart": chartMultipaneOptions[0],
            "series": seriesCandlestickChart
        },
        {
            "chart": chartMultipaneOptions[1],
            "series": seriesVolumeChart
        },
        {
            "chart": chartMultipaneOptions[2],
            "series": seriesMACDchart
        }
    ], 'multipane')