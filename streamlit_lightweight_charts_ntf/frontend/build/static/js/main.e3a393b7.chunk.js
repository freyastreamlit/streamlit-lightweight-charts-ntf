(this.webpackJsonpstreamlit_lightweight_charts_ntf=this.webpackJsonpstreamlit_lightweight_charts_ntf||[]).push([[0],{26:function(e,t,n){e.exports=n(36)},36:function(e,t,n){"use strict";n.r(t);var i=n(10),r=n.n(i),c=n(23),a=n.n(c),o=n(17),l=n(4),s=n(5),u=n(9),f=n(16),h=n(25),m=function(){var e=Object(o.useRenderData)().args.charts,t=Object(i.useRef)(null),n=Array(e.length).fill(Object(i.useRef)(null)),c=Object(i.useRef)([]);return Object(i.useEffect)((function(){if(!n.find((function(e){return!e.current}))){n.forEach((function(t,i){var r,a=c.current[i]=Object(h.a)(t.current,Object(u.a)({height:300,width:n[i].current.clientWidth},e[i].chart)),o=Object(s.a)(e[i].series);try{for(o.s();!(r=o.n()).done;){var m=r.value,p=a["add".concat(m.type,"Series")](m.options);m.priceScale&&a.priceScale(m.options.priceScaleId||"").applyOptions(m.priceScale),p.setData(m.data),m.markers&&p.setMarkers(m.markers)}}catch(d){o.e(d)}finally{o.f()}a.subscribeClick((function(t){if(t.point&&t.time){var n=[];e.forEach((function(e){var i=[];e.series.forEach((function(e,n){var r=Object(l.a)(t.seriesData.values())[n];i.push({title:e.title,type:e.type,values:r})})),n.push({time:t.time,prices:i})})),f.Streamlit.setComponentValue(n)}})),a.timeScale().fitContent()}));var t=c.current.map((function(e){return e}));return e.length>1&&t.forEach((function(e){e&&(e.timeScale().subscribeVisibleTimeRangeChange((function(n){t.filter((function(t){return t!==e})).forEach((function(t){t.timeScale().applyOptions({rightOffset:e.timeScale().scrollPosition()})}))})),e.timeScale().subscribeVisibleLogicalRangeChange((function(n){n&&t.filter((function(t){return t!==e})).forEach((function(e){e.timeScale().setVisibleLogicalRange({from:null===n||void 0===n?void 0:n.from,to:null===n||void 0===n?void 0:n.to})}))})))})),function(){t.forEach((function(e){e.remove()}))}}}),[e,n,c]),r.a.createElement("div",{ref:t},n.map((function(e,t){return r.a.createElement("div",{ref:e,id:"lightweight-charts-".concat(t),key:"lightweight-charts-".concat(t)})})))};a.a.render(r.a.createElement(r.a.StrictMode,null,r.a.createElement(o.StreamlitProvider,null,r.a.createElement(m,null))),document.getElementById("root"))}},[[26,1,2]]]);
//# sourceMappingURL=main.e3a393b7.chunk.js.map