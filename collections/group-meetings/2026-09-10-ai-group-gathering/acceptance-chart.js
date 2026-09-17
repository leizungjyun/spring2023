/* Probabilities are illustrative scenarios supplied in the meeting outline. */
const n = Array.from({length:20}, (_, i) => i + 1);
let chartReady = false;
function drawChart() {
  const target = document.getElementById('plot');
  if (!target || !window.Plotly) return;
  if (chartReady) { Plotly.Plots.resize(target); return; }
  chartReady = true;
  const scenarios = [
    [.10, 'p = 10% (NSFC General Program)', '#42affa'],
    [.20, 'p = 20% (AAAI-like)', '#ffbf69'],
    [.25, 'p = 25% (NeurIPS/CVPR-like)', '#72dfbe']
  ];
  Plotly.newPlot(target, scenarios.map(([p,name,color]) => ({
    x:n, y:n.map(k => 1-Math.pow(1-p,k)), name, mode:'lines+markers',
    line:{color,width:3}, marker:{size:5},
    hovertemplate:'Submissions: %{x}<br>Probability: %{y:.1%}<extra>%{fullData.name}</extra>'
  })), {
    width:1100, height:382, paper_bgcolor:'#191919', plot_bgcolor:'#191919',
    font:{family:'Arial, sans-serif',size:17,color:'#eee'},
    margin:{l:80,r:25,t:15,b:65},
    showlegend:false,
    shapes:[{type:'line',xref:'paper',x0:0,x1:1,yref:'y',y0:.5,y1:.5,line:{color:'#ff5252',width:2,dash:'dash'}}],
    annotations:[{xref:'paper',x:1,yref:'y',y:.5,text:'50%',showarrow:false,xanchor:'right',yanchor:'bottom',font:{color:'#ff5252',size:17},bgcolor:'#191919'}],
    xaxis:{title:'Number of independent submissions (n)',tickmode:'array',tickvals:[1,5,10,15,20],range:[.7,20.3],gridcolor:'#383838',zeroline:false},
    yaxis:{title:'Probability',tickformat:'.0%',range:[0,1.02],dtick:.2,gridcolor:'#383838',zeroline:false}
  }, {responsive:true,displayModeBar:false});
}

drawChart();

// Keyboard events in an iframe do not bubble to the presentation.
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && window.parent !== window && window.parent.Reveal) {
    event.preventDefault();
    window.parent.Reveal.toggleOverview();
    window.parent.focus();
  }
});
