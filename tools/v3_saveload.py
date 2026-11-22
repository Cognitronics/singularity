"""Adds SAVE and LOAD to site/play3 (V3; V4 inherits it when built): three save slots in the browser plus
download / upload of a save file. Works on the version's autosave key (GAME_KEY), so V4 only has to swap
that one constant."""
import sys
P=sys.argv[1] if len(sys.argv)>1 else 'site/play3/index.html'
s=open(P).read()
def rep(a,b,n=1):
  global s
  assert s.count(a)==n,(s.count(a),a[:90]);s=s.replace(a,b)
assert 'id="savegame"' not in s

rep('<button id="newgame">NEW GAME</button><button id="quitgame">QUIT GAME</button>',
    '<button id="newgame">NEW GAME</button><button id="savegame">SAVE</button><button id="loadgame">LOAD</button><button id="quitgame">QUIT GAME</button>')
rep('<div class="modal" id="quitdlg"',
    '<div class="modal sldlg" id="sldlg" role="dialog" aria-modal="true" aria-labelledby="sl_title"><div class="qbox slbox"><button class="mclose" id="sl_close" aria-label="Close">✕</button><h2 id="sl_title">SAVE &amp; LOAD</h2><div id="slbody"></div></div></div>\n<div class="modal" id="quitdlg"')

JS=r"""
// ===== save & load: 3 slots in the browser + save file download/upload =====
const GAME_KEY='singularity-v3-dev';
function slotKey(n){return GAME_KEY+'-slot'+n}
function slotGet(n){try{const j=localStorage.getItem(slotKey(n));return j?JSON.parse(j):null}catch(e){return null}}
function saveMeta(){return{name:agentName()||'Agent',mode:S.endless?'Endless':'Epochal',diff:(DIFFS[S.diff]||DIFFS.hard).n,turn:S.round+1,date:new Date().toLocaleString('en-GB',{day:'numeric',month:'short',hour:'2-digit',minute:'2-digit'})}}
function saveSlot(n){if(!S||S.over)return false;save();try{localStorage.setItem(slotKey(n),JSON.stringify({meta:saveMeta(),data:localStorage.getItem(GAME_KEY)}));return true}catch(e){return false}}
// loading writes the data into the autosave key and lets the normal load() validate it; on failure the old game comes back
function loadData(data){let prev=null;try{prev=localStorage.getItem(GAME_KEY)}catch(e){}
 try{localStorage.setItem(GAME_KEY,data);if(load()){S.paper=null;$('modesel').classList.remove('on');window.LABOPEN=false;tab='bezirk';S.sel=null;render();return true}}catch(e){}
 try{if(prev)localStorage.setItem(GAME_KEY,prev);load();render()}catch(e){}return false}
function downloadSave(){if(!S)return;save();let data='';try{data=localStorage.getItem(GAME_KEY)}catch(e){}
 const m=saveMeta(),blob=new Blob([JSON.stringify({game:'singularity',key:GAME_KEY,meta:m,data})],{type:'application/json'});
 const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=`singularity-${m.name.replace(/[^\w-]+/g,'_')}-turn${m.turn}.json`;document.body.appendChild(a);a.click();setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove()},500)}
function openSaveLoad(msg){const d=$('sldlg');const inGame=S&&!S.over&&!$('modesel').classList.contains('on');
 let h=msg?`<p class="slmsg">${msg}</p>`:'';
 h+=`<div class="slslots">`+[1,2,3].map(n=>{const o=slotGet(n),m=o&&o.meta;return`<div class="slslot"><b>Slot ${n}</b><span>${m?`${esc(m.name)} · ${m.mode} · ${m.diff} · turn ${m.turn}<small>${esc(m.date)}</small>`:'<small>empty</small>'}</span><button class="btn small" data-sls="${n}" ${inGame?'':'disabled'}>Save here</button><button class="btn small" data-sll="${n}" ${o?'':'disabled'}>Load</button></div>`}).join('')+`</div>`;
 h+=`<div class="slfile"><button class="btn small" id="sldown" ${inGame?'':'disabled'}>Download save file</button><label class="btn small slup">Load save file<input type="file" id="slup" accept=".json,application/json" hidden></label></div><p class="note">Slots live in this browser. A save file can be moved to another computer.</p>`;
 $('slbody').innerHTML=h;d.classList.add('on');
 d.querySelectorAll('[data-sls]').forEach(b=>b.onclick=()=>{const n=+b.dataset.sls;if(slotGet(n)&&!b.dataset.armed){b.dataset.armed=1;b.textContent='Overwrite?';b.classList.add('arm');return}openSaveLoad(saveSlot(n)?`Saved to slot ${n}.`:'Could not save (browser storage full or blocked).')});
 d.querySelectorAll('[data-sll]').forEach(b=>b.onclick=()=>{const o=slotGet(+b.dataset.sll);if(o&&loadData(o.data))d.classList.remove('on');else openSaveLoad('This slot could not be loaded.')});
 $('sldown').onclick=downloadSave;
 $('slup').onchange=e=>{const f=e.target.files[0];if(!f)return;f.text().then(t=>{let o=null;try{o=JSON.parse(t)}catch(_){}
  if(!o||o.game!=='singularity'||!o.data)return openSaveLoad('That is not a Singularity save file.');
  if(o.key!==GAME_KEY)return openSaveLoad('That save file belongs to another version of the game.');
  if(loadData(o.data))d.classList.remove('on');else openSaveLoad('The save file could not be loaded.')})}}
"""
rep("// ===== V3: mode selection after the intro",JS+"// ===== V3: mode selection after the intro")
rep("document.getElementById('newgame').onclick=()=>openModeSel(!S.over);",
    "document.getElementById('newgame').onclick=()=>openModeSel(!S.over);\ndocument.getElementById('savegame').onclick=()=>openSaveLoad();\ndocument.getElementById('loadgame').onclick=()=>openSaveLoad();\n{const d=document.getElementById('sldlg');document.getElementById('sl_close').onclick=()=>d.classList.remove('on');d.addEventListener('click',e=>{if(e.target===d)d.classList.remove('on')});document.addEventListener('keydown',e=>{if(e.key==='Escape'&&d.classList.contains('on'))d.classList.remove('on')})}")
# the start screen gets a LOAD GAME button
rep("<button class=\"btn mscont\" id=\"tohs\">HALL OF FAME<small>The best agents</small></button></div></div>`;",
    "<button class=\"btn mscont\" id=\"msload\">LOAD GAME<small>Slots or a save file</small></button><button class=\"btn mscont\" id=\"tohs\">HALL OF FAME<small>The best agents</small></button></div></div>`;")
rep(" $('chname').onclick=e=>"," $('msload').onclick=()=>openSaveLoad();\n $('chname').onclick=e=>")

CSS="""
/* save & load dialog (above the start screen) */
.sldlg{z-index:320}.slbox{max-width:520px}
.slslots{display:flex;flex-direction:column;gap:8px;margin:12px 0}
.slslot{display:grid;grid-template-columns:52px 1fr auto auto;gap:8px;align-items:center;text-align:left;padding:7px 8px;background:rgba(0,0,0,.35);border:1px solid #3a3122}
.slslot b{font:400 13px 'Federo',serif;color:#e2c480}.slslot span{font-size:12px;color:#d9d2c3}.slslot small{display:block;font-size:10.5px;color:#8d877b}
.slfile{display:flex;gap:8px;justify-content:center;flex-wrap:wrap}.slup{cursor:pointer}
.slmsg{color:#9ff0b0;margin:6px 0 0}
@media(max-width:520px){.slslot{grid-template-columns:1fr 1fr}.slslot b,.slslot span{grid-column:span 2}}
"""
idx=s.rindex("</style>",0,s.index("<body"));s=s[:idx]+CSS+s[idx:]
open(P,'w').write(s);print('save/load patched',len(s))
