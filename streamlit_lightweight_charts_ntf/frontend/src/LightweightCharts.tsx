import { Streamlit } from "streamlit-component-lib"
import { useRenderData } from "streamlit-component-lib-react-hooks"

import './App.css';
import {
  ChartOptions,
  createChart,
  IChartApi,
  MouseEventParams
} from "lightweight-charts"

import React, { useRef, useEffect } from "react"

interface ChartsDataItems {
  chart: ChartOptions;
  series: any;
}

enum Chart{
    Area = 'addAreaSeries',
    Baseline = 'addBaselineSeries',
    Histogram = 'addHistogramSeries',
    Line = 'addLineSeries',
    Bar = 'addBarSeries',
    Candlestick = 'addCandlestickSeries',
}

function formatTime(timeInput: number | string): string {
  let date: Date;

  // Check if the time is a number (Unix timestamp)
  if (typeof timeInput === 'number') {
    date = new Date(timeInput * 1000); // Convert Unix timestamp to milliseconds
  } else if (typeof timeInput === 'string') {
    // Check if the time is in ISO string format (like '2023-05-22' or more detailed)
    if (timeInput.match(/^\d{4}-\d{2}-\d{2}/)) {
      date = new Date(timeInput);
    } else {
      console.error("Unrecognized time format:", timeInput);
      return "Invalid time"; 
    }
  } else {
    console.error("Unrecognized time type:", typeof timeInput);
    return "Invalid time"; 
  }

  // Format the time as desired, e.g., 'YYYY-MM-DD HH:MM:SS'
  return date.toISOString().slice(0, 19).replace('T', ' ');
}


const LightweightChartsMultiplePanes: React.VFC = () => {

  // { args: object, disabled: boolean, theme: object } from Streamlit
  const renderData = useRenderData()
  const chartsData = renderData.args["charts"]

  const chartsContainerRef = useRef<HTMLDivElement>(null)
  const chartElRefs = Array(chartsData.length).fill(useRef<HTMLDivElement>(null))
  const chartRefs = useRef<IChartApi[]>([])


  const toolTipWidth = 80;
  const toolTipHeight = 80;
  const toolTipMargin = 15;
  // Tooltip element
  const tooltip = document.createElement('div');
  tooltip.style.background = 'white';
  tooltip.style.color = 'black';
  tooltip.style.borderColor = '#2962FF';
  tooltip.className = 'floating-tooltip-2';
  tooltip.style.display = 'none';

    useEffect(() => {
      if (chartElRefs.find((ref) => !ref.current)) return;

      chartElRefs.forEach((ref, i) => {
        const chart: IChartApi = chartRefs.current[i] = createChart(
          ref.current as HTMLDivElement,{
            height: 300,
            width: chartElRefs[i].current.clientWidth,
            ...chartsData[i].chart,
          }
        );

        for (const series of chartsData[i].series){

          // @ts-ignore - dynamic access to IChartApi methods (e.g.: chart.addLineSeries() )
          const chartSeries = chart[Chart[series.type]](series.options)

          if(series.priceScale)
            chart.priceScale(series.options.priceScaleId || '').applyOptions(series.priceScale)

          chartSeries.setData(series.data)

          if(series.markers)
            chartSeries.setMarkers(series.markers)

        }


        ref.current.appendChild(tooltip);

        // Attach event listener for the crosshair move to each chart
        chart.subscribeCrosshairMove((param: MouseEventParams) => {
          if (!param.point || !param.time) {
            // Hide the tooltip if the crosshair is off the chart
            tooltip.style.display = 'none'
            return
          }

          // Extract the prices for the current crosshair position
          const prices: any[] = []
          chartsData.forEach((el: ChartsDataItems) => {
            el.series.forEach((series: any, idx: number) => {
              // Use the spread operator to get the whole set by idx
              const values = [ ...param.seriesData.values() ][idx]
              prices.push({
                'title': series.title,
                'type': series.type,
                values
              });
            });
          });

          // Format the time from the timestamp
          const formattedTime = formatTime(param.time as any);

          // Construct the tooltip content
          let tooltipHtml = `<div class="tooltip-content"><strong>Time:</strong> ${formattedTime}</div>`;
          prices.forEach((price) => {
            tooltipHtml +=`<div class="tooltip-content"><strong class="tooltip-title">${price.title}</strong>: `;
            if (price.type === 'Candlestick') {
              tooltipHtml += `O: ${price.values.open}, H: ${price.values.high}, L: ${price.values.low}, C: ${price.values.close}</div>`;
            } else {
              tooltipHtml += ` ${Math.round(100 * (price.values.value + Number.EPSILON)) / 100}</div>`;
            }
          });

          const y = param.point.y;
          let left = param.point.x + toolTipMargin + 100;
          if (left > ref.current.clientWidth - toolTipWidth) {
            left = param.point.x - toolTipMargin - toolTipWidth;
          }

          let top = y + toolTipMargin;
          if (top > ref.current.clientHeight - toolTipHeight) {
            top = y - toolTipHeight - toolTipMargin;
          }
          tooltip.style.left = left + 'px';
          tooltip.style.top = top + 'px';

          // Update the tooltip content and position
          tooltip.innerHTML = tooltipHtml;
          tooltip.style.display = 'block';
        });

        


        // user clicked the 'pointer'
        chart.subscribeClick((param: MouseEventParams) => {
          if (!param.point || !param.time) { return }

          const prices: any[] = []

          chartsData.forEach((el: ChartsDataItems) => {
            el.series.forEach((series: any, idx: number) => {
              // @ts-ignore - get the whole set by idx 
              const values = [ ...param.seriesData.values() ][idx]
              prices.push({
                'title': series.title,
                'type': series.type,
                values
              })
            })
          })

          Streamlit.setComponentValue({
            'time': param.time,
            prices
          })

        })

        // user moved the 'pointer'
        // chart.subscribeCrosshairMove(param => {
        //   console.log('CrossHair',param)
        // })

        // chart.timeScale().subscribeVisibleTimeRangeChange(param => {
        //   console.log('TimeRangeChange',param)
        // });

        chart.timeScale().fitContent();

      })
  
      const charts = chartRefs.current.map((c) => c as IChartApi);
      
      if(chartsData.length > 1){ // sync charts

        charts.forEach((chart) => {
          if (!chart) return;

          chart.timeScale().subscribeVisibleTimeRangeChange((e) => {
            charts
              .filter((c) => c !== chart)
              .forEach((c) => {
                c.timeScale().applyOptions({
                  rightOffset: chart.timeScale().scrollPosition()
                })
              })
          })

          chart.timeScale().subscribeVisibleLogicalRangeChange((range) => {
            if (range) {
              charts
                .filter((c) => c !== chart)
                .forEach((c) => {
                  c.timeScale().setVisibleLogicalRange({
                    from: range?.from,
                    to: range?.to

      }) }) } }) }) }

      // const handleResize = () => {
      //   chart.applyOptions({ width: chartsContainerRef?.current?.clientWidth })
      // }
      // window.addEventListener('resize', handleResize)

      return () => { // required because how useEffect() works
        charts.forEach((chart) => {
          chart.remove()
          tooltip.remove()
        })
      }

    }, [ chartsData, chartElRefs, chartRefs])

    return (
      <div ref={chartsContainerRef}>
        {chartElRefs.map((ref, i) => (
          <div
            ref={ref}
            id={`lightweight-charts-${i}`}
            key={`lightweight-charts-${i}`}
          />
        ))}
      </div>
    )

}

export default LightweightChartsMultiplePanes
