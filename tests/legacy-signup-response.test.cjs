'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const test=require('node:test');
const html=fs.readFileSync(path.join(__dirname,'../sms/index.html'),'utf8');
const script=html.match(/<script>\s*(function handleSubmit[\s\S]*?)<\/script>/)[1];

for(const failure of ['http400','http503','bad-json','unsuccessful','network']) {
  test(`legacy signup does not claim success on ${failure}`,async()=>{
    const elements=Object.fromEntries(['submit-btn','consent','first_name','last_name','email','phone','form-section','success-section','submit-error'].map(id=>[id,{value:'synthetic',style:{},hidden:true,checked:true}]));
    let calls=0;
    const context=vm.createContext({document:{getElementById:id=>elements[id]},fetch:async()=>{
      calls++;
      if(failure==='network')throw new Error('synthetic offline failure');
      return {ok:!failure.startsWith('http'),json:async()=>{
        if(failure==='bad-json')throw new Error('synthetic parse failure');
        return {success:false};
      }};
    }});
    vm.runInContext(script,context);
    context.handleSubmit({preventDefault(){}});
    await new Promise(resolve=>setImmediate(resolve));
    assert.equal(calls,1);
    assert.notEqual(elements['success-section'].style.display,'block');
    assert.notEqual(elements['form-section'].style.display,'none');
    assert.equal(elements['submit-error'].hidden,false);
    assert.equal(elements['submit-btn'].disabled,false);
  });
}
