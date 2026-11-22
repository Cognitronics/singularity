"""V4 add-on (run after v4_fbi.py): great projects get their own tab (PROJECTS) and leave the tech tree.
Each project: requirements -> research with RP (button) -> build. Chain: Wardenclyffe Tower ->
(Observatory invention) -> Federal Bureau of Investigation -> Parallel Universe Pictureframe."""
import sys
P=sys.argv[1] if len(sys.argv)>1 else 'site/play4/index.html'
s=open(P).read()
def rep(a,b,n=1):
  global s
  assert s.count(a)==n,(s.count(a),a[:90]);s=s.replace(a,b)

# ---- great projects leave the bench, the tree, hints and recipe gifts ----
rep("const same=Object.entries(INV).filter(([id,v])=>!S.inv[id]&&","const same=Object.entries(INV).filter(([id,v])=>v.t!=='G'&&!S.inv[id]&&")
rep("const warm=ps.filter(p=>Object.entries(INV).some(([id,v])=>!S.inv[id]&&","const warm=ps.filter(p=>Object.entries(INV).some(([id,v])=>v.t!=='G'&&!S.inv[id]&&")
rep("function craneHunch(){const e=era();const cand=Object.entries(INV).filter(([id,v])=>!S.inv[id]&&","function craneHunch(){const e=era();const cand=Object.entries(INV).filter(([id,v])=>v.t!=='G'&&!S.inv[id]&&")
rep("const cand=Object.entries(INV).filter(([id,v])=>!S.inv[id]&&!S.known.includes(id)&&ps.some(","const cand=Object.entries(INV).filter(([id,v])=>v.t!=='G'&&!S.inv[id]&&!S.known.includes(id)&&ps.some(")
rep("list=Object.entries(INV).filter(([id,v])=>v.era===a)","list=Object.entries(INV).filter(([id,v])=>v.era===a&&v.t!=='G')")
rep("S.bot=d;S.rid=i;S.known.push('wardenclyffe');","S.bot=d;S.rid=i;")
rep("known:['coil','damper','portalgeo','observatory','wardenclyffe','fbi']","known:['coil','damper','portalgeo','observatory']")
# Observatory and Portal become great projects too (stage 1 and 2); one of each, built from the Projects tab
rep(" observatory:{n:'Observatory',era:1,r:{lig:2,eth:1},t:'A',"," observatory:{n:'Observatory',era:0,r:{lig:2,eth:1},t:'G',")
rep("d:'Unlocks the Observatory',con:'Needs a finished Wardenclyffe Tower'}","d:'Great project: a domed observatory that searches the sky for anchors (+2 anchor search per turn) and makes the Federal Bureau possible'}")
rep(" portalgeo:{n:'Portal Geometry',era:1,r:{eth:2,sym:2},t:'A',d:'Unlocks the Portal'}"," portalgeo:{n:'Portal',era:1,r:{eth:2,sym:2},t:'G',d:'Great project: a gate to a neighbouring universe – buy crystals there. The Empire State Building anchor needs it'}")
rep(" wardenclyffe:{n:'Wardenclyffe Tower',era:1"," wardenclyffe:{n:'Wardenclyffe Tower',era:0")
rep(" obs:{name:'Observatory',cost:7000,bt:2,k:0,"," obs:{name:'Observatory',cost:9000,bt:3,k:1,great:true,")
rep(" portal:{name:'Portal',cost:15000,bt:4,k:5,up:600,mw:40,col:'#ffffff',d:'Crystal trade with a neighbouring universe',req:'portalgeo'},"," portal:{name:'Portal',cost:15000,bt:4,k:5,up:600,mw:40,col:'#ffffff',d:'Crystal trade with a neighbouring universe',req:'portalgeo',great:true},")
# the Observer leaves a note in the newspaper whenever a new great project becomes possible
rep(" if(!BOT&&MV&&MV.news.length)msgs.unshift(...MV.news.splice(0));",
    " if(!BOT){S.obsSaid=S.obsSaid||{};const g=GP.find(x=>!S.inv[x.id]&&!S.obsSaid[x.id]&&gpReqOk(x));if(g){S.obsSaid[g.id]=1;msgs.push(['A man in a blue hat',`Witnesses describe a bald, pale gentleman in a blue tweed suit who stood perfectly still on ${['Fifth Avenue','the Brooklyn Bridge','Wall Street','Times Square'][S.round%4]} for an hour and then was simply gone. He left a card: \"${INV[g.id].n}. Now.\" (See the Projects tab.)`])}}\n if(!BOT&&MV&&MV.news.length)msgs.unshift(...MV.news.splice(0));")
# counts shown to the player only count real inventions
s=s.replace("${Object.keys(INV).length}","${NINV()}")
# great buildings are built from the Projects tab, not from the district build menu
rep("if(FAC[t].great&&count(S,t))continue;const ok=","if(FAC[t].great)continue;const ok=")
# the old "Great projects" block in the district overview gives way to the tab
rep("<div class=\"bank\"><h3>Great projects</h3>","<div class=\"bank\" hidden><h3>Great projects</h3>")
rep("The <b>Wardenclyffe Tower</b> is ready to be built on the Brooklyn shore (district overview).","The <b>Wardenclyffe Tower</b> is ready to be built on the Brooklyn shore (Projects tab).")
rep("' – build it in the district overview.':' – invent it in the laboratory first.'","' – build it in the Projects tab.':' – research it in the Projects tab first.'")

JS=r"""
// ===== V4: great projects (own tab) =====
function NINV(){return Object.values(INV).filter(v=>v.t!=='G').length}
// a finished building of type t somewhere in Manhattan
function builtFac(t,u){u=u||S;return Object.values(u.slots).some(a=>a.some(f=>f&&f.t===t&&!(f.bt>0)))}
function facLeft(t){const f=Object.values(S.slots).flat().find(f=>f&&f.t===t);return f&&f.bt}
// great projects by technological stage (stage n opens with Age n). Each: requirements -> research (RP) -> save money into its fund -> build
const GP=[
 {id:'wardenclyffe',stage:1,rp:12,site:'Brooklyn shore',money:()=>WC.cost,k:()=>WC.k,bt:()=>WC.bt,req:()=>[['Electricity 2',S.prin.ele>=2],['Waves 1',S.prin.wav>=1]],
  state:()=>wcDone()?'done':S.wc?'building':'',left:()=>S.wc&&S.wc.bt},
 {id:'observatory',stage:1,rp:12,site:'Manhattan',fac:'obs',req:()=>[['Wardenclyffe Tower built',wcDone()],['Light 2',S.prin.lig>=2],['Ether 1',S.prin.eth>=1]]},
 {id:'portalgeo',stage:2,rp:18,site:'Manhattan',fac:'portal',req:()=>[['Ether 2',S.prin.eth>=2],['Symmetry 2',S.prin.sym>=2]]},
 {id:'fbi',stage:2,rp:20,site:'Manhattan',fac:'fbi',req:()=>[['Observatory built',builtFac('obs')],['Psyche 2',S.prin.psy>=2],['Symmetry 2',S.prin.sym>=2]]},
 {id:'pframe',stage:3,rp:30,site:'Manhattan',fac:'pframe',req:()=>[['Federal Bureau HQ built',fbiDone()],['Light 3',S.prin.lig>=3],['Ether 2',S.prin.eth>=2],['Symmetry 2',S.prin.sym>=2]]}];
GP.forEach(g=>{if(!g.fac)return;g.money=()=>FAC[g.fac].cost;g.k=()=>FAC[g.fac].k;g.bt=()=>FAC[g.fac].bt;g.state=()=>builtFac(g.fac)?'done':count(S,g.fac)?'building':'';g.left=()=>facLeft(g.fac)});
function gpStageOk(g){return era()>=g.stage-1}
function gpReqs(g){return[[`Stage ${g.stage} · Age ${['I','II','III','IV'][g.stage-1]}${g.stage>1?' (knowledge '+ERA_KN[g.stage-1]+')':''}`,gpStageOk(g)],...g.req()]}
function gpReqOk(g){return gpReqs(g).every(r=>r[1])}
function gpFund(id){return(S.fund&&S.fund[id])||0}
function researchGP(id){const g=GP.find(x=>x.id===id);if(!g||S.inv[id]||!gpReqOk(g)||S.rp<g.rp||S.over)return;S.rp-=g.rp;S.inv[id]=S.round+1;onInvent(id);save();render()}
// money is saved into the project's fund; the build itself is paid from the fund
function fundGP(id,amt){const g=GP.find(x=>x.id===id);if(!g||!S.inv[id]||S.over)return;S.fund=S.fund||{};const need=g.money()-gpFund(id);amt=Math.min(amt,need,Math.max(0,Math.floor(S.money)));if(amt<=0)return;S.money-=amt;S.fund[id]=gpFund(id)+amt;save();render()}
function buildGP(id,k){const g=GP.find(x=>x.id===id);if(!g||!S.inv[id]||S.over)return;const c=g.money();if(!BOT&&gpFund(id)<c)return;
 if(!BOT){S.money+=c;S.fund[id]-=c}const m0=S.money;
 if(id==='wardenclyffe')buildWC();else if(k){const i=S.slots[k].indexOf(null);if(i>=0)build(k,i,g.fac)}
 if(!BOT&&S.money===m0){S.money-=c;S.fund[id]+=c}save();render()}
// ---- the Observer: cryptic hints about the next great project ----
function observerHint(){const g=GP.find(x=>x.state()!=='done');if(!g)return'Everything that was meant to be built, has been built. Now you will see.';const v=INV[g.id];
 if(g.state()==='building')return`The ${v.n} is being built. It was always going to be.`;
 const miss=gpReqs(g).find(r=>!r[1]);if(miss)return`The ${v.n}. Not yet. First: ${miss[0].toLowerCase()}. I have seen it happen. I do not know when.`;
 if(!S.inv[g.id])return S.rp>=g.rp?`You may study the ${v.n} now. ${g.rp} points. Do it.`:`The ${v.n} requires ${g.rp} research points. You have ${S.rp}. Be patient. Patience is a variable.`;
 const need=g.money()-gpFund(g.id);if(need>0)return`Put money aside for the ${v.n}. $${fmt(need)} more. It will matter. It already has.`;
 if(S.crystals<g.k())return`The ${v.n} needs ${g.k()} crystals. You have ${Math.floor(S.crystals)}.`;
 return`Everything is ready for the ${v.n}. Build it. ${g.site==='Manhattan'?'Choose the place. The place will not choose you.':''}`}
"""
rep("// ===== V4: the Parallel Universe View =====",JS+"// ===== V4: the Parallel Universe View =====")

# bots bank research points as soon as a great project can be researched
rep(" // anchors: activate free ones, seize from others when rich in crystals"," {const ng=GP.find(g=>g.id!=='fbi'&&!S.inv[g.id]&&gpReqOk(g));if(ng){if(S.rp>=ng.rp)researchGP(ng.id);else S.resTarget=null}}\n // anchors: activate free ones, seize from others when rich in crystals")
# the tab
rep('      <button data-t="rivals">RIVALS</button>','      <button data-t="gp">PROJECTS</button>\n      <button data-t="rivals">RIVALS</button>')
rep(" if(tab==='rivals'){",""" if(tab==='gp'){
  let h=`<div class="dhero" style="--img:url(art/inv_pframe.webp);margin-top:-14px"><h2>GREAT PROJECTS</h2></div>`;
  h+=`<div class="observer"><img src="sprites/observer.webp" alt="The Observer" width="66" height="88"><div><b>THE OBSERVER</b><small>Watches. Does not explain.</small><p>${observerHint()}</p></div></div>`;
  h+=`<p class="note">Wonders of science. Each stage of technology opens new projects. A project is researched with research points (${S.rp} RP), then you save money into its fund, then you build it.</p>`;
  let lastStage=0;
  GP.forEach(g=>{const v=INV[g.id],st=g.state(),reqs=gpReqs(g),ok=reqs.every(r=>r[1]),res=!!S.inv[g.id],fund=gpFund(g.id),cost=g.money(),full=fund>=cost;
   if(g.stage!==lastStage){lastStage=g.stage;h+=`<h3 class="gpstage ${gpStageOk(g)?'':'off'}">Stage ${g.stage} · ${ERA_NAME[g.stage-1]}${gpStageOk(g)?'':` · opens at knowledge ${ERA_KN[g.stage-1]}`}</h3>`}
   const free=Object.keys(DISTRICTS).filter(k=>S.slots[k].includes(null));const pick=window.GPDIST&&free.includes(window.GPDIST)?window.GPDIST:free[0];
   h+=`<div class="gpcard ${st} ${!ok&&!res?'locked':''}"><div class="gpart" style="background-image:url(art/inv_${g.id}.webp)"></div><h4>${v.n}</h4><p class="note">${v.d}.</p><ol class="gpsteps">`+
   `<li class="${ok||res?'ok':''}"><b>Requirements</b><br>${reqs.map(r=>`<span class="${r[1]?'y':'n'}">${r[1]?'✓':'✗'} ${r[0]}</span>`).join(' · ')}</li>`+
   `<li class="${res?'ok':''}"><b>Research</b> · ${g.rp} RP<br>${res?'<span class="y">✓ researched</span>':`<button class="btn small" data-gpr="${g.id}" ${ok&&S.rp>=g.rp&&!S.over?'':'disabled'}>Research · ${g.rp} RP</button>`}</li>`+
   `<li class="${full||st?'ok':''}"><b>Save up</b> · $${fmt(cost)}<br>${st?'<span class="y">✓ paid</span>':!res?'<span class="n">research it first</span>':`<span class="fundbar"><i style="width:${Math.min(100,fund/cost*100)}%"></i><em>$${fmt(fund)} / $${fmt(cost)}</em></span>${full?'':`<span class="fundbtns">${[2500,10000].map(a=>`<button class="btn small" data-gpf="${g.id}:${a}" ${S.money>=1&&!S.over?'':'disabled'}>+ $${fmt(a)}</button>`).join('')}<button class="btn small" data-gpf="${g.id}:${cost}" ${S.money>=1&&!S.over?'':'disabled'}>All I can</button></span>`}`}</li>`+
   `<li class="${st==='done'?'ok':''}"><b>Build</b> · ${g.site} · ◆${g.k()} · ${g.bt()} turns<br>${st==='done'?'<span class="y">✓ completed</span>':st==='building'?`<span>under construction · ${g.left()} turn${g.left()>1?'s':''} left</span>`:!res||!full?'<span class="n">research it and save up first</span>':g.id==='wardenclyffe'?`<button class="btn small" data-gpb="${g.id}" ${S.crystals>=g.k()&&!S.over?'':'disabled'}>Build on the Brooklyn shore</button>`:free.length?`<select class="gpsel" data-gps="${g.id}">${free.map(k=>`<option value="${k}" ${k===pick?'selected':''}>${DISTRICTS[k].name}</option>`).join('')}</select> <button class="btn small" data-gpb="${g.id}" ${S.crystals>=g.k()&&!S.over?'':'disabled'}>Build</button>`:'<span class="n">no free plot in Manhattan – sell a facility first</span>'}</li></ol></div>`});
  p.innerHTML=h;
  p.querySelectorAll('[data-gpr]').forEach(b=>b.onclick=()=>researchGP(b.dataset.gpr));
  p.querySelectorAll('[data-gpf]').forEach(b=>b.onclick=()=>{const [id,a]=b.dataset.gpf.split(':');fundGP(id,+a)});
  p.querySelectorAll('[data-gps]').forEach(sel=>sel.onchange=()=>{window.GPDIST=sel.value;render()});
  p.querySelectorAll('[data-gpb]').forEach(b=>b.onclick=()=>{const id=b.dataset.gpb;const sel=p.querySelector(`[data-gps="${id}"]`);buildGP(id,sel&&sel.value)});
 }
 if(tab==='rivals'){""")

# bots research the projects they need
rep(" // research: work towards known recipes, sometimes search anchors, otherwise study broadly\n",
    " // research: great projects first when possible, then known recipes, sometimes anchors, otherwise study broadly\n for(const g of GP){if(g.id==='fbi')continue;if(!S.inv[g.id]&&gpReqOk(g)&&S.rp>=g.rp){researchGP(g.id);break}}\n if(!S.inv.wardenclyffe){if(S.prin.ele<2)S.resTarget='p:ele';else if(S.prin.wav<2)S.resTarget='p:wav';else if(era()<1){const ps=Object.keys(PRIN).filter(p=>S.prin[p]<1);if(ps.length)S.resTarget='p:'+ps[0]}}\n")

CSS="""
/* V4: great projects tab */
.gpcard{border:1px solid #6b5a35;background:linear-gradient(#17140d,#0b0a07);margin:0 0 14px;padding:0 0 8px;box-shadow:0 0 0 1px #000}
.gpcard.done{border-color:#9ff0b0}.gpcard.locked{opacity:.6}
.gpart{position:relative;height:110px;background:#000 center/cover no-repeat;border-bottom:1px solid #6b5a35}.gpart span{position:absolute;left:8px;top:6px;font:400 22px 'Federo',serif;color:#e2c480;text-shadow:0 0 8px #000}
.gpcard h4{margin:8px 10px 2px;font:400 16px 'Federo',serif;letter-spacing:1px;color:#e2c480}.gpcard>.note{margin:0 10px 6px}
.gpsteps{margin:0 10px;padding-left:18px;font-size:12px;line-height:1.5}.gpsteps li{margin:0 0 6px;color:#cfc6b2}.gpsteps li.ok::marker{color:#9ff0b0}.gpsteps b{font:400 12px 'Federo',serif;letter-spacing:1px;color:#e2c480}
.gpsteps .y{color:#9ff0b0}.gpsteps .n{color:#e09a8a}.gpsteps .btn{margin-top:3px}
.tabs button{font-size:9px!important;padding:10px 2px!important;border-width:7px 3px 2px!important;letter-spacing:0!important}
.observer{display:flex;gap:10px;align-items:flex-start;margin:0 0 10px;padding:8px;border:1px solid #3a5a8a;background:linear-gradient(#0e1420,#080b12);box-shadow:inset 0 0 18px rgba(60,100,170,.25)}
.observer img{width:66px;height:88px;object-fit:cover;border:1px solid #3a5a8a;flex:none}.observer b{display:block;font:400 12px 'Federo',serif;letter-spacing:3px;color:#9ab8e8}.observer small{display:block;font-size:10px;color:#6f7f9a;margin-bottom:4px}
.observer p{margin:0;font:italic 13px/1.45 'Josefin Sans',sans-serif;color:#d4ddf0}
.gpstage{margin:14px 0 6px;color:#e2c480}.gpstage.off{color:#6f6a5e}
.fundbar{position:relative;display:block;height:16px;margin:3px 0;background:#14110c;border:1px solid #3a3122}.fundbar i{position:absolute;inset:0 auto 0 0;background:linear-gradient(90deg,#6b5a35,#e2c480)}.fundbar em{position:relative;display:block;text-align:center;font:normal 10px/16px 'Josefin Sans',sans-serif;color:#fff;text-shadow:0 1px 2px #000}
.fundbtns{display:flex;flex-wrap:wrap;gap:4px}.fundbtns .btn{font-size:10.5px!important;padding:3px 6px!important}
@media(max-width:1680px){html:not(.m) .rp small,html:not(.m) .rp .info{display:none}}@media(max-width:1440px){html:not(.m) .top .title{font-size:0;letter-spacing:0}html:not(.m) .top .title img{margin-right:0!important}}html:not(.m) .gamebtns button{letter-spacing:1px}
.gpsel{background:#0a0d0f;color:#e2c480;border:1px solid #6b5a35;font:12px 'Josefin Sans',sans-serif;padding:3px}
"""
idx=s.rindex("</style>",0,s.index("<body"));s=s[:idx]+CSS+s[idx:]
open(P,'w').write(s);print('projects patched',len(s))
