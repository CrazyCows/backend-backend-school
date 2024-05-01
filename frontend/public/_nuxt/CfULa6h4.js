var Y=Object.defineProperty;var K=(l,o,a)=>o in l?Y(l,o,{enumerable:!0,configurable:!0,writable:!0,value:a}):l[o]=a;var f=(l,o,a)=>(K(l,typeof o!="symbol"?o+"":o,a),a);import{L as V,d as j,o as z,r as _,t as m,v as g,x as n,y as r,M as b,N as k,O as N,P as H,B as y,C as J,D as U,_ as W}from"./D1UBHpIw.js";class ${constructor(o,a,S,D,x,w,i,u){f(this,"date");f(this,"uid_shift");f(this,"start_time");f(this,"end_time");f(this,"wishedShiftMembers");f(this,"actualShiftMembers");f(this,"active");f(this,"description");this.date=o,this.uid_shift=a,this.start_time=S,this.end_time=D,this.wishedShiftMembers=x,this.actualShiftMembers=w,this.active=i,this.description=u}}const q={uid_user:"c277b223-cd1f-482f-91ee-9622472c1d79"},G=V("calendar",{state:()=>({Shifts:[],Calendar:[],user:q}),getters:{getShifts(){return this.Shifts},getCalendar(){return this.Calendar},getUser(){return this.user}},actions:{updateShifts(l){this.Shifts=l},async fetchShiftsForMonthAsync(l){const o=await fetch("https://example.com",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(l)});if(!o.ok)throw new Error(`HTTP error! status: ${o.status}`)}}}),C=l=>(J("data-v-f3708610"),l=l(),U(),l),Q={class:"calendar-container"},R={class:"days-grid"},X=["onMousedown","onMousemove","onMouseup"],Z={class:"day-content"},ee={class:"day-note-container"},te={class:"center-box"},se={class:"left-center-box"},ne={class:"day-note-content"},ae={class:"shift-date"},le={class:"shift-time"},oe=C(()=>n("br",null,null,-1)),ie={class:"shift-description"},ue={class:"shift-status"},re={class:"shift-members"},ce=C(()=>n("br",null,null,-1)),de=C(()=>n("div",{class:"right-center-box"},[n("button",{class:"btn"},"Delete"),n("button",{class:"btn"},"Create")],-1)),ve=j({__name:"calendar",setup(l){z(async()=>{await o()});const o=async()=>{const s=new Date(u.value,i.value);console.log("fetch function is called");const e=await x.retrieveShiftsForMonthAsync(s);console.log(e.length),console.log("does it work yet??"),a.push(...e)};let a=[],S=new $(new Date,"uid_shift_example",new Date,new Date,[],[],!0,"example description");a.push(S),a.push(S);const D=["Søn","Man","Tirs","Ons","Tors","Fre","Lør"],x=G(),w=new Date,i=_(w.getMonth()),u=_(w.getFullYear()),c=_([]),d=_([]);let M=!1,v=_(null),h=_(null),O=!1;const I=_({}),B=s=>{v.value=null,h.value=null,c.value.length=0,console.log("hello"),M=!0,!a.map(e=>e.date.getDate()).includes(s)&&(d.value.includes(s)?(O=!0,console.log("Asked for removal"),c.value.push(s),v.value=s):(console.log("Asked for add"),c.value.push(s),v.value=s))},E=s=>{if(M&&!c.value.includes(s)){if(v.value!=null&&s>v.value){h.value=s;for(let e=v.value;e<=s;e++)c.value.includes(e)||c.value.push(e)}}else if(M&&v.value!=null&&h.value!=null&&h.value>s)for(let e=s;e<=h.value;e++){const t=c.value.indexOf(e);t>-1&&c.value.splice(t,1)}},P=s=>{if(M=!1,h.value=s,v.value!=null&&h.value!=null){if(O){const e=d.value.indexOf(v.value),t=d.value.indexOf(h.value);e!==-1&&t!==-1&&(d.value.splice(e,t-e+1),d.value),O=!1}else for(let e=v.value;e<=h.value;e++)if(!d.value.includes(e)&&!a.map(t=>t.date.getDate()).includes(e)){d.value.push(e);let t=new $(new Date(u.value,i.value,e),"uid_shift_example",new Date(u.value,i.value,e),new Date(u.value,i.value,e),[],[],!1,"example description");a.push(t)}c.value.length=0}},T=(s,e)=>new Date(e,s+1,0).getDate(),F=_(T(i.value,u.value)),A=s=>{let e=i.value+s;for(;e>11;)e-=12,u.value++;for(;e<0;)e+=12,u.value--;I.value[i.value]=d.value,i.value=e,F.value=T(i.value,u.value),d.value=I.value[i.value]||[],o()},L=s=>new Date(u.value,s).toLocaleString("default",{month:"long"});return(s,e)=>(m(),g(b,null,[n("div",Q,[n("header",null,[n("button",{onClick:e[0]||(e[0]=t=>A(-1))},"Tilbage"),n("h2",null,r(L(i.value.valueOf()))+" / "+r(u.value.valueOf()),1),n("button",{onClick:e[1]||(e[1]=t=>A(1))},"Frem")]),n("div",R,[(m(!0),g(b,null,k(D.length,t=>(m(),g("div",{key:t,class:"day-name"},r(D[new Date(u.value.valueOf(),i.value.valueOf(),t).getDay()]),1))),128)),(m(!0),g(b,null,k(F.value,t=>(m(),g("div",{key:t,class:H(["day",{inSelection:c.value.includes(t),selected:d.value.includes(t),createdShifts:N(a).filter(p=>p.active&&p.date.getMonth()==i.value.valueOf()).map(p=>p.date.getDate()).includes(t)}]),onMousedown:p=>B(t),onMousemove:p=>E(t),onMouseup:p=>P(t)},[n("div",Z,r(t),1)],42,X))),128))])]),n("div",ee,[(m(!0),g(b,null,k(N(a),t=>(m(),g("div",{key:t.uid_shift,class:"day-note"},[n("div",te,[n("div",se,[n("div",ne,[n("span",ae,r(t.start_time.getDate().valueOf()+" - "+L(t.start_time.getMonth().valueOf())),1),n("span",le,[y("Start: "+r(new Date(t.start_time).toLocaleString("da-DK",{day:"numeric",month:"long",year:"numeric",hour:"2-digit",minute:"2-digit"}))+" ",1),oe,y("Slut: "+r(new Date(t.end_time).toLocaleString("da-DK",{day:"numeric",month:"long",year:"numeric",hour:"2-digit",minute:"2-digit"})),1)]),n("span",ie,"Description: "+r(t.description),1),n("span",ue,"Active: "+r(t.active?"Yes":"No"),1),n("span",re,[y("Wished Members: "+r(t.wishedShiftMembers.length)+" ",1),ce,y("Actual Members: "+r(t.actualShiftMembers.length),1)])])]),de])]))),128))])],64))}}),_e=W(ve,[["__scopeId","data-v-f3708610"]]);export{_e as default};