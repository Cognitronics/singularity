"""V4 add-on (run after v4_wardenclyffe.py): the Federal Bureau of Investigation - second great project.
Only after the Wardenclyffe Tower and the Observatory. A headquarters in Manhattan (one per game, on any
building plot). Until it stands the bureau knows nothing about the other universes: the Rivals tab and the
rival overview are hidden, and there is no diplomacy or trade."""
import sys
P=sys.argv[1] if len(sys.argv)>1 else 'site/play4/index.html'
s=open(P).read()
def rep(a,b,n=1):
  global s
  assert s.count(a)==n,(s.count(a),a[:90]);s=s.replace(a,b)

rep(" pframe:{n:'Parallel Universe Pictureframe'",
    " fbi:{n:'Federal Bureau of Investigation',era:1,r:{psy:2,sym:2},t:'G',pre:'observatory',d:'Great project: a headquarters in Manhattan that gathers intelligence on the other universes. Unlocks the Rivals tab, pacts and trade',con:'Needs the Observatory invention first'},\n pframe:{n:'Parallel Universe Pictureframe'")
rep(" pframe:{name:'Pictureframe',",
    " fbi:{name:'Federal Bureau HQ',cost:16000,bt:5,k:2,up:500,mw:20,col:'#d8c070',d:'Great project · intelligence on the other universes: Rivals tab, pacts and trade · only one',req:'fbi',spr:'fac_fbi',great:true},\n pframe:{name:'Pictureframe',")
rep("'front','pframe'].forEach(t=>{const im=new Image();","'front','pframe','fbi'].forEach(t=>{const im=new Image();")
rep("'fac_pframe','fac_wardenclyffe'];","'fac_pframe','fac_wardenclyffe','fac_fbi'];")
rep("const V2_ART=new Set(['fac_wardenclyffe',","const V2_ART=new Set(['fac_fbi','fac_wardenclyffe',")
rep("known:['coil','damper','portalgeo','observatory','wardenclyffe']","known:['coil','damper','portalgeo','observatory','wardenclyffe','fbi']")

JS=r"""
// ===== V4: the Federal Bureau of Investigation (great project: intelligence on the other universes) =====
function fbiDone(u){u=u||S;return !!(u&&u.slots&&Object.values(u.slots).some(a=>a.some(f=>f&&f.t==='fbi'&&!(f.bt>0))))}
"""
rep("// ===== V4: the Parallel Universe View =====",JS+"// ===== V4: the Parallel Universe View =====")
# hide the Rivals tab and the overview until the HQ stands
rep(" $('rivstrip').innerHTML=rivalStrip();",
    " if(tab==='rivals'&&!fbiDone())tab='bezirk';\n {const rb=document.querySelector('.tabs [data-t=rivals]');if(rb)rb.hidden=!fbiDone()}\n $('rivstrip').innerHTML=fbiDone()?rivalStrip():'';")
rep("function proposePact(i){if(!wcDone(S))return;","function proposePact(i){if(!wcDone(S)||!fbiDone(S))return;")
rep("function trade4(i,kind){if(!wcDone(S))return;","function trade4(i,kind){if(!wcDone(S)||!fbiDone(S))return;")
rep("const lead=MV.rivals.filter((r,i)=>!r.over&&knows(i)).sort(","const lead=MV.rivals.filter((r,i)=>fbiDone()&&!r.over&&knows(i)).sort(")
rep("– see the Rivals tab. To reach them, Tesla\\'s Wardenclyffe Tower must first stand on the Brooklyn shore.",
    "– but we know nothing about them yet. To reach them we need Tesla\\'s Wardenclyffe Tower on the Brooklyn shore; to learn what they are doing, a Federal Bureau of Investigation headquarters in Manhattan.")
# district overview: status of the second great project
rep("'<p class=\"note\">⚡ Wardenclyffe Tower: <b>contact established</b> ($400 upkeep).</p>'}</div>",
    "'<p class=\"note\">⚡ Wardenclyffe Tower: <b>contact established</b> ($400 upkeep).</p>'}${fbiDone()?'<p class=\"note\">🦅 Federal Bureau HQ: <b>intelligence on the other universes</b> – see the Rivals tab.</p>':count(S,'fbi')?'<p class=\"note\">🦅 Federal Bureau HQ under construction.</p>':inv('fbi')?'<p class=\"note\">🦅 The <b>Federal Bureau HQ</b> can now be built on any free plot in Manhattan (select a district).</p>':wcDone()?'<p class=\"note\">Next great project: the <b>Federal Bureau of Investigation</b> – it needs the Observatory invention first.</p>':''}</div>")
open(P,'w').write(s);print('fbi patched',len(s))
