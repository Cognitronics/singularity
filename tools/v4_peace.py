"""V4 add-on (run after v4_haarp.py): P.E.A.C.E. - Particle Ether Accelerator for Cosmic Erasure.
Stage-4 great project. Fired at a rival universe it erases that universe completely (its anchors become free),
at a heavy price: +20 % instability for the shooter, +8 % for everyone else, every survivor turns hostile,
8 turns to recharge. Bots can build and fire it too - if they erase you, the game is over."""
import sys
P=sys.argv[1] if len(sys.argv)>1 else 'site/play4/index.html'
s=open(P).read()
def rep(a,b,n=1):
  global s
  assert s.count(a)==n,(s.count(a),a[:90]);s=s.replace(a,b)

rep(" haarp:{n:'HAARP'",
    " peace:{n:'P.E.A.C.E.',era:3,r:{rad:3,eth:3,tim:2},t:'G',d:'Great project: the Particle Ether Accelerator for Cosmic Erasure – a collider that can erase an entire universe. Every shot shakes all the others'},\n haarp:{n:'HAARP'")
rep(" fbi:{name:'Federal Bureau HQ'",
    " peace:{name:'P.E.A.C.E. Collider',cost:60000,bt:8,k:12,up:1200,mw:80,col:'#ff4a3a',d:'Great project · erases a whole universe',req:'peace',spr:'fac_peace',great:true},\n fbi:{name:'Federal Bureau HQ'")
rep("left:()=>S.haarp&&S.haarp.bt}];",
    "left:()=>S.haarp&&S.haarp.bt},\n {id:'peace',stage:4,rp:40,site:'Manhattan',fac:'peace',req:()=>[['Pictureframe built',viewReady()],['Radioactivity 3',S.prin.rad>=3],['Ether 3',S.prin.eth>=3],['Time 2',S.prin.tim>=2]]}];\nGP.forEach(g=>{if(g.fac&&!g.state){g.money=()=>FAC[g.fac].cost;g.k=()=>FAC[g.fac].k;g.bt=()=>FAC[g.fac].bt;g.state=()=>builtFac(g.fac)?'done':count(S,g.fac)?'building':'';g.left=()=>facLeft(g.fac)}});")
rep("${g.id==='haarp'&&st==='done'?haarpPanel():''}","${g.id==='haarp'&&st==='done'?haarpPanel():''}${g.id==='peace'&&st==='done'?peacePanel():''}")
rep("  p.querySelectorAll('[data-wx]').forEach(",
    "  p.querySelectorAll('[data-peace]').forEach(b=>b.onclick=()=>{if(b.dataset.armed){firePeace(+b.dataset.peace);return}b.dataset.armed=1;b.innerHTML='ERASE THEM? <small>there is no way back</small>';b.classList.add('arm');setTimeout(()=>{if(b.isConnected)render()},3500)});\n  p.querySelectorAll('[data-wx]').forEach(")
rep("'fac_pframe','fac_wardenclyffe','fac_fbi','fac_haarp'];","'fac_pframe','fac_wardenclyffe','fac_fbi','fac_haarp','fac_peace'];")
rep("const V2_ART=new Set(['fac_haarp',","const V2_ART=new Set(['fac_peace','fac_haarp',")
rep("'front','pframe','fbi'].forEach(t=>{const im=new Image();","'front','pframe','fbi','peace'].forEach(t=>{const im=new Image();")
# bots: follow the whole chain (but HAARP stays a player tool) and build what it needs
rep("for(const g of GP){if(g.id==='fbi')continue;","for(const g of GP){if(g.id==='haarp')continue;")
rep("const ng=GP.find(g=>g.id!=='fbi'&&!S.inv[g.id]&&gpReqOk(g));","const ng=GP.find(g=>g.id!=='haarp'&&!S.inv[g.id]&&gpReqOk(g));")
rep("if(has('pframe')&&!count(S,'pframe')&&S.money>34000)need.unshift('pframe');",
    "if(has('pframe')&&!count(S,'pframe')&&S.money>34000)need.unshift('pframe');\n if(has('observatory')&&!count(S,'obs')&&S.money>13000)need.unshift('obs');\n if(has('fbi')&&!count(S,'fbi')&&S.money>20000)need.unshift('fbi');\n if(has('peace')&&!count(S,'peace')&&S.money>64000&&S.crystals>=12)need.unshift('peace');")
rep(" if(viewReady(S)&&!viewOn(S)&&S.crystals>=VIEW_K+4",
    " if(peaceReady(S)&&S.crystals>=PEACE_K&&S.psy>=PEACE_PSY&&rnd()<.12){const tg=allU().filter(u=>u!==S&&!(u!==MV.me&&u.over)).sort((a,b)=>Object.keys(b.anchors).length-Object.keys(a.anchors).length)[0];if(tg)firePeaceAt(S,tg)}\n if(viewReady(S)&&!viewOn(S)&&S.crystals>=VIEW_K+4")

JS=r"""
// ===== V4: P.E.A.C.E. - Particle Ether Accelerator for Cosmic Erasure =====
const PEACE_K=10,PEACE_PSY=40,PEACE_CD=8;
function peaceReady(u){u=u||S;return builtFac('peace',u)&&!(u.peaceCd>u.round)}
function firePeace(i){const r=MV.rivals[i];if(!r||r.over||!peaceReady(S)||S.crystals<PEACE_K||S.psy<PEACE_PSY||S.over)return;firePeaceAt(S,r);
 if(S.paper){showPaper()}save();render()}
function firePeaceAt(src,dst){src.crystals-=PEACE_K;src.psy-=PEACE_PSY;src.peaceCd=src.round+PEACE_CD;
 const freed=Object.keys(dst.anchors).map(id=>ANCHORS.find(a=>a.id===id).name);dst.anchors={};
 src.inst=clamp(src.inst+20,0,100);allU().forEach(u=>{if(u!==src&&u!==dst&&!(u!==MV.me&&u.over))u.inst=clamp(u.inst+8,0,100)});
 const me=MV.me;
 if(dst===me){me.over='lose-erased';me.erasedBy=src.bot.name;me.score=gameScore();return}
 dst.over='erased';
 MV.rivals.forEach((r,i)=>{if(!r.over)MV.rel[i]=clamp(MV.rel[i]-(src===me?40:0),-100,100)});
 const what=`${dst.bot.name} – ${dst.bot.lead}'s Manhattan – no longer exists.${freed.length?' Its anchors are free: '+freed.join(', ')+'.':''}`;
 if(src===me){MV.rep=`<b>P.E.A.C.E. fired.</b> ${what} Our instability +20 %, every other universe +8 %. The survivors will never trust us again.`;
  me.paper={title:`${dst.bot.name.toUpperCase()} ERASED`,photo:'art/paper_peace.webp',items:[['A sky that went out',`At ${['dawn','noon','dusk','midnight'][me.round%4]} the second skyline that New Yorkers had grown used to seeing in the clouds flared white and was gone. ${what}`],['"We have made peace"','A bureau spokesman, pale and shaking, read a single sentence to the press and left without taking questions. Instability across Manhattan rose sharply; churches stayed open all night.']]}}
 else MV.news.push([`${dst.bot.name} erased`,`${src.bot.name} fired a weapon called P.E.A.C.E. ${what} The shock wave raised our instability by 8 %.`])}
function peacePanel(){const alive=MV.rivals.map((r,i)=>[r,i]).filter(([r])=>!r.over),cd=S.peaceCd>S.round?S.peaceCd-S.round:0;
 return`<div class="hpanel ppanel"><b>Fire P.E.A.C.E.</b><small>◆${PEACE_K} and ${PEACE_PSY} psy per shot · erases the target universe and frees its anchors · our instability +20 %, all others +8 %, every survivor turns hostile · ${PEACE_CD} turns to recharge</small>`+
 (cd?`<small class="n">Recharging – ${cd} turn${cd>1?'s':''} left.</small>`:!alive.length?'<small>No other universe is left.</small>':`<div class="wxbtns">${alive.map(([r,i])=>`<button class="btn small" style="--rc:${rcol(r)}" data-peace="${i}" ${S.crystals>=PEACE_K&&S.psy>=PEACE_PSY&&!S.over?'':'disabled'}>Erase ${r.bot.name}<small>${r.bot.lead}</small></button>`).join('')}</div>`)+`</div>`}
"""
rep("// ===== V4: the Parallel Universe View =====",JS+"// ===== V4: the Parallel Universe View =====")
# being erased by a bot ends the game straight away
rep(" MV.rel=MV.rel.map(",
    " if(S.over==='lose-erased'){S.paper={title:endTitle(),photo:'art/paper_peace.webp',items:endItems()};S.log.unshift({round:S.round,items:S.paper.items});save();render();showPaper();return}\n MV.rel=MV.rel.map(")
rep("function endTitle(){return S.over==='win'?'The Universe Holds':S.over==='lose-rival'?'Another Manhattan Prevails':'The Singularity'}",
    "function endTitle(){return S.over==='win'?'The Universe Holds':S.over==='lose-rival'?'Another Manhattan Prevails':S.over==='lose-erased'?'Manhattan Erased':'The Singularity'}")
rep(" if(S.over==='lose-rival')return[['Another universe prevails',",
    " if(S.over==='lose-erased')return[['There was no warning',`${S.erasedBy} fired P.E.A.C.E. – the Particle Ether Accelerator for Cosmic Erasure – at our universe. In one white instant every street, every clock and every pigeon of our Manhattan ceased to have ever been.`],['Score',`${S.score} points.`]];\n if(S.over==='lose-rival')return[['Another universe prevails',")
# the bot's endTurn collapse message must not treat an erased rival twice (only lose-inst is announced there) - nothing to do

CSS="""
.ppanel{border-color:#8a2a2a;background:linear-gradient(#200c0c,#120606)}.ppanel>b{color:#ff8a7a}.ppanel .btn{border-left:3px solid var(--rc,#8a2a2a)!important}.ppanel .n{color:#e09a8a}
"""
idx=s.rindex("</style>",0,s.index("<body"));s=s[:idx]+CSS+s[idx:]
open(P,'w').write(s);print('peace patched',len(s))
