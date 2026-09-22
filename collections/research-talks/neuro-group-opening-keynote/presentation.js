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
  await Plotly.newPlot('compute-gap-chart', [{
    type:'bar',orientation:'h',y:['Other','China','United States'],x:[10,15,75],
    marker:{color:['#b9cbd6',colors.amber,colors.blue]},
    text:['~10%','~15%','~75%'],textposition:'outside',cliponaxis:false,
    hovertemplate:'%{y}: ~%{x}%<extra>Tracked performance · 2025 study</extra>'
  }], {...chartBase,margin:{l:112,r:45,t:15,b:45},
    xaxis:{...chartBase.xaxis,range:[0,90],tickvals:[0,25,50,75],ticksuffix:'%',title:{text:'Share of tracked performance',font:{size:14}}},
    yaxis:{...chartBase.yaxis,showgrid:false},bargap:.45}, chartConfig);
  charts.push(document.getElementById('compute-gap-chart'));
  await Plotly.newPlot('electricity-chart', [{
    type:'bar',x:['2025','2030'],y:[485,950],
    marker:{color:[colors.blue,'rgba(0,100,158,.13)'],line:{color:colors.blue,width:[0,2]}},
    text:['485','950'],textposition:'outside',cliponaxis:false,
    customdata:['Historical estimate','Central projection'],
    hovertemplate:'%{x}: %{y} TWh<br>%{customdata}<extra>IEA 2026</extra>'
  }], {...chartBase,margin:{l:62,r:28,t:25,b:42},
    xaxis:{...chartBase.xaxis,type:'category',tickvals:['2025','2030'],ticktext:['2025','2030 · projected']},
    yaxis:{...chartBase.yaxis,range:[0,1100],tickvals:[0,250,500,750,1000],title:{text:'TWh / year',font:{size:14}}},bargap:.53},chartConfig);
  charts.push(document.getElementById('electricity-chart'));
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
      customdata:members.map(m=>[m.index,m.name,m.url,m.status]),
      text:members.map(m=>m.label||''),textposition:members.map(m=>m.position||'top center'),
      textfont:{size:11,color:colors.text},marker:{color,size:9,line:{color:'#fff',width:1}},
      hovertemplate:'<b>%{customdata[1]}</b><br>~%{y:.3g} PFLOP-days<br>%{customdata[3]}<br>Paper: %{customdata[2]}<extra>Click point to open source</extra>'};
  });
  const training=document.getElementById('training-chart');
  await Plotly.newPlot(training,traces,{...chartBase,margin:{l:72,r:25,t:29,b:43},
    xaxis:{...chartBase.xaxis,range:[1984,2026],tickvals:[1985,1995,2005,2015,2025]},
    yaxis:{...chartBase.yaxis,type:'log',range:[-10.8,7.3],tickvals:[1e-10,1e-6,1e-2,1e2,1e6],ticktext:['10⁻¹⁰','10⁻⁶','10⁻²','10²','10⁶'],title:{text:'Training compute · PFLOP-days',font:{size:13}}},
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
