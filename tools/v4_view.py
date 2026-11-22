"""V4 add-on (run after v4_rivals.py): great projects + the Parallel Universe View.
The Parallel Universe Pictureframe is the first great project: invented in Age III once the Observatory
is known, then built once. With enough anchors and crystals it opens the View for 3 turns: the buildings
of every rival appear as ghosts in their colour over your own map. On activation every building that
stands on the same tile in two universes is destroyed - yours and theirs."""
import sys
P=sys.argv[1] if len(sys.argv)>1 else 'site/play4/index.html'
s=open(P).read()
def rep(a,b,n=1):
  global s
  assert s.count(a)==n,(s.count(a),a[:90]);s=s.replace(a,b)

# ---------- the invention (type G = great project) ----------
rep(" counter:{n:'Counter-Resonance',",
    " pframe:{n:'Parallel Universe Pictureframe',era:2,r:{lig:3,eth:2,sym:2},t:'G',pre:'observatory',d:'Great project: a monumental frame that looks into the other universes. Unlocks the Pictureframe and the Parallel Universe View',con:'Needs the Observatory invention first'},\n counter:{n:'Counter-Resonance',")
# experiments respect the prerequisite
rep("const hit=same.find(([id,v])=>v.era<=e&&Object.entries(v.r).every(([p,l])=>S.prin[p]>=l));",
    "const hit=same.find(([id,v])=>v.era<=e&&(!v.pre||S.inv[v.pre])&&Object.entries(v.r).every(([p,l])=>S.prin[p]>=l));")
rep("  else{const miss=Object.entries(v.r).find(([p,l])=>S.prin[p]<l);res='near';",
    "  else if(v.pre&&!S.inv[v.pre]){res='near';txt=`The frame of something enormous takes shape – but we must first master the <b>${INV[v.pre].n}</b>.`}\n  else{const miss=Object.entries(v.r).find(([p,l])=>S.prin[p]<l);res='near';")
# ---------- the building ----------
rep(" front:{name:'Front Company',",
    " pframe:{name:'Pictureframe',cost:30000,bt:6,k:6,up:500,mw:40,col:'#ffe08a',d:'Great project · opens the Parallel Universe View · only one',req:'pframe',spr:'fac_pframe',great:true},\n front:{name:'Front Company',")
rep("'fac_core','fac_front'];","'fac_core','fac_front','fac_pframe'];")
rep("const V2_ART=new Set(['fac_front',","const V2_ART=new Set(['fac_pframe','fac_front',")
rep(" if(t==='front'&&S.slots[k].some(f=>f&&f.t==='front'))return;"," if(t==='front'&&S.slots[k].some(f=>f&&f.t==='front'))return;\n if(FAC[t].great&&count(S,t))return;")
rep("if(t==='front'&&S.slots[k].some(f=>f&&f.t==='front'))continue;const ok=","if(t==='front'&&S.slots[k].some(f=>f&&f.t==='front'))continue;if(FAC[t].great&&count(S,t))continue;const ok=")
# cards: great projects get their own label and frame
rep("const TY={E:'Edict',A:'Facility',M:'Module',P:'Psy action'};\n for(let a=0;a<4;a++)","const TY={E:'Edict',A:'Facility',M:'Module',P:'Psy action',G:'Great project'};\n for(let a=0;a<4;a++)")

# ---------- the view ----------
JS=r"""
// ===== V4: the Parallel Universe View =====
const VIEW_K=5,VIEW_ANC=2,VIEW_TURNS=3;
function viewReady(u){u=u||S;return u.slots&&Object.values(u.slots).some(a=>a.some(f=>f&&f.t==='pframe'&&!(f.bt>0)&&!f.off&&!f.mb))}
function viewOn(u){u=u||MV.me;return u.viewUntil>u.round}
function activateView(){const u=S;if(!MV||!viewReady(u)||viewOn(u)||u.over||u.crystals<VIEW_K||Object.keys(u.anchors).length<VIEW_ANC)return;
 u.crystals-=VIEW_K;u.viewUntil=u.round+VIEW_TURNS;u.inst=clamp(u.inst+1,0,100);
 // annihilation: every building on a tile that another universe also built on
 const lost=[];
 allU().forEach(o=>{if(o===u||(o!==MV.me&&o.over))return;
  for(const k in u.slots)u.slots[k].forEach((f,i)=>{if(!f)return;const [x,y]=u.slotTiles[k][i];
   for(const k2 in o.slots)o.slots[k2].forEach((g,j)=>{if(!g||!u.slots[k][i])return;const [x2,y2]=o.slotTiles[k2][j];if(x===x2&&y===y2){lost.push([o,FAC[f.t].name,FAC[g.t].name,DISTRICTS[k].name]);u.slots[k][i]=null;o.slots[k2][j]=null}})})});
 const me=MV.me;
 if(u===me){MV.rep=`<b>Parallel Universe View</b> open for ${VIEW_TURNS} turns.`+(lost.length?' Where two universes overlapped, reality tore: '+lost.map(([o,a,b,d])=>`our ${a} and ${o.bot.name}'s ${b} in ${d}`).join('; ')+' were destroyed.':' No building overlapped – nothing was lost.')}
 else{const hit=lost.filter(([o])=>o===me);if(hit.length)me.log&&MV.news.push(['Rift flash!',`${u.bot.name} opened a window into the other universes. Where their buildings overlapped ours, both were annihilated: `+hit.map(([o,a,b,d])=>`our ${b} in ${d}`).join(', ')+'.'])}
 computePower();save();render();if(typeof buildDim==='function'&&u===me)draw()}
const GHOST_IMG={},GHOST_T={};
['gen','lab','sender','drill','stab','tesla','portal','obs','tube','hangar','cooler','doppel','riftanchor','core','front','pframe'].forEach(t=>{const im=new Image();im.src='sprites/ghost_'+t+'.webp';GHOST_IMG[t]=im});
function ghostTinted(t,col){const key=t+col;if(GHOST_T[key])return GHOST_T[key];const im=GHOST_IMG[t];if(!im||!im.complete||!im.naturalWidth)return null;
 const c=document.createElement('canvas');c.width=im.naturalWidth;c.height=im.naturalHeight;const x=c.getContext('2d');x.drawImage(im,0,0);
 x.globalCompositeOperation='source-atop';x.globalAlpha=.42;x.fillStyle=col;x.fillRect(0,0,c.width,c.height);return GHOST_T[key]=c}
function drawGhosts(g,t){if(!MV||!viewOn())return;
 MV.rivals.forEach(r=>{if(r.over)return;const col=rcol(r);
  for(const k in r.slots)r.slots[k].forEach((f,i)=>{if(!f)return;const [x,y]=r.slotTiles[k][i];const img=ghostTinted(f.t,col);if(!img)return;
   const p=P(x+.5,y+.5),w=(f.t==='pframe'?40:30)*STREET_K,h=w*img.height/img.width;
   g.save();g.globalAlpha=(f.bt>0?.4:.82)+.1*Math.sin(t*3+x+y);g.shadowColor=col;g.shadowBlur=1.5*RS;g.drawImage(img,p[0]-w/2,p[1]+7-h,w,h);g.restore()})})}
"""
rep("// ===== V3: agent name + online Hall of Fame",JS+"// ===== V3: agent name + online Hall of Fame")
# draw the ghosts right after the city layer
rep("g.setTransform(1,0,0,1,0,0);g.drawImage(city,0,0);if(FXHI){g.globalCompositeOperation='lighter';g.globalAlpha=.55;g.drawImage(WGLOW,0,0)}g.globalAlpha=1;g.globalCompositeOperation='source-over';g.setTransform(RS,0,0,RS,0,0);",
    "g.setTransform(1,0,0,1,0,0);g.drawImage(city,0,0);if(FXHI){g.globalCompositeOperation='lighter';g.globalAlpha=.55;g.drawImage(WGLOW,0,0)}g.globalAlpha=1;g.globalCompositeOperation='source-over';g.setTransform(RS,0,0,RS,0,0);\n drawGhosts(g,frameN/60);")
# while the view is open we also see every rival's anchors
rep("function knows(i){return !!(MV.contact[i]||pactOn(i)||MV.intel[i]>=MV.me.round)}","function knows(i){return !!(MV.contact[i]||pactOn(i)||MV.intel[i]>=MV.me.round||MV.me.viewUntil>MV.me.round)}")

# ---------- button on the map ----------
rep('<button class="end" id="end">END TURN</button>','<button class="end" id="end">END TURN</button><button class="pview" id="pview" hidden>PARALLEL VIEW</button>')
rep(" $('rivstrip').innerHTML=rivalStrip();",
""" $('rivstrip').innerHTML=rivalStrip();
 {const b=$('pview');const ready=MV&&viewReady(S),on=MV&&viewOn();b.hidden=!ready&&!on;
  const why=Object.keys(S.anchors).length<VIEW_ANC?`needs ${VIEW_ANC} anchors`:S.crystals<VIEW_K?`needs ◆${VIEW_K}`:'';
  b.innerHTML=on?`VIEW OPEN <small>${S.viewUntil-S.round} turn${S.viewUntil-S.round>1?'s':''}</small>`:`PARALLEL VIEW <small>${why||'◆'+VIEW_K+' · '+VIEW_TURNS+' turns'}</small>`;
  b.disabled=on||!!why||!!S.over;b.classList.toggle('on',!!on)}""")
rep("$('end').onclick=endTurn;","$('end').onclick=endTurn;\n$('pview').onclick=()=>{const b=$('pview');if(b.dataset.armed){delete b.dataset.armed;activateView();return}b.dataset.armed=1;b.innerHTML='OPEN THE VIEW? <small>overlapping buildings are destroyed</small>';setTimeout(()=>{if(b.dataset.armed){delete b.dataset.armed;render()}},3500)};")

# ---------- bots: build the great project and use the view ----------
rep(" if(S.crystals<8)need.push('drill');"," if(S.crystals<8)need.push('drill');\n if(has('pframe')&&!count(S,'pframe')&&S.money>34000)need.unshift('pframe');")
rep(" // psy\n if(S.c.unruhe>55&&S.psy>=5)usePsy(null,'calm');"," if(viewReady(S)&&!viewOn(S)&&S.crystals>=VIEW_K+4&&Object.keys(S.anchors).length>=VIEW_ANC&&rnd()<.25)activateView();\n // psy\n if(S.c.unruhe>55&&S.psy>=5)usePsy(null,'calm');")

CSS="""
/* V4: great projects + the Parallel Universe View */
.icard.tG{border:2px solid #e2c480;box-shadow:0 0 12px rgba(226,196,128,.3);background:linear-gradient(#1c1810,#0c0a06)}.icard.tG .itop small{color:#e2c480}
.pview{position:absolute;top:122px;right:12px;width:auto;min-width:190px;pointer-events:auto;text-align:center;padding:8px 10px;font:14px 'Federo',serif;letter-spacing:3px;color:#e9ddff;background:linear-gradient(#2a1d40,#140d22);border:1px solid #c9a0ff;box-shadow:0 0 12px rgba(192,112,255,.35);cursor:pointer}
.pview small{display:block;font:11px 'Josefin Sans',sans-serif;letter-spacing:1px;color:#c9b8e8}.pview:disabled{opacity:.6;cursor:default}.pview.on{color:#fff;background:linear-gradient(#5a3a90,#2a1848);animation:pvpulse 2s ease-in-out infinite}
@keyframes pvpulse{50%{box-shadow:0 0 26px rgba(192,112,255,.8)}}
"""
idx=s.rindex("</style>",0,s.index("<body"));s=s[:idx]+CSS+s[idx:]
open(P,'w').write(s);print('view patched',len(s))
