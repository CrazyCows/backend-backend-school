import{d as _,a3 as g,bl as x,H as y,r as l,t as h,b4 as C,A as s,z as a,x as u,y as S,b6 as U,b5 as k}from"./DWLzgMwE.js";import{j as A,w as B,x as R,y as F,e as f,i as T,h as L}from"./LZ6aDNKp.js";const M=u("span",{class:"text-h3"},"Login",-1),N={class:"d-inline-block",style:{color:"red"}},P=u("p",null,[u("a",{href:"#"},"Forgot password?")],-1),D=_({__name:"login",setup(j){const c=g(),v=x();y(()=>c.getUser!=null,()=>v.push("/"),{deep:!0});const r=l(""),n=l(""),d=l(!1),m=l(!1),i=l(""),p=o=>o?!0:"Password is required",V=[p],b=[p];async function w(o){if(i.value="",!(await o).valid)return;d.value=!0,await c.authenticateAsync(r.value,n.value)||(i.value="Username or password is incorrect"),d.value=!1}return(o,e)=>(h(),C(A,{class:"m-auto w-75","max-width":"500",elevation:"10",border:"sm",loading:d.value},{default:s(()=>[a(B,{class:"text-center mt-2"},{default:s(()=>[M]),_:1}),a(R,null,{default:s(()=>[u("p",N,S(i.value),1)]),_:1}),a(L,{modelValue:m.value,"onUpdate:modelValue":e[2]||(e[2]=t=>m.value=t),"validate-on":"input",onSubmit:[e[3]||(e[3]=k(()=>{},["prevent"])),w],"fast-fail":!0},{default:s(()=>[a(F,null,{default:s(()=>[a(f,{class:"mb-2",modelValue:r.value,"onUpdate:modelValue":e[0]||(e[0]=t=>r.value=t),rules:V,label:"Username",variant:"outlined"},null,8,["modelValue"]),a(f,{class:"mb-2",modelValue:n.value,"onUpdate:modelValue":e[1]||(e[1]=t=>n.value=t),rules:b,label:"Password",variant:"outlined",type:"password"},null,8,["modelValue"]),P]),_:1}),a(T,null,{default:s(()=>[a(U,{class:"mb-2",text:"Login",type:"submit",variant:"flat",color:"success",block:""})]),_:1})]),_:1},8,["modelValue"])]),_:1},8,["loading"]))}});export{D as default};