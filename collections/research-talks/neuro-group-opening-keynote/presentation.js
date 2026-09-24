// Local data and plotting library keep the talk usable without a network.
const colors = {blue:'#00649e', amber:'#b76b29', text:'#203441', muted:'#607582', line:'#d5e2e9'};
const chartConfig = {displayModeBar:false, responsive:true, scrollZoom:false};
const chartBase = {
  paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)',
  font:{family:'Arial, sans-serif', size:16, color:colors.text},
  margin:{l:56,r:24,t:16,b:45},
  xaxis:{fixedrange:true,zeroline:false,gridcolor:colors.line},
  yaxis:{fixedrange:true,zeroline:false,gridcolor:colors.line}
};
const charts = [];
async function createCharts() {
  const response = await fetch('media/data/training-compute.json');
  if (!response.ok) throw new Error('Training-compute data could not load');
  const {models} = await response.json();
  const categories = {Language:colors.blue,Vision:'#8157a6',Games:colors.amber,Other:'#497c69'};
  const select = document.getElementById('model-select');
  const detail = document.getElementById('model-detail');
  models.forEach((model,i) => { const option=document.createElement('option'); option.value=i; option.textContent=model.name; select.append(option); });
  function showModel(index) {
    const model=models[index]; select.value=index; detail.replaceChildren();
    const value=document.createElement('span'); value.textContent=`${model.date.slice(0,4)} · ~${Number(model.pflopDays.toPrecision(3)).toLocaleString('en-US',{maximumSignificantDigits:3})} PFLOP-days · `;
    const link=document.createElement('a'); link.href=model.url;link.target='_blank';link.rel='noopener';link.textContent='Open model paper ↗';
    detail.append(value,link); detail.dataset.model=model.name;
  }
  select.addEventListener('change',()=>showModel(Number(select.value)));
  select.addEventListener('keydown',e=>e.stopPropagation());
  const traces=Object.entries(categories).map(([category,color]) => {
    const members=models.map((model,i)=>({...model,index:i})).filter(model=>model.category===category);
    return {type:'scatter',mode:'markers+text',name:category,
      x:members.map(m=>m.year),y:members.map(m=>m.pflopDays),
      customdata:members.map(m=>[m.index,m.name,m.url]),
      text:members.map(m=>m.label||''),textposition:members.map(m=>m.position||'top center'),
      textfont:{size:9.5,color:colors.text},marker:{color,size:9,line:{color:'#fff',width:1}},
      hovertemplate:'<b>%{customdata[1]}</b><br>~%{y:.3g} PFLOP-days<extra>Click point to open source</extra>'};
  });
  // Era trend lines for the chart, transcribed from the supplied computing-demands.pdf.
  // Each slope is the doubling rate that figure labels; each span covers the era it
  // marks. The third line is drawn at the geometry that figure uses, where it doubles
  // about every 3.5 months, so it is labelled with that rate rather than the reference's
  // "2 months", which describes the GPT-2 to GPT-3 step instead.
  const eras = [
    {colour:'#6f6b9c',slope:Math.log10(2)/2,       d2000:-7.02, from:1986.5,to:2012.3,
     text:'2 years per doubling',   tx:2001.6,ty:-6.30},
    {colour:'#1f7f4f',slope:Math.log10(2)/(3.4/12),d2000:-17.30,from:2012.5,to:2018.5,
     text:'3.4 months<br>per doubling',tx:2014.6,ty:-2.20},
    {colour:'#b0403c',slope:1.025,                 d2000:-18.32,from:2018.7,to:2022.7,
     text:'~3.5 months<br>per doubling',tx:2021.2,ty:0.60}
  ];
  // The y axis is logarithmic, so a shape's endpoints are data values: convert the
  // decade positions with 10**d. (Annotation coordinates on a log axis are decades.)
  const decadeAt=(e,year)=>Math.pow(10,e.slope*(year-2000)+e.d2000);
  const eraLayout = {
    shapes:eras.map(e=>({type:'line',x0:e.from,y0:decadeAt(e,e.from),
      x1:e.to,y1:decadeAt(e,e.to),layer:'below',
      line:{color:e.colour,width:2.5,dash:'dash'}})),
    annotations:eras.map(e=>({x:e.tx,y:e.ty,text:e.text,showarrow:false,xanchor:'left',
      font:{size:10.5,color:e.colour},bgcolor:'rgba(255,255,255,.78)',borderpad:1.5}))
  };
  const training=document.getElementById('training-chart');
  await Plotly.newPlot(training,traces,{...chartBase,margin:{l:72,r:25,t:29,b:43},...eraLayout,
    xaxis:{...chartBase.xaxis,range:[1984,2026],tickvals:[1985,1995,2005,2015,2025]},
    yaxis:{...chartBase.yaxis,type:'log',range:[-10.9,6.9],tickvals:[1e-10,1e-6,1e-2,1e2,1e6],ticktext:['10⁻¹⁰','10⁻⁶','10⁻²','10²','10⁶'],title:{text:'PFLOP-days',font:{size:13}}},
    legend:{orientation:'h',x:0,y:1.16,font:{size:11}},hoverlabel:{font:{size:12},bgcolor:'#fff'},hovermode:'closest'},chartConfig);
  // Resolve actual screen-space marker centres: native Plotly hit testing in this
  // bundled version drifts when Reveal scales the slide using zoom/transform.
  function nearestMarker(event) {
    let closest=null, distance=16;
    training.querySelectorAll('.scatterlayer .trace').forEach((trace,curveNumber)=>{
      trace.querySelectorAll('.point').forEach((point,pointNumber)=>{
        const rect=point.getBoundingClientRect();
        const d=Math.hypot(event.clientX-rect.left-rect.width/2,event.clientY-rect.top-rect.height/2);
        if(d<distance){distance=d;closest={curveNumber,pointNumber};}
      });
    });
    return closest;
  }
  let activePoint='';
  training.addEventListener('mousemove',event=>{
    event.stopImmediatePropagation();
    const point=nearestMarker(event);
    const key=point ? `${point.curveNumber}:${point.pointNumber}` : '';
    if(key===activePoint)return;
    activePoint=key;
    if(point){
      Plotly.Fx.hover(training,[point]);
      showModel(traces[point.curveNumber].customdata[point.pointNumber][0]);
    } else Plotly.Fx.unhover(training);
  },true);
  training.addEventListener('mouseleave',()=>{activePoint='';Plotly.Fx.unhover(training);});
  training.addEventListener('click',event=>{
    const point=nearestMarker(event);
    if(!point)return;
    event.stopImmediatePropagation();
    window.open(traces[point.curveNumber].customdata[point.pointNumber][2],'_blank','noopener');
  },true);
  showModel(models.length-1); charts.push(training);
  document.documentElement.dataset.chartsReady='true';
}
Reveal.initialize({
  width:1200,height:700,margin:.04,hash:true,center:false,
  slideNumber:'c/t',transition:'fade',
  plugins:[RevealAnnotations,RevealMarkdown,RevealNotes,RevealSearch,RevealZoom]
});
Reveal.on('ready',()=>createCharts().catch(error=>{
  console.error(error);document.documentElement.dataset.chartError=error.message;
}));
// Resize local charts as their slide becomes visible.
Reveal.on('slidechanged',()=>{ charts.forEach(chart=>Plotly.Plots.resize(chart)); });
