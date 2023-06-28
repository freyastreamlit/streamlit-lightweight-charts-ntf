import { Streamlit } from "streamlit-component-lib"
import { useRenderData } from "streamlit-component-lib-react-hooks"
import {
  ChartOptions,
  createChart,
  IChartApi,
  MouseEventParams,
} from "lightweight-charts"

import React, { useRef, useEffect } from "react"

interface ChartsDataItems {
  chart: ChartOptions;
  series: any;
}

const LightweightChartsMultiplePanes: React.VFC = () => {

  // { args: object, disabled: boolean, theme: object } from Streamlit
  const renderData = useRenderData()
  const chartsData = renderData.args["charts"]

  const chartsContainerRef = useRef<HTMLDivElement>(null)
  const chartElRefs = Array(chartsData.length).fill(useRef<HTMLDivElement>(null))
  const chartRefs = useRef<IChartApi[]>([])

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
          const chartSeries = chart[`add${series.type}Series`](series.options)

          if(series.priceScale)
            chart.priceScale(series.options.priceScaleId || '').applyOptions(series.priceScale)

          chartSeries.setData(series.data)

          if(series.markers)
            chartSeries.setMarkers(series.markers)

        }

        // user clicked the 'pointer'
        chart.subscribeClick((param: MouseEventParams) => {
          if (!param.point || !param.time) { return }

          const charts: any[] = []
          chartsData.forEach((el: ChartsDataItems) => {
            const prices: any[] = []
            el.series.forEach((series: any, idx: number) => {
              // @ts-ignore - get the whole set by idx 
              const values = [ ...param.seriesData.values() ][idx]
              prices.push({
                'title': series.title,
                'type': series.type,
                values
              })
            })
            charts.push({
              'time': param.time,
              prices
            })
          })

          Streamlit.setComponentValue(charts)

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
