// Scene used by tune-embedded-slides.py; helpers come from the exported figure.
function scene({moves=0,decision=null,picked=true,candOpacity=1,compare=false}={}){
 let s='';
 if(compare)edgesOf(optimal.route).forEach(([a,b])=>s+=edge(a,b,{key:`opt-${edgeKey(a,b)}`,color:C.muted,width:4,dash:true}));
 const ch=decision===null?null:nn.choices[decision];
 if(ch)ch.candidates.forEach(({to},j)=>s+=edge(ch.from,to,{key:`cand-${ch.from}-${to}`,color:picked&&j===0?C.accent:C.muted,width:picked&&j===0?4:3,dash:true,opacity:candOpacity,shorten:28}));
 const off=new Set(offEdges.map(e=>edgeKey(...e)));
 edgesOf(R).slice(0,moves).forEach(([a,b])=>s+=edge(a,b,{key:`route-${edgeKey(a,b)}`,color:compare&&off.has(edgeKey(a,b))?C.A:C.accent}));
 const visited=new Set(R.slice(0,moves+1)),current=moves<n?R[moves]:null;
 s+=cities({stroke:i=>visited.has(i)?C.accent:C.ink,fill:i=>i===current?C.accent:C.paper});
 // Reserve a separate band below the map for the decision explanation.
 s=`<g transform="translate(5 0) scale(.88)">${s}</g>`;
 s+=keyed('map-legend',text(35,35,'塗りつぶし：今いる都市',21,C.ink));
 // 訪問順
 s+=keyed('order-head',text(470,62,'訪問順',22,C.muted));
 R.slice(0,moves+1).forEach((c,j)=>{const x=490+j*76;
  if(j)s+=keyed(`order-arrow-${j}`,text(x-38,117,'→',26,C.muted,'middle'));
  s+=keyed(`order-${j}`,`<circle cx="${x}" cy="108" r="21" fill="${C.paper}" stroke="${C.accent}" stroke-width="3"/>`+text(x,116,label(c),23,C.ink,'middle'));});
 // 今いる都市から未訪問の都市までの距離
 if(ch){s+=keyed(`dist-head-${ch.from}`,text(470,180,`都市${label(ch.from)}からの距離（未訪問のみ）`,22,C.ink)+text(470,213,'棒が短いほど近い',21,C.muted),`opacity="${candOpacity}"`);
  ch.candidates.forEach(({to,d},j)=>{const y=232+j*54,hi=picked&&j===0;
   s+=keyed(`dist-${ch.from}-${to}`,text(540,y+27,`都市${label(to)}`,24,hi?C.accent:C.ink,'end')+`<rect x="${bx}" y="${y+5}" width="${(d*bs).toFixed(1)}" height="30" rx="3" fill="${hi?C.accent:muted}"/>`+text(bx+d*bs+10,y+29,f2(d),23,hi?C.accent:C.ink),`opacity="${candOpacity}"`);});}
 if(moves===n&&!compare)s+=keyed('length',text(470,250,`経路長 ${f2(nnLength)}`,32,C.ink));
 if(compare){const row=(y,body,label)=>body+text(560,y+9,label,25,C.ink);
  s+=keyed('legend-nn',row(220,`<line x1="470" y1="220" x2="540" y2="220" stroke="${C.accent}" stroke-width="6" stroke-linecap="round"/>`,`最近傍法 ${f2(nnLength)}`));
  s+=keyed('legend-opt',row(280,`<line x1="470" y1="280" x2="540" y2="280" stroke="${C.muted}" stroke-width="4" stroke-dasharray="10 9"/>`,`最適 ${f2(optimal.length)}`));
  s+=keyed('legend-off',row(340,`<line x1="470" y1="340" x2="540" y2="340" stroke="${C.A}" stroke-width="6" stroke-linecap="round"/>`,'最適経路と異なる辺'));}
 // Explain the decision in words, alongside the distance comparison.
 let message,rule;
 if(compare){
  message='各回で一番近い都市を選んでも、全体の最短経路になるとは限らない';
  rule='実線：最近傍法の経路　点線：最短経路';
 }else if(moves===n){
  message=`全都市を訪問したので、出発した都市${label(R[0])}へ戻る`;
  rule='訪問順に結んだ経路が完成';
 }else if(ch){
  const nearest=ch.candidates[0];
  message=picked
   ? `最も近い都市${label(nearest.to)}を選び、都市${label(ch.from)} → ${label(nearest.to)}へ進む（距離 ${f2(nearest.d)}）`
   : `今いる都市${label(ch.from)}から、未訪問の都市までの距離を比べる`;
  rule=picked ? '次は、移動先の都市から同じ選び方を繰り返す' : '一番短い棒の都市を選ぶ。訪問済みの都市は候補から除く';
 }else{
  message='最近傍法：今いる都市から、最も近い未訪問の都市へ進む';
  rule='全都市を訪れるまで繰り返し、最後に出発都市へ戻る';
 }
 s+=keyed('decision-message',text(35,485,message,24,C.ink));
 s+=keyed('decision-rule',text(35,528,rule,22,C.muted));
 return svg(s,'最近傍法で今いる都市から最も近い未訪問の都市へ順に進み、最適経路と比べる',W,H);}
