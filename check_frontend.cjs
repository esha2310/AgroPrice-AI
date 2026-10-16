// Syntax and DOM-stub interaction checks, NOT a real-browser visual test.
const fs=require('fs'),vm=require('vm'),assert=require('assert');
const html=fs.readFileSync(__dirname+'/index.html','utf8');
const snap=html.match(/<script id="snapshot" type="application\/json">([\s\S]*?)<\/script>/)[1];
const code=html.match(/<script>\s*('use strict';[\s\S]*?)<\/script>/)[1];
const nodes=new Map();function node(id){if(!nodes.has(id))nodes.set(id,{textContent:id==='snapshot'?snap:'',innerHTML:'',value:'',dataset:{},className:'',classList:{add(){},remove(){},toggle(){return false}},setAttribute(){},addEventListener(){},scrollIntoView(){},showModal(){},close(){},click(){}});return nodes.get(id)}
let stored={};const ctx={console,document:{body:{dataset:{page:'welcome'}},documentElement:{dataset:{backend:'0'}},getElementById:node,querySelectorAll:()=>[],createElement:()=>node('anchor')},localStorage:{getItem:k=>stored[k]||null,setItem:(k,v)=>stored[k]=v},window:{location:{pathname:'/index.html',hash:'',href:''}},setTimeout:()=>1,clearTimeout(){},Blob,URL,URLSearchParams};vm.createContext(ctx);vm.runInContext(code,ctx);
vm.runInContext(`for (const s of ALL){state.id=s.id;state.commodity=s.commodity;state.model=s.selected_model;render();if(!document.getElementById('chart').innerHTML.includes('<path'))throw Error('Empty chart '+s.id);for (const m of ['Persistence','Seasonal naive','Random Forest','XGBoost']){state.model=m;render();}}`,ctx);
vm.runInContext(`state.commodity='flour';state.id='';selectors();state.compare=ALL.find(s=>s.commodity==='flour'&&s.id!==state.id).id;render();`,ctx);
vm.runInContext(`saveWatch(state.id,true)`,ctx);assert(stored['agroprice-watchlist']);
vm.runInContext(`document.getElementById('downloadBtn').onclick();openAuth();`,ctx);
vm.runInContext(`showWelcome();if(document.body.dataset.page!=='welcome')throw Error('Welcome page');document.getElementById('startBtn').onclick();if(window.location.href!=='login.html')throw Error('Login page route');showWorkspace('explore');if(!window.location.href.startsWith('dashboard.html?commodity=')||!window.location.href.endsWith('#explore'))throw Error('Dashboard route');window.location.pathname='/dashboard.html';showWorkspace('watchlist');if(document.body.dataset.page!=='workspace')throw Error('Workspace view');document.getElementById('backWelcome').onclick();if(window.location.href!=='index.html#home')throw Error('Welcome route');`,ctx);
for(const name of ['login','signup']){
 const page=fs.readFileSync(__dirname+'/'+name+'.html','utf8');
 const js=page.match(/<script>\s*('use strict';[\s\S]*?)<\/script>/)[1];new vm.Script(js);
 const inputs=['username','password','confirm','email','fullName','accept','remember','submitBtn'].map(node);
 const ac={document:{documentElement:{dataset:{backend:'0'}},getElementById:node,querySelectorAll:q=>q.startsWith('#accountForm')?inputs:[]},window:{location:{assign(){},replace(){}}}};vm.createContext(ac);vm.runInContext(js,ac);
 assert.equal(node('guestLink').href,'dashboard.html');assert.equal(node('switchLink').href,name==='login'?'signup.html':'login.html');assert(inputs.every(n=>n.disabled));assert(!/__PADDY__|__LEAF__|__TITLE__|__FIELDS__/.test(page));
}

assert(!/__DATA__|__PADDY__|__LANDSCAPE__|__LEAF__|__RICE_ART__|__LENTILS_ART__|__FLOUR_ART__|__OIL_ART__/.test(html));assert(!/https?:\/\/[^'" ]+\.(?:js|css)/.test(html));
console.log('PASS: JS parse, render all series × four models, missing forecast handling, comparison, watchlist storage, CSV, auth-preview branch, separate-page navigation, login/signup syntax and disabled public-preview forms. Browser layout remains unchecked.');
