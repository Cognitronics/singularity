"""V4 add-on (run after v4_view.py): the Wardenclyffe Tower - the first great project.
Tesla's tower is built on a fixed site on the Brooklyn shore, right of the Brooklyn Bridge. It makes
contact with the parallel universes: only with a finished tower can a bureau send missions, sign pacts
or trade. The Observatory (and so the Pictureframe) can only be invented once the tower stands."""
import sys
P=sys.argv[1] if len(sys.argv)>1 else 'site/play4/index.html'
s=open(P).read()
def rep(a,b,n=1):
  global s
  assert s.count(a)==n,(s.count(a),a[:90]);s=s.replace(a,b)

# ---- invention + chain: Wardenclyffe -> Observatory -> Pictureframe ----
rep(" observatory:{n:'Observatory',era:1,r:{lig:2,eth:1},t:'A',d:'Unlocks the Observatory'},",
    " wardenclyffe:{n:'Wardenclyffe Tower',era:1,r:{ele:2,wav:2},t:'G',d:'Great project: Tesla\\'s giant wireless tower on the Brooklyn shore. It makes contact with the parallel universes – missions, pacts and trade become possible'},\n observatory:{n:'Observatory',era:1,r:{lig:2,eth:1},t:'A',pre:'wardenclyffe',d:'Unlocks the Observatory',con:'Needs a finished Wardenclyffe Tower'},")
rep("const hit=same.find(([id,v])=>v.era<=e&&(!v.pre||S.inv[v.pre])","const hit=same.find(([id,v])=>v.era<=e&&preOk(v)")
rep("  else if(v.pre&&!S.inv[v.pre]){res='near';txt=`The frame of something enormous takes shape – but we must first master the <b>${INV[v.pre].n}</b>.`}",
    "  else if(!preOk(v)){res='near';txt=v.pre==='wardenclyffe'?'The instruments pick up faint signals from beyond – but without contact we cannot focus them. First finish the <b>Wardenclyffe Tower</b>.':`The frame of something enormous takes shape – but we must first master the <b>${INV[v.pre].n}</b>.`}")
rep("known:['coil','damper','portalgeo','observatory']","known:['coil','damper','portalgeo','observatory','wardenclyffe']")

JS=r"""
// ===== V4: the Wardenclyffe Tower (great project on a fixed site on the Brooklyn shore) =====
const WC_T=[15,4],WC={cost:20000,k:3,bt:8,up:400};
function wcDone(u){u=u||S;return !!(u&&u.wc&&!(u.wc.bt>0))}
function preOk(v){return !v.pre||(v.pre==='wardenclyffe'?wcDone():!!S.inv[v.pre])}
function buildWC(){if(!inv('wardenclyffe')||S.wc||S.money<WC.cost||S.crystals<WC.k||S.over)return;S.money-=WC.cost;S.crystals-=WC.k;S.wc={bt:WC.bt};S.c.unruhe+=2;save();render()}
"""
rep("// ===== V4: the Parallel Universe View =====",JS+"// ===== V4: the Parallel Universe View =====")
# upkeep and construction
rep(" let loanPay=0;"," if(wcDone())upkeep+=WC.up;\n let loanPay=0;")
rep(" for(const k in S.slots)S.slots[k].forEach(f=>{if(f&&f.mods)",
    " if(S.wc&&S.wc.bt>0){S.wc.bt--;if(!S.wc.bt)msgs.unshift(['Wardenclyffe Tower completed',BOT?'':'Tesla\\'s tower crackles to life over the Brooklyn shore. For the first time we can reach the other universes: missions, pacts and trade are now possible – and the Observatory can be invented.'])}\n for(const k in S.slots)S.slots[k].forEach(f=>{if(f&&f.mods)")
# contact gates: missions, pacts, trade
rep("function playerMission(sci,i,type){","function playerMission(sci,i,type){if(!wcDone(S))return;")
rep("function proposePact(i){","function proposePact(i){if(!wcDone(S))return;")
rep("function trade4(i,kind){","function trade4(i,kind){if(!wcDone(S))return;")
rep("if(S.sci.length&&S.psy>=MISSION_PSY&&rnd()<PS.mis)","if(wcDone(S)&&S.sci.length&&S.psy>=MISSION_PSY&&rnd()<PS.mis)")
# bots know the recipe and build the tower
rep("S.bot=d;S.rid=i;","S.bot=d;S.rid=i;S.known.push('wardenclyffe');")
rep("if(has('pframe')&&!count(S,'pframe')&&S.money>34000)need.unshift('pframe');",
    "if(has('pframe')&&!count(S,'pframe')&&S.money>34000)need.unshift('pframe');\n if(inv('wardenclyffe')&&!S.wc){if(S.money>=WC.cost&&S.crystals>=WC.k)buildWC();else S.saveWC=1}else S.saveWC=0;")
rep(" let builds=S.money>30000?2:1;"," let builds=S.saveWC&&S.money<WC.cost?0:S.money>30000?2:1; // bots save up for the tower")
# UI: agents + rivals without contact
rep("if(alive.length&&S.sci.length)h+=",
    "if(!wcDone(S))h+=`<p class=\"mrep\">No contact with the other universes yet. Missions need the <b>Wardenclyffe Tower</b>${S.wc?` – it is under construction (${S.wc.bt} turn${S.wc.bt>1?'s':''} left).`:inv('wardenclyffe')?' – build it in the district overview.':' – invent it in the laboratory first.'}</p>`;\n  else if(alive.length&&S.sci.length)h+=")
rep("const tg=MV&&MV.rivals[window.MTARGET];","const tg=MV&&wcDone(S)&&MV.rivals[window.MTARGET];") if "const tg=MV&&MV.rivals[window.MTARGET];" in s else None
rep("`<div class=\"btns\">${pact?'':","`<div class=\"btns\">${!wcDone(S)?'<p class=\"note\">No contact yet – the Wardenclyffe Tower opens diplomacy and trade.</p>':pact?'':")
rep("race us for the same ten anchors – see the Rivals tab.","race us for the same ten anchors – see the Rivals tab. To reach them, Tesla\\'s Wardenclyffe Tower must first stand on the Brooklyn shore.")
# district overview: the great projects
rep("<div class=\"bank\"><h3>Bank of Manhattan</h3>",
    "<div class=\"bank\"><h3>Great projects</h3>${!inv('wardenclyffe')?`<p class=\"note\">${S.known.includes('wardenclyffe')?'The recipe of the <b>Wardenclyffe Tower</b> is known – invent it at the bench.':'Great projects are invented in the laboratory. The first one makes contact with the other universes.'}</p>`:!S.wc?`<button class=\"btn\" id=\"buildwc\" ${S.money>=WC.cost&&S.crystals>=WC.k&&!S.over?'':'disabled'}>Build the Wardenclyffe Tower<small>on the Brooklyn shore · $${fmt(WC.cost)} · ◆${WC.k} · ${WC.bt} turns · contact with the parallel universes</small></button>`:S.wc.bt>0?`<p class=\"note\">Wardenclyffe Tower under construction – ${S.wc.bt} turn${S.wc.bt>1?'s':''} left.</p>`:'<p class=\"note\">⚡ Wardenclyffe Tower: <b>contact established</b> ($400 upkeep).</p>'}</div><div class=\"bank\"><h3>Bank of Manhattan</h3>")
rep("  if($('loan'))$('loan').onclick=takeLoan;","  if($('loan'))$('loan').onclick=takeLoan;if($('buildwc'))$('buildwc').onclick=buildWC;")
rep(" if(!S.resTarget)t.push('Our researchers are idle.",
    " if(inv('wardenclyffe')&&!S.wc&&S.money>=WC.cost)t.unshift('The <b>Wardenclyffe Tower</b> is ready to be built on the Brooklyn shore (district overview). With it we can finally reach the other universes.');\n if(!S.resTarget)t.push('Our researchers are idle.")
# map: the tower on the Brooklyn shore (the shore building on that tile gives way)
rep("    if(SB.length){if(r()<.6)","    if(S&&S.wc&&t.x===WC_T[0]&&t.y===WC_T[1])continue;\n    if(SB.length){if(r()<.6)")
rep("  const order=[...TILES].sort",
    "  if(!MASK&&S&&S.wc&&SPR.fac_wardenclyffe){const p=P(WC_T[0]+.5,WC_T[1]+.5);cx.save();if(S.wc.bt>0)cx.globalAlpha=.35+.55*(1-S.wc.bt/WC.bt);spr(cx,'fac_wardenclyffe',p[0],p[1]+6,34,false,null);cx.restore();if(!(S.wc.bt>0))LIGHTS.push({x:p[0],y:p[1]-52,c:'#9ad8ff',r:18})}\n  const order=[...TILES].sort")
rep("'fac_front','fac_pframe'];","'fac_front','fac_pframe','fac_wardenclyffe'];")
rep("const V2_ART=new Set(['fac_pframe',","const V2_ART=new Set(['fac_wardenclyffe','fac_pframe',")
open(P,'w').write(s);print('wardenclyffe patched',len(s))
