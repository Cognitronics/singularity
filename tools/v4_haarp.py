"""V4 add-on (run after v4_projects.py): HAARP - stage-3 great project on the New Jersey shore.
Weather control (once per turn, 8 psy) and a stealth veil: a share of your facilities is hidden from the
Parallel Universe View of other bureaus and survives overlaps. 30 % at first, upgradable to 45/60/80 %;
fog adds 15 %."""
import sys
P=sys.argv[1] if len(sys.argv)>1 else 'site/play4/index.html'
s=open(P).read()
def rep(a,b,n=1):
  global s
  assert s.count(a)==n,(s.count(a),a[:90]);s=s.replace(a,b)

rep(" pframe:{n:'Parallel Universe Pictureframe'",
    " haarp:{n:'HAARP',era:2,r:{wav:3,ele:2},t:'G',d:'Great project: an ionospheric research array on the New Jersey shore. It controls the weather and veils your facilities from the Parallel Universe View of other bureaus'},\n pframe:{n:'Parallel Universe Pictureframe'")
rep("{id:'wardenclyffe',stage:1,rp:12,site:'Brooklyn shore',","{id:'wardenclyffe',stage:1,rp:12,site:'Brooklyn shore',fixed:true,")
rep("['Symmetry 2',S.prin.sym>=2]]}];",
    "['Symmetry 2',S.prin.sym>=2]]},\n {id:'haarp',stage:3,rp:25,site:'New Jersey shore',fixed:true,money:()=>HP.cost,k:()=>HP.k,bt:()=>HP.bt,req:()=>[['Wardenclyffe Tower built',wcDone()],['Waves 3',S.prin.wav>=3],['Electricity 2',S.prin.ele>=2]],state:()=>haarpDone()?'done':S.haarp?'building':'',left:()=>S.haarp&&S.haarp.bt}];")
rep(" if(id==='wardenclyffe')buildWC();else if(k)"," if(id==='wardenclyffe')buildWC();else if(id==='haarp')buildHaarp();else if(k)")
rep("g.id==='wardenclyffe'?`<button class=\"btn small\" data-gpb=\"${g.id}\" ${S.crystals>=g.k()&&!S.over?'':'disabled'}>Build on the Brooklyn shore</button>`",
    "g.fixed?`<button class=\"btn small\" data-gpb=\"${g.id}\" ${S.crystals>=g.k()&&!S.over?'':'disabled'}>Build on the ${g.site}</button>`")
rep("'<span class=\"n\">no free plot in Manhattan – sell a facility first</span>'}</li></ol></div>`});",
    "'<span class=\"n\">no free plot in Manhattan – sell a facility first</span>'}</li></ol>${g.id==='haarp'&&st==='done'?haarpPanel():''}</div>`});")
rep("  p.querySelectorAll('[data-gpf]').forEach(",
    "  p.querySelectorAll('[data-wx]').forEach(b=>b.onclick=()=>setWeather(b.dataset.wx));\n  p.querySelectorAll('[data-stealth]').forEach(b=>b.onclick=upgradeStealth);\n  p.querySelectorAll('[data-gpf]').forEach(")

JS=r"""
// ===== V4: HAARP (weather control + stealth veil) =====
const HP_T=[-6,12],HP={cost:25000,k:4,bt:6,up:500},STEALTH=[.30,.45,.60,.80],STEALTH_UP=[[15,6000],[20,9000],[25,12000]];
function haarpDone(u){u=u||S;return !!(u&&u.haarp&&!(u.haarp.bt>0))}
function buildHaarp(){if(!inv('haarp')||S.haarp||S.money<HP.cost||S.crystals<HP.k||S.over)return;S.money-=HP.cost;S.crystals-=HP.k;S.haarp={bt:HP.bt};save();render()}
function veilPct(u){u=u||S;if(!haarpDone(u))return 0;return Math.min(.95,STEALTH[u.stealth||0]+(u.weather==='fog'?.15:0))}
// which facilities are veiled is fixed per plot, so raising the share only ever adds hidden ones
function veiled(u,k,i){const p=veilPct(u);if(!p||!u.slotTiles[k])return false;const [x,y]=u.slotTiles[k][i];const h=(Math.imul(x+31,73856093)^Math.imul(y+17,19349663)^Math.imul(i+3,83492791))>>>0;return(h%1000)/1000<p}
function upgradeStealth(){const l=S.stealth||0;if(!haarpDone()||l>=3||S.over)return;const [rp,m]=STEALTH_UP[l];if(S.rp<rp||S.money<m)return;S.rp-=rp;S.money-=m;S.stealth=l+1;save();render()}
function setWeather(w){if(!haarpDone()||S.wxSet===S.round||S.psy<8||S.over||S.weather===w)return;S.psy-=8;S.weather=w;S.wxSet=S.round;save();render()}
function haarpPanel(){const l=S.stealth||0,pct=Math.round(veilPct()*100);let n=0,hid=0;for(const k in S.slots)S.slots[k].forEach((f,i)=>{if(!f)return;n++;if(veiled(S,k,i))hid++});
 const WXN={clear:['☀ Clear','calm skies'],rain:['☂ Rain','unrest −2'],fog:['≋ Fog','press −3, veil +15 %'],storm:['ϟ Storm','power −15 %']};
 return`<div class="hpanel"><b>Weather control</b><small>Once per turn · 8 psy · takes effect at once</small><div class="wxbtns">${Object.entries(WXN).map(([k,v])=>`<button class="btn small ${S.weather===k?'on':''}" data-wx="${k}" title="${v[1]}" ${S.wxSet===S.round||S.psy<8||S.weather===k||S.over?'disabled':''}>${v[0]}<small>${v[1]}</small></button>`).join('')}</div>
 <b>Stealth veil · ${pct} %</b><small>Hidden from the Parallel Universe View of other bureaus${S.weather==='fog'?' (fog adds 15 %)':''}: ${hid} of ${n} facilities right now. Veiled facilities also survive when universes overlap.</small>
 ${l<3?`<button class="btn small" data-stealth="1" ${S.rp>=STEALTH_UP[l][0]&&S.money>=STEALTH_UP[l][1]&&!S.over?'':'disabled'}>Upgrade the veil to ${Math.round(STEALTH[l+1]*100)} %<small>${STEALTH_UP[l][0]} RP · $${fmt(STEALTH_UP[l][1])}</small></button>`:'<small class="y">The veil is at its maximum (80 %).</small>'}</div>`}
"""
rep("// ===== V4: the Parallel Universe View =====",JS+"// ===== V4: the Parallel Universe View =====")
# upkeep + construction
rep(" if(wcDone())upkeep+=WC.up;"," if(wcDone())upkeep+=WC.up;\n if(haarpDone())upkeep+=HP.up;")
rep(" if(S.wc&&S.wc.bt>0){S.wc.bt--;",
    " if(S.haarp&&S.haarp.bt>0){S.haarp.bt--;if(!S.haarp.bt)msgs.unshift(['HAARP completed',BOT?'':'The antenna field on the New Jersey shore hums into the clouds. We can now steer the weather – and part of our work is veiled from the eyes of other universes.'])}\n if(S.wc&&S.wc.bt>0){S.wc.bt--;")
# the view: veiled facilities are invisible and survive overlaps
rep("const lost=[];\n allU()","const lost=[],spared=[];\n allU()")
rep("if(x===x2&&y===y2){lost.push([o,FAC[f.t].name,FAC[g.t].name,DISTRICTS[k].name]);u.slots[k][i]=null;o.slots[k2][j]=null}",
    "if(x===x2&&y===y2){if(veiled(u,k,i)||veiled(o,k2,j)){spared.push([o,FAC[f.t].name,FAC[g.t].name,DISTRICTS[k].name])}else{lost.push([o,FAC[f.t].name,FAC[g.t].name,DISTRICTS[k].name]);u.slots[k][i]=null;o.slots[k2][j]=null}}")
rep(" computePower();save();render();if(typeof buildDim==='function'&&u===me)draw()}",
    " if(u!==me){const sp=spared.filter(([o])=>o===me);if(sp.length)MV.news.push(['The veil holds',`HAARP kept ${sp.length} of our facilities hidden when ${u.bot.name} opened its window – they survived.`])}\n computePower();save();render();if(typeof buildDim==='function'&&u===me)draw()}")
rep("  for(const k in r.slots)r.slots[k].forEach((f,i)=>{if(!f)return;const [x,y]=r.slotTiles[k][i];const img=ghostTinted(",
    "  for(const k in r.slots)r.slots[k].forEach((f,i)=>{if(!f||veiled(r,k,i))return;const [x,y]=r.slotTiles[k][i];const img=ghostTinted(")
# district panel: show which of my facilities are veiled
rep("<b>${FAC[f.t].name}</b><small>${st}</small>","<b>${FAC[f.t].name}</b><small>${st}${veiled(S,k,i)?' · 🌫 veiled':''}</small>")
# map: HAARP on the New Jersey shore
rep("    if(S&&S.wc&&t.x===WC_T[0]&&t.y===WC_T[1])continue;","    if(S&&S.wc&&t.x===WC_T[0]&&t.y===WC_T[1])continue;\n    if(S&&S.haarp&&t.x===HP_T[0]&&t.y===HP_T[1])continue;")
rep("  if(!MASK&&S&&S.wc&&SPR.fac_wardenclyffe){",
    "  if(!MASK&&S&&S.haarp&&SPR.fac_haarp){const p=P(HP_T[0]+.5,HP_T[1]+.5);cx.save();if(S.haarp.bt>0)cx.globalAlpha=.35+.55*(1-S.haarp.bt/HP.bt);spr(cx,'fac_haarp',p[0],p[1]+6,32,false,null);cx.restore();if(!(S.haarp.bt>0))LIGHTS.push({x:p[0],y:p[1]-30,c:'#c9a0ff',r:16})}\n  if(!MASK&&S&&S.wc&&SPR.fac_wardenclyffe){")
rep("'fac_pframe','fac_wardenclyffe','fac_fbi'];","'fac_pframe','fac_wardenclyffe','fac_fbi','fac_haarp'];")
rep("const V2_ART=new Set(['fac_fbi',","const V2_ART=new Set(['fac_haarp','fac_fbi',")

CSS="""
/* V4: HAARP panel */
.hpanel{margin:8px 10px 0;padding:8px;border:1px solid #5a3a8a;background:linear-gradient(#140f20,#0a0812)}.hpanel>b{display:block;font:400 12px 'Federo',serif;letter-spacing:2px;color:#c9a0ff;margin-top:4px}.hpanel>small{display:block;font-size:11px;color:#a89cc0;margin:2px 0 6px}
.wxbtns{display:grid;grid-template-columns:1fr 1fr;gap:4px;margin-bottom:6px}.wxbtns .btn{font-size:11px!important;padding:4px!important}.wxbtns .btn small{display:block;font-size:9.5px;color:#a89cc0}
.hpanel .y{color:#9ff0b0}
"""
idx=s.rindex("</style>",0,s.index("<body"));s=s[:idx]+CSS+s[idx:]
open(P,'w').write(s);print('haarp patched',len(s))
