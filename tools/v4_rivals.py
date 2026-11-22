"""Turns site/play4/index.html (a copy of V3) into V4: 1-3 rival universes, each a full simulation
of the same game played by a bot. Shared anchors, missions (spy / sabotage / card ability),
diplomacy (pacts, trade). Every replacement asserts its anchor exists exactly once."""
import sys
P=sys.argv[1] if len(sys.argv)>1 else 'site/play4/index.html'
s=open(P).read()
def rep(a,b,n=1):
  global s
  assert s.count(a)==n,(s.count(a),a[:90]);s=s.replace(a,b)

rep('<title>Singularity – Prototype V3</title>','<title>Singularity – V4 (dev)</title>')
rep("const GAME_KEY='singularity-v3-dev';","const GAME_KEY='singularity-v4-dev';")

# ---------- card abilities now act on rival universes ----------
for old,new in [
 ("ab:'Ether Coil – overloads a rival generator for 2 turns.'","ab:'Ether Coil – overloads all of a rival\\'s generators for 2 turns.'"),
 ("ab:'Radiant Trace – reveals a rival\\'s crystal stock.'","ab:'Radiant Trace – steals 2 crystals from a rival.'"),
 ("ab:'Relative Frame – learns a rival\\'s research goal.'","ab:'Relative Frame – copies one of a rival\\'s inventions.'"),
 ("ab:'Complementarity – a failed mission is never traced back to you.'","ab:'Complementarity – a rival loses 15 % control.'"),
 ("ab:'Fission – halves a rival\\'s next crystal yield.'","ab:'Fission – halves a rival\\'s crystal yield for 2 turns.'"),
 ("ab:'Skyward – delays a rival facility under construction by 1 turn.'","ab:'Skyward – delays all of a rival\\'s construction by 1 turn.'"),
 ("ab:'Invariant – reveals which anchors a rival holds.'","ab:'Invariant – learns where a rival\\'s anchors are and watches them for 8 turns.'"),
 ("ab:'Redshift – shows a rival\\'s instability trend.'","ab:'Redshift – pushes a rival\\'s instability up by 5 %.'")]:
  rep(old,new)
rep("if(S.counterRes===S.round)cr=0;","if(S.counterRes===S.round)cr=0;if(S.fissionUntil>S.round)cr*=.5;")

# ---------- persistence: player + rivals ----------
rep("function save(){try{localStorage.setItem('singularity-v3-dev',JSON.stringify(S))}catch(e){}}",
    "function save(){if(BOT)return;try{localStorage.setItem('singularity-v4-dev',JSON.stringify({S,R:MV?MV.rivals:[],rel:MV?MV.rel:[],pact:MV?MV.pact:[],intel:MV?MV.intel:[],contact:MV?MV.contact:[],news:MV?MV.news:[],rep:MV?MV.rep:''}))}catch(e){}}")
rep("function load(){try{const j=localStorage.getItem('singularity-v3-dev');if(j){S=JSON.parse(j);",
    "function load(){try{const j=localStorage.getItem('singularity-v4-dev');if(j){const o=JSON.parse(j);S=o.S;if(!S||!o.R||!o.R.length){S=null;return false}MV={me:S,rivals:o.R,rel:o.rel,pact:o.pact,intel:o.intel,contact:o.contact||o.R.map(()=>false),news:o.news||[],rep:o.rep||''};")
rep("function newGame(seed,endless,diff){","function newGame(seed,endless,diff,nriv){")
rep(" S.paper={title:'The Bureau Awakens',"," if(!BOT)makeRivals(nriv||2,endless,diff,seed);\n S.paper={title:'The Bureau Awakens',")
rep("['Dr. Crane\\'s notebook',","['Other universes',`${MV?MV.rivals.length:0} rival bureau${MV&&MV.rivals.length>1?'s':''} in neighbouring universes race us for the same ten anchors – see the Rivals tab. Only one Manhattan will survive.`],['Dr. Crane\\'s notebook',")

# ---------- turn order: rivals first, then the player ----------
rep("function render(){\n computePower();","function render(){\n if(BOT)return;\n computePower();")
rep("function showPaper(){","function showPaper(){\n if(BOT)return;")
rep("$('end').onclick=endRound;","$('end').onclick=endTurn;")
rep("if(S.over&&S.over!=='quit'){S.score=gameScore();if(S.endless)try{","if(S.over&&S.over!=='quit'){S.score=gameScore();if(S.endless&&!BOT)try{")
rep("  if(!S.endless&&Object.keys(S.anchors).length>=winNeed())S.over='win';\n }",
"""  if(!S.endless&&Object.keys(S.anchors).length>=winNeed())S.over='win';
  if(!BOT&&MV&&!S.endless){const rw=MV.rivals.filter(r=>r.over==='win');if(rw.length){const best=Math.max(...rw.map(r=>Object.keys(r.anchors).length));if(S.over!=='win'||best>Object.keys(S.anchors).length){S.over='lose-rival';S.rivalWin=rw.find(r=>Object.keys(r.anchors).length===best).bot.name}}}
 }""")
rep(" if(!msgs.length)msgs.push(['Quiet weeks','The city goes about its business.']);",
    " if(!BOT&&MV&&MV.news.length)msgs.unshift(...MV.news.splice(0));\n if(!msgs.length)msgs.push(['Quiet weeks','The city goes about its business.']);")
rep("function endTitle(){return S.over==='win'?'The Universe Holds':'The Singularity'}",
    "function endTitle(){return S.over==='win'?'The Universe Holds':S.over==='lose-rival'?'Another Manhattan Prevails':'The Singularity'}")
rep(" if(S.over==='lose-inst')return[['Collapse',",
    " if(S.over==='lose-rival')return[['Another universe prevails',`${S.rivalWin} held enough anchors first. Their Manhattan is the one that remains – yours fades into the ether.`],['Score',`${S.score} points.`]];\n if(S.over==='lose-inst')return[['Collapse',")

# ---------- shared anchors ----------
rep("function activate(id){const a=ANCHORS.find(a=>a.id===id);if(!S.found[id]||",
    "function activate(id){const a=ANCHORS.find(a=>a.id===id);const ow=ownerOf(id);if(ow&&ow!==S)return;if(!S.found[id]||")

# ---------- the V4 module ----------
JS=r"""
// ===================== V4: rival universes =====================
// Every rival is a complete game state (same rules, own map) that a bot plays. The player's state is MV.me;
// while a bot plays, the global S points at that rival and BOT is true (no rendering, no saving).
let MV=null,BOT=false;
const RIVAL_DEF=[
 {u:'β',name:'Universe β',lead:'Director Ada Thornfield',pers:'scholar'},
 {u:'γ',name:'Universe γ',lead:'Commissioner Elias Rusk',pers:'saboteur'},
 {u:'δ',name:'Universe δ',lead:'Madame Iris Vale',pers:'mystic'},
 {u:'ε',name:'Universe ε',lead:'Mr. Cornelius Hale',pers:'industrialist'}];
const RCOL={'β':'#e8504a','γ':'#4a90ff','δ':'#b070ff','ε':'#f0c63a'};
function rcol(u){return u&&u.bot?RCOL[u.bot.u]:'#5fd4e0'}
const PERS={
 scholar:{n:'Scholar',d:'Researches relentlessly, rarely attacks.',mis:.08,build:['lab','lab','sender','drill','stab'],spy:.8},
 saboteur:{n:'Saboteur',d:'Sends agents against whoever leads.',mis:.35,build:['lab','sender','drill','gen','front'],spy:.3},
 mystic:{n:'Mystic',d:'Psy power and ether – hunts the rift anchors.',mis:.15,build:['sender','lab','drill','drill','stab'],spy:.5},
 industrialist:{n:'Industrialist',d:'Money and power plants, trades gladly.',mis:.12,build:['front','gen','lab','drill','tesla'],spy:.5}};
const BOT_SKILL={easy:.55,normal:.75,hard:1};
function makeRivals(n,endless,diff,seed){const me=S;const r0=rng((seed||me.seed)+77);
 const defs=RIVAL_DEF.slice().sort(()=>r0()-.5).slice(0,Math.max(1,Math.min(3,n)));
 const rivals=defs.map((d,i)=>{BOT=true;try{newGame(Math.floor(r0()*1e9),endless,'hard');S.bot=d;S.rid=i;S.skill=BOT_SKILL[diff]||.8;return S}finally{BOT=false}}); // rivals always play by the hard rules; the difficulty only sets how well they play
 S=me;MV={me,rivals,rel:rivals.map(()=>0),pact:rivals.map(()=>-1),intel:rivals.map(()=>-1),contact:rivals.map(()=>false),news:[],rep:''}}
function asRival(r,fn){const me=S;BOT=true;S=r;try{return fn()}finally{S=me;BOT=false}}
function allU(){return MV?[MV.me,...MV.rivals]:[S]}
function uName(u){return u===MV.me?'your bureau':u.bot.name}
function ownerOf(id){if(!MV)return S.anchors[id]!==undefined?S:null;return allU().find(u=>!(u!==MV.me&&u.over)&&u.anchors[id]!==undefined)||null}
function rivIdx(u){return MV.rivals.indexOf(u)}
function pactOn(i){return MV.pact[i]>MV.me.round}
// what the player knows about a rival's anchors: permanent contact (pact or trade) or fresh intel from spying
function knows(i){return !!(MV.contact[i]||pactOn(i)||MV.intel[i]>=MV.me.round)}
function knowsU(u){return u===MV.me||knows(rivIdx(u))}
function seizeCost(a){return Math.ceil(ancCost(a)*1.5)}
function seize(id){const a=ANCHORS.find(x=>x.id===id),o=ownerOf(id);if(!o||o===S||!S.found[id]||!a.test(S)||S.crystals<seizeCost(a)||S.over)return;
 if(S!==MV.me&&o===MV.me&&pactOn(rivIdx(S)))return;
 if(S===MV.me&&pactOn(rivIdx(o))){MV.pact[rivIdx(o)]=-1;MV.rel[rivIdx(o)]-=40}
 S.crystals-=seizeCost(a);delete o.anchors[id];S.anchors[id]=S.round;
 if(o===MV.me)MV.news.push(['Anchor seized!',`${S.bot.name} has torn the <b>${a.name}</b> away from us. We can take it back if we meet its condition again.`]);
 else if(S===MV.me){MV.rel[rivIdx(o)]-=15;MV.rep=`You seized the ${a.name} from ${o.bot.name}.`}
 save();render()}
// ---- missions: spy / sabotage / the card's ability ----
const MISSION_PSY=10;
function missionChance(sci,type,dst){const c=SCI_CARD[sci];const v=type==='spy'?c.spy:type==='sab'?c.sab:Math.max(c.spy,c.sab)-1;return clamp(.3+.09*v-.004*dst.c.kontrolle,.1,.9)}
function doMission(src,dst,sci,type){const c=SCI_CARD[sci],ok=Math.random()<missionChance(sci,type,dst),traced=!ok||Math.random()<.25;
 const me=MV.me,si=rivIdx(src),di=rivIdx(dst);let what='';
 if(ok){
  if(type==='spy'){const ids=Object.keys(dst.inv).filter(id=>!src.inv[id]&&!src.known.includes(id));if(ids.length){const id=ids[Math.floor(Math.random()*ids.length)];src.known.push(id);what=`stole the recipe for <b>${INV[id].n}</b>`}else what='found nothing new in their labs';if(src===me)MV.intel[di]=me.round+6}
  else if(type==='sab'){const fs=[];for(const k in dst.slots)dst.slots[k].forEach(f=>{if(f&&!(f.bt>0)&&!f.off)fs.push([k,f])});if(fs.length){const [k,f]=fs[Math.floor(Math.random()*fs.length)];f.off=2;what=`knocked out the ${FAC[f.t].name} in ${DISTRICTS[k].name} for 2 turns`}else what='found nothing worth sabotaging';dst.inst=clamp(dst.inst+2,0,100)}
  else switch(c.id){
   case'tesla':{let n=0;for(const k in dst.slots)dst.slots[k].forEach(f=>{if(f&&(f.t==='gen'||f.t==='tesla'||f.t==='core')){f.off=2;n++}});what=`overloaded ${n} generator${n===1?'':'s'}`;break}
   case'curie':{const n=Math.min(2,Math.floor(dst.crystals));dst.crystals-=n;src.crystals+=n;what=`stole ${n} crystal${n===1?'':'s'}`;break}
   case'einstein':{const ids=Object.keys(dst.inv).filter(id=>!src.inv[id]);if(ids.length){const id=ids[Math.floor(Math.random()*ids.length)];src.inv[id]=src.round+1;what=`copied the <b>${INV[id].n}</b>`}else what='found no invention to copy';break}
   case'bohr':dst.c.kontrolle=Math.max(0,dst.c.kontrolle-15);what='undermined their control (−15 %)';break;
   case'meitner':dst.fissionUntil=dst.round+2;what='halved their crystal yield for 2 turns';break;
   case'goddard':{let n=0;for(const k in dst.slots)dst.slots[k].forEach(f=>{if(f&&f.bt>0){f.bt++;n++}});what=n?`delayed ${n} construction site${n>1?'s':''}`:'found no construction to delay';break}
   case'noether':{const ids=Object.keys(dst.anchors).concat(Object.keys(dst.found)).filter(id=>!src.found[id]);if(ids[0])src.found[ids[0]]=true;if(src===me)MV.intel[di]=me.round+8;what=ids[0]?`located the ${ANCHORS.find(a=>a.id===ids[0]).name}`:'mapped their anchors';break}
   case'hubble':dst.inst=clamp(dst.inst+5,0,100);what='pushed their instability up by 5 %';break}
 }
 const T={spy:'Espionage',sab:'Sabotage',ab:c.ab.split(' – ')[0]}[type];
 if(src===me){const rv=dst.bot.name;
  if(pactOn(di)){MV.pact[di]=-1;MV.rel[di]-=40}
  if(traced)MV.rel[di]-=ok?10:20;
  if(!ok)me.attention+=6;
  MV.rep=ok?`<b>${T}</b> against ${rv}: ${sci} ${what}.${traced?' But we were spotted.':''}`:`<b>${T}</b> against ${rv} failed – ${sci} was spotted. Relations suffer.`}
 else if(dst===me){
  if(traced)MV.rel[si]-=10;
  if(ok)MV.news.push([`${T}!`,`${traced?src.bot.name:'Unknown agents'} ${what.replace(/their /g,'our ')}.`]);
  else MV.news.push(['Agents caught',`Our counter-intelligence caught agents from ${src.bot.name}. Relations cool.`])}
}
function playerMission(sci,i,type){const dst=MV.rivals[i];if(!dst||dst.over||S.over||S.psy<MISSION_PSY||(S.mcd&&S.mcd[sci]>S.round)||!S.sci.includes(sci))return;
 S.psy-=MISSION_PSY;(S.mcd=S.mcd||{})[sci]=S.round+3;doMission(S,dst,sci,type);save();render()}
// ---- diplomacy ----
function proposePact(i){const r=MV.rivals[i];if(r.over||pactOn(i))return;const need=r.bot.pers==='saboteur'?30:0;
 if(MV.rel[i]>=need){MV.pact[i]=S.round+8;MV.contact[i]=true;MV.rel[i]+=5;MV.rep=`${r.bot.lead} signs a non-aggression pact for 8 turns.`}else{MV.rel[i]-=3;MV.rep=`${r.bot.lead} refuses a pact. They do not trust us (yet).`}save();render()}
function tradeCost(){return count(S,'portal')?1:2}
function trade4(i,kind){const r=MV.rivals[i];if(r.over||S.over)return;const ok=MV.rel[i]>=-20;let msg='';
 if(kind==='buy'){if(S.money<3500)return;if(ok&&r.crystals>=6||r.bot.pers==='industrialist'&&r.crystals>=4){S.money-=3500;r.money+=3500;r.crystals-=2;S.crystals+=2;msg='sells us 2 crystals for $3,500'}}
 else if(kind==='sell'){if(S.crystals<2)return;if(ok&&r.money>=6000){S.crystals-=2;r.crystals+=2;r.money-=2800;S.money+=2800;msg='buys 2 crystals for $2,800'}}
 else if(kind==='swap'){const give=Object.keys(S.inv).find(id=>!r.inv[id]&&!r.known.includes(id)),get=Object.keys(r.inv).find(id=>!S.inv[id]&&!S.known.includes(id));
  if(give&&get&&(MV.rel[i]>=10||r.bot.pers==='scholar'&&MV.rel[i]>=0)){r.known.push(give);S.known.push(get);msg=`swaps recipes: we give the ${INV[give].n}, we get the <b>${INV[get].n}</b>`}else if(!give||!get){MV.rep='There is no recipe to swap right now.';save();render();return}}
 if(msg){MV.rel[i]+=6;MV.contact[i]=true;S.inst=clamp(S.inst+tradeCost(),0,100);MV.rep=`${r.bot.name} ${msg}. Crossing the rift costs ${tradeCost()} % instability.`}else{MV.rel[i]-=1;MV.rep=`${r.bot.lead} declines the offer.`}
 save();render()}
// ---- the bot ----
function botPlay(){const B=S.bot,PS=PERS[B.pers],rnd=rng(S.seed+S.round*977);if(rnd()>(S.skill||1))return;
 // research: work towards known recipes, sometimes search anchors, otherwise study broadly
 if(!inv('damper')&&S.inst>22){if(S.prin.res<1)S.resTarget='p:res';else if(S.rp>=3)experiment(['eth','res'])} // every bureau learns to stabilise once the rift gets loud
 const kn=S.known.find(id=>!S.inv[id]&&INV[id].era<=era());
 if(kn){const ps=Object.keys(INV[kn].r);if(ps.every(p=>S.prin[p]>=INV[kn].r[p]))experiment(ps);else S.resTarget='p:'+ps.find(p=>S.prin[p]<INV[kn].r[p])}
 for(let k=0;k<2&&S.rp>=9;k++){const av=Object.keys(PRIN).filter(p=>S.prin[p]>=1);const a=av[Math.floor(rnd()*av.length)],b=av[Math.floor(rnd()*av.length)];if(a!==b)experiment([a,b])}
 if(ANCHORS.some(a=>!S.found[a.id])&&S.round>=4&&S.round%3===0&&(S.inv.wardenclyffe||S.round>20))S.resTarget='anchor';
 else if(!kn&&(!S.resTarget||S.resTarget==='anchor'||S.prin[S.resTarget.slice(2)]>=3)){const ps=Object.keys(PRIN).filter(p=>S.prin[p]<3).sort((a,b)=>S.prin[a]-S.prin[b]);if(ps.length)S.resTarget='p:'+ps[Math.floor(rnd()*Math.min(3,ps.length))]}
 // anchors: activate free ones, seize from others when rich in crystals
 ANCHORS.forEach(a=>{if(!S.found[a.id]||!a.test(S))return;const o=ownerOf(a.id);if(!o)activate(a.id);else if(o!==S&&S.crystals>=seizeCost(a)+3)seize(a.id)});
 // money trouble
 if(S.money<0&&!S.loan)takeLoan();
 if(S.money<-2000){const id=Object.keys(S.inv).find(x=>!S.patent[x]);if(id)sellPatent(id)}
 // build: needs first, then the personality's favourites
 const need=[];const found=id=>S.found[id]&&ownerOf(id)!==S;
 if(S.mw.prod-S.mw.use<15)need.push(has('coil')&&S.crystals>=4?'tesla':'gen');
 if(S.inst>28&&has('damper'))need.push('stab');
 if(S.inst>45&&has('cooltower')&&S.crystals>=3)need.push('cooler');
 if(found('chrysler')&&has('coil')&&count(S,'tesla')<AT().tesla&&S.crystals>=2)need.push('tesla');
 if(found('esb')&&has('portalgeo')&&!count(S,'portal')&&S.crystals>=5)need.push('portal');
 if(found('park')&&S.slots.park.filter(f=>f&&f.t==='drill').length<2)need.push('drill');
 if(S.crystals<8)need.push('drill');
 need.push(...PS.build);
 let builds=S.money>30000?2:1;
 for(const t of need){if(!builds)break;if(!has(FAC[t].req))continue;const cost=FAC[t].cost;if(S.money<cost+4000||S.crystals<FAC[t].k)continue;
  const order=t==='drill'?['park','harlem','les','village']:['les','fidi','midtown','times','village','harlem','park','hells'];
  const k=order.filter(d=>S.slots[d].includes(null)&&!(t==='front'&&S.slots[d].some(f=>f&&f.t==='front'))).sort((a,b)=>(S.slots[a].some(f=>f)?1:0)-(S.slots[b].some(f=>f)?1:0))[0];
  if(k){build(k,S.slots[k].indexOf(null),t);builds--}}
 if(S.money>20000)for(const k in S.slots)S.slots[k].forEach((f,i)=>{if(f&&!(f.bt>0))Object.keys(INV).filter(id=>INV[id].t==='M'&&inv(id)&&INV[id].fit.includes(f.t)).forEach(id=>installMod(k,i,id))});
 // psy
 if(S.c.unruhe>55&&S.psy>=5)usePsy(null,'calm');
 if((found('brooklyn')||found('grand'))&&S.c.kontrolle<AT().brook&&S.psy>=10+MISSION_PSY)usePsy(null,'whisper');
 if(S.c.loyal<45&&has('neon')&&S.psy>=8)usePsy(null,'inspire');
 if(found('times')&&S.psy<AT().psy)return; // saves psy for Times Square
 // missions against the strongest universe that is not protected by a pact
 if(S.sci.length&&S.psy>=MISSION_PSY&&rnd()<PS.mis){const me=S,si=rivIdx(me);
  const tg=allU().filter(u=>u!==me&&!(u!==MV.me&&u.over)&&!(u===MV.me&&pactOn(si))).sort((a,b)=>Object.keys(b.anchors).length-Object.keys(a.anchors).length+(a===MV.me?-MV.rel[si]/40:0))[0];
  const sci=S.sci.find(n=>!(S.mcd&&S.mcd[n]>S.round));
  if(tg&&sci){S.psy-=MISSION_PSY;(S.mcd=S.mcd||{})[sci]=S.round+4;const type=B.pers==='saboteur'?(rnd()<.5?'sab':'ab'):B.pers==='scholar'?'spy':['spy','sab','ab'][Math.floor(rnd()*3)];doMission(me,tg,sci,type)}}
}
function endTurn(){if(S.over)return;
 MV.rivals.forEach(r=>{if(r.over)return;asRival(r,()=>{botPlay();endRound()});
  if(r.over==='lose-inst'){const freed=Object.keys(r.anchors).map(id=>ANCHORS.find(a=>a.id===id).name);r.anchors={};MV.news.push([`${r.bot.name} collapses`,`The rift swallows ${r.bot.lead}'s Manhattan.${freed.length?' Its anchors are free again: '+freed.join(', ')+'.':''}`])}});
 MV.rel=MV.rel.map(v=>clamp(v+(v<0?1:v>0?-1:0),-100,100));
 endRound()}
function rivalStrip(){if(!MV)return'';return MV.rivals.map((r,i)=>{const a=Object.keys(r.anchors).length;return`<div class="rv ${r.over?'dead':''}" style="--rc:${rcol(r)}" title="${r.bot.name} – ${r.bot.lead}"><b>${r.bot.u}</b><span class="rvb"><i style="width:${r.inst}%"></i></span><em>${r.over?'collapsed':knows(i)?a+'⚓':'?⚓'}</em></div>`}).join('')}
"""
rep("// ===== V3: agent name + online Hall of Fame",JS+"// ===== V3: agent name + online Hall of Fame")

# ---------- UI: tabs ----------
rep('      <button data-t="sci">SCIENTISTS</button>','      <button data-t="sci">AGENTS</button>')
rep('      <button data-t="zeitung">NEWS</button>','      <button data-t="rivals">RIVALS</button>\n      <button data-t="zeitung">NEWS</button>')
rep('<div class="bar"><i id="instb"></i></div>','<div class="bar"><i id="instb"></i></div><div class="rivstrip" id="rivstrip"></div>')
rep(" $('instv').textContent=Math.round(S.inst)+' %';"," $('rivstrip').innerHTML=rivalStrip();\n $('instv').textContent=Math.round(S.inst)+' %';")

# agents tab: cards with missions
rep("""  let h=`<div class="dhero" style="--img:url(art/all.webp);margin-top:-14px"><h2>SCIENTISTS</h2></div>""",
    """  let h=`<div class="dhero" style="--img:url(art/all.webp);margin-top:-14px"><h2>AGENTS</h2></div>${MV&&MV.rep?`<p class="mrep">${MV.rep}</p>`:''}""")
rep("""  h+=`<div class="scards">${S.sci.map(n=>`<div class="swrap">${sciCard(n)}<div class="sfield">★ ${(SCI_PRIN[n]||[]).map(q=>pic(q,'sm')+' '+PRIN[q].n).join(' · ')}</div></div>`).join('')}""",
    """  const alive=MV?MV.rivals.map((r,i)=>[r,i]).filter(([r])=>!r.over):[];window.MTARGET=alive.some(([r,i])=>i===window.MTARGET)?window.MTARGET:(alive[0]||[])[1];
  if(alive.length&&S.sci.length)h+=`<div class="mtarget"><span>Missions against</span>${alive.map(([r,i])=>`<button class="tbtn ${i===window.MTARGET?'on':''}" style="--rc:${rcol(r)}" data-mt="${i}">${r.bot.name}${pactOn(i)?' 🤝':''}</button>`).join('')}<small>Each mission costs ${MISSION_PSY} psy. Missions against a pact partner break the pact.</small></div>`;
  const tg=MV&&MV.rivals[window.MTARGET];
  h+=`<div class="scards">${S.sci.map(n=>{const cd=S.mcd&&S.mcd[n]>S.round?S.mcd[n]-S.round:0;return`<div class="swrap">${sciCard(n)}<div class="sfield">★ ${(SCI_PRIN[n]||[]).map(q=>pic(q,'sm')+' '+PRIN[q].n).join(' · ')}</div>`+(tg?`<div class="mbtns">${cd?`<small>Back in ${cd} turn${cd>1?'s':''}</small>`:['spy','sab','ab'].map(t=>`<button class="btn small" data-ms="${t}:${n}" ${S.psy>=MISSION_PSY&&!S.over?'':'disabled'} title="${t==='ab'?SCI_CARD[n].ab:t==='spy'?'Steal a recipe and watch them for 6 turns':'Knock out a facility for 2 turns, +2 % instability'}">${t==='spy'?'Spy':t==='sab'?'Sabotage':SCI_CARD[n].ab.split(' – ')[0]} <small>${Math.round(missionChance(n,t,tg)*100)} %</small></button>`).join('')}</div>`:'')+`</div>`}).join('')}""")
rep("""  h+=`<h3>On staff (${S.sci.length}/${maxSci()})</h3>`+(S.sci.length?'':'<p class="note">None yet.</p>');""",
    """  h+=`<h3>On staff (${S.sci.length}/${maxSci()})</h3>`+(S.sci.length?'':'<p class="note">None yet. Once a scientist joins, you can send them on missions against rival universes.</p>');""")
rep("""${SCIENTISTS.filter(x=>!S.sci.includes(x.name)).map(sciBack).join('')}</div>`;
  p.innerHTML=h;
 }""","""${SCIENTISTS.filter(x=>!S.sci.includes(x.name)).map(sciBack).join('')}</div>`;
  p.innerHTML=h;
  p.querySelectorAll('[data-mt]').forEach(b=>b.onclick=()=>{window.MTARGET=+b.dataset.mt;render()});
  p.querySelectorAll('[data-ms]').forEach(b=>b.onclick=()=>{const [t,n]=b.dataset.ms.split(':');playerMission(n,window.MTARGET,t)});
 }
 if(tab==='rivals'){
  let h=`<div class="dhero" style="--img:url(art/inv_worldbridge.webp);margin-top:-14px"><h2>RIVALS</h2></div>${MV.rep?`<p class="mrep">${MV.rep}</p>`:''}<p class="note">Bureaus in neighbouring universes race you for the same ten anchors. Whoever holds ${S.endless?'the most':winNeed()} at the end of an epoch survives. Trades cross the rift: ${tradeCost()} % instability each${count(S,'portal')?' (your portal halves it)':' (a portal would halve it)'}.</p>`;
  MV.rivals.forEach((r,i)=>{const an=Object.keys(r.anchors),seen=MV.intel[i]>=S.round,rel=MV.rel[i],pact=pactOn(i);
   h+=`<div class="rcard ${r.over?'dead':''}" style="--rc:${rcol(r)}"><div class="rtop"><b>${r.bot.u}</b><div><h4>${r.bot.name}</h4><small>${r.bot.lead} · ${PERS[r.bot.pers].n}</small></div></div>`+
   (r.over?`<p class="note">Collapsed into the Singularity.</p></div>`:
   `<p class="note">${PERS[r.bot.pers].d}</p><div class="rstats"><span>Anchors <b>${knows(i)?an.length:'?'}</b></span><span>Instability <b>${Math.round(r.inst)} %</b></span><span>Facilities <b>${totalFac(r)}</b></span>`+
   (seen?`<span>Money <b>$${fmt(r.money)}</b></span><span>Crystals <b>${Math.floor(r.crystals)}</b></span><span>Inventions <b>${Object.keys(r.inv).length}</b></span><span>Knowledge <b>${know(r)}</b></span><span>Scientists <b>${r.sci.length}</b></span>`:`<span class="nointel">Spy on them to see more</span>`)+`</div>`+
   (!knows(i)?`<p class="note nocon">No connection yet – sign a pact, trade with them or spy on them to learn which anchors they hold.</p>`:an.length?`<p class="ranch">Holds: ${an.map(id=>ANCHORS.find(a=>a.id===id).name).join(', ')}${MV.contact[i]||pactOn(i)?'':' <small>(spy report)</small>'}</p>`:'<p class="note">Holds no anchors.</p>')+
   `<div class="relbar"><span>Relations</span><i><em style="left:${50+rel/2}%"></em></i><b>${rel>20?'friendly':rel<-20?'hostile':'neutral'}</b>${pact?`<small>🤝 pact until turn ${MV.pact[i]+1}</small>`:''}</div>`+
   `<div class="btns">${pact?'':`<button class="btn small" data-dip="pact:${i}">Propose a pact<small>8 turns without missions</small></button>`}<button class="btn small" data-dip="buy:${i}" ${S.money>=3500?'':'disabled'}>Buy 2 crystals<small>$3,500</small></button><button class="btn small" data-dip="sell:${i}" ${S.crystals>=2?'':'disabled'}>Sell 2 crystals<small>+$2,800</small></button><button class="btn small" data-dip="swap:${i}">Swap a recipe<small>one invention each</small></button></div></div>`)});
  p.innerHTML=h;
  p.querySelectorAll('[data-dip]').forEach(b=>b.onclick=()=>{const [k,i]=b.dataset.dip.split(':');if(k==='pact')proposePact(+i);else trade4(+i,k)});
 }""")

# anchors tab: owner + seize
rep("""const act=S.anchors[a.id]!==undefined;const ok=a.test(S);
   h+=`<div class="acard ${act?'active':ok?'ok':''}" style="--img:url(art/anc_${a.id}.webp)"><div class="aact">${act?'<span class="abadge">ACTIVE</span>':`<button class="btn small" data-a="${a.id}" ${ok&&S.crystals>=ancCost(a)?'':'disabled'}>Activate ◆${ancCost(a)}</button>`}</div><b>${a.name}</b><span class="c">${a.kind} · ${a.cond} ${ok?'✓':''}</span></div>`});""",
"""const act=S.anchors[a.id]!==undefined;const ok=a.test(S);const ow=ownerOf(a.id),theirs=ow&&ow!==S;
   h+=`<div class="acard ${act?'active':theirs?'theirs':ok?'ok':''}" style="--img:url(art/anc_${a.id}.webp)"><div class="aact">${act?'<span class="abadge">ACTIVE</span>':theirs?`<button class="btn small" data-seize="${a.id}" ${ok&&S.crystals>=seizeCost(a)?'':'disabled'} title="Meet the condition and pay 50 % more crystals to take it">Seize ◆${seizeCost(a)}</button>`:`<button class="btn small" data-a="${a.id}" ${ok&&S.crystals>=ancCost(a)?'':'disabled'}>Activate ◆${ancCost(a)}</button>`}</div><b>${a.name}</b><span class="c">${theirs?`${knowsU(ow)?`<em class="aown" style="color:${rcol(ow)}">held by ${ow.bot.name}</em>`:'<em class="aown">held by another universe</em>'} · `:''}${a.kind} · ${a.cond} ${ok?'✓':''}</span></div>`});""")
rep("  p.innerHTML=h;p.querySelectorAll('[data-a]').forEach(b=>b.onclick=()=>activate(b.dataset.a));",
    "  p.innerHTML=h;p.querySelectorAll('[data-a]').forEach(b=>b.onclick=()=>activate(b.dataset.a));p.querySelectorAll('[data-seize]').forEach(b=>b.onclick=()=>seize(b.dataset.seize));")

# map: anchors held by rivals get a violet light pillar
rep("  for(const a of ANCHORS)if(S.anchors[a.id]!==undefined&&a.pos){const p=P(a.pos[0]+.5,a.pos[1]+.5);pillar(p[0],p[1],120,8,'#5fd4e0',",
    "  for(const a of ANCHORS){const ow=MV&&ownerOf(a.id);if(ow&&ow!==S&&a.pos&&knowsU(ow)){const p=P(a.pos[0]+.5,a.pos[1]+.5);pillar(p[0],p[1],90,6,rcol(ow),.3+.08*Math.sin(t*2+a.pos[1]))}}\n  for(const a of ANCHORS)if(S.anchors[a.id]!==undefined&&a.pos){const p=P(a.pos[0]+.5,a.pos[1]+.5);pillar(p[0],p[1],120,8,'#5fd4e0',")

# Crane warns about rivals
rep(" const out=t.slice(0,2);"," if(MV){const lead=MV.rivals.filter((r,i)=>!r.over&&knows(i)).sort((a,b)=>Object.keys(b.anchors).length-Object.keys(a.anchors).length)[0];if(lead&&!S.endless&&Object.keys(lead.anchors).length>=winNeed()-1)t.unshift(`<b>${lead.bot.name}</b> holds ${Object.keys(lead.anchors).length} anchors – one more and they may win at the end of the epoch! Seize one of theirs or sabotage them.`)}\n const out=t.slice(0,2);")

# mode selection: number of rivals
rep("function curDiff(){","function curRiv(){try{const n=+localStorage.getItem('singularity-v4-riv');if(n>=1&&n<=3)return n}catch(e){}return 2}\nfunction curDiff(){")
rep(" <div class=\"mscards\">"," <div class=\"msriv\"><span>Rival universes</span>${[1,2,3].map(n=>`<button class=\"rbtn ${n===curRiv()?'on':''}\" data-riv=\"${n}\">${n}</button>`).join('')}</div>\n <div class=\"mscards\">")
rep("  newGame(0,md==='endless',curDiff());showPaper();render()});","  newGame(0,md==='endless',curDiff(),curRiv());showPaper();render()});\n m.querySelectorAll('[data-riv]').forEach(b=>b.onclick=()=>{try{localStorage.setItem('singularity-v4-riv',b.dataset.riv)}catch(e){}openModeSel(canContinue)});")
rep("$('ng').onclick=()=>{newGame();showPaper();render()};$('ngE').onclick=()=>{newGame(0,true);showPaper();render()};",
    "$('ng').onclick=()=>openModeSel(!S.over);$('ngE').onclick=()=>openModeSel(!S.over);")

CSS="""
/* ===== V4: rivals ===== */
.rivstrip{display:flex;flex-direction:column;gap:3px;margin:6px 0 2px}.rv{display:grid;grid-template-columns:16px 1fr 58px;align-items:center;gap:6px;font:11px 'Federo',serif;color:#cfc6b2}
.rv b{color:var(--rc,#c9a0ff);font-size:13px;text-shadow:0 0 6px var(--rc)}.rvb{height:5px;background:#1a1d20;border:1px solid #3a3122}.rvb i{display:block;height:100%;background:linear-gradient(90deg,#7fd68a,#e0c040,#f06a6a)}.rv em{font-style:normal;text-align:right;color:var(--rc,#c9a0ff)}.rv.dead{opacity:.4}
.mrep{background:rgba(60,48,22,.35);border-left:3px solid #e2c480;padding:7px 10px;font-size:12.5px;line-height:1.45;color:#ece4d0}
.mtarget{display:flex;flex-wrap:wrap;align-items:center;gap:5px;margin:6px 0 10px;font:12px 'Federo',serif;color:#cfc6b2}.mtarget small{flex-basis:100%;font:11px 'Josefin Sans',sans-serif;color:#8d877b}
.tbtn{padding:4px 9px;background:rgba(10,13,15,.85);border:1px solid #3a3122;color:#cfc6b2;cursor:pointer;font:12px 'Federo',serif}.tbtn{border-left:3px solid var(--rc,#3a3122)!important}.tbtn.on{border-color:var(--rc,#c9a0ff);color:#fff;background:rgba(255,255,255,.08);box-shadow:0 0 8px var(--rc)}
.mbtns{display:flex;flex-direction:column;gap:3px}.mbtns .btn{font-size:10.5px!important;padding:4px!important}.mbtns .btn small{display:inline;color:#9ff0b0}.mbtns>small{text-align:center;color:#8d877b;font-size:11px}
.rcard{border:1px solid #3a3122;border-left:4px solid var(--rc,#3a3122);background:linear-gradient(#12171a,#0a0d0f);padding:10px;margin:0 0 12px}.rcard.dead{opacity:.5}
.rtop{display:flex;gap:10px;align-items:center}.rtop>b{font:400 30px 'Federo',serif;color:var(--rc,#c9a0ff);text-shadow:0 0 10px var(--rc);width:36px;text-align:center}.rtop h4{margin:0;font:400 15px 'Federo',serif;letter-spacing:1px;color:#e2c480}.rtop small{color:#8d877b;font-size:11px}
.rstats{display:grid;grid-template-columns:1fr 1fr;gap:2px 10px;font-size:12px;margin:6px 0}.rstats b{color:#e2c480;float:right}.nointel{grid-column:span 2;color:#8d877b;font-style:italic}
.ranch{font-size:12px;color:var(--rc,#c9a0ff);margin:4px 0}
.relbar{display:flex;align-items:center;gap:8px;font-size:11px;color:#8d877b;margin:6px 0}.relbar i{position:relative;flex:1;height:6px;background:linear-gradient(90deg,#f06a6a,#55585e,#7fd68a)}.relbar em{position:absolute;top:-3px;width:3px;height:12px;background:#fff;transform:translateX(-1px)}.relbar b{color:#cfc6b2;font-weight:400}.relbar small{flex-basis:100%}
.acard.theirs{filter:saturate(.7)}.aown{font-style:normal;color:#c9a0ff}
.msriv{display:flex;align-items:center;justify-content:center;gap:8px;margin:0 0 14px;font:14px 'Federo',serif;letter-spacing:2px;color:#cfc6b2}
.rbtn{width:44px;height:36px;background:rgba(10,13,15,.85);border:1px solid #3a3122;color:#cfc6b2;font:18px 'Federo',serif;cursor:pointer}.rbtn.on{border-color:#c9a0ff;color:#fff;background:rgba(90,60,140,.35);box-shadow:0 0 10px rgba(192,112,255,.3)}
"""
idx=s.rindex("</style>",0,s.index("<body"));s=s[:idx]+CSS+s[idx:]
rep(" const send=submit&&"," const send=false&&submit&&") # Dev Edition: games never reach the live Hall of Fame
rep('<title>Singularity – V4 (dev)</title>','<title>Singularity – V4 Dev Edition</title>')
rep('style="vertical-align:middle;margin:-6px 8px -6px 0">SINGULARITY</div>','style="vertical-align:middle;margin:-6px 8px -6px 0">SINGULARITY<span class="devbadge">DEV EDITION</span></div>')
rep('<div class="mstitle">SINGULARITY</div><div class="mssub">Welcome,','<div class="mstitle">SINGULARITY</div><div class="devline">V4 · DEV EDITION · rival universes · scores are not recorded</div><div class="mssub">Welcome,')
rep("<div class=\"mstitle\">HALL OF FAME</div>${mine}","<div class=\"mstitle\">HALL OF FAME</div>${mine}<p class=\"devline\">Dev Edition – this game is not entered into the list.</p>")
s=s[:s.rindex("</style>",0,s.index("<body"))]+".devbadge{display:inline-block;margin-left:10px;padding:2px 7px;font:11px 'Federo',serif;letter-spacing:2px;color:#c9a0ff;border:1px solid #c9a0ff;vertical-align:middle;-webkit-text-fill-color:#c9a0ff}.devline{font:12px 'Federo',serif;letter-spacing:3px;color:#c9a0ff;margin:2px 0 8px}\n"+s[s.rindex("</style>",0,s.index("<body")):]
open(P,'w').write(s);print('V4 patched',len(s))
