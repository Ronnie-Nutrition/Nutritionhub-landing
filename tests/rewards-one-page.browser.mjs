import { spawn } from 'node:child_process';
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const dir = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(dir, '..');
const assert = (condition, label) => { if (!condition) throw new Error(label); };
const scenarios = [];
const record = (name, evidence) => { scenarios.push({name, ...evidence}); };
const profile = await fs.mkdtemp('/tmp/nh-rewards-render-');
const chrome = spawn('/Users/apple/Library/Caches/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-mac-arm64/chrome-headless-shell', ['--headless','--no-first-run','--disable-background-networking','--disable-component-update','--disable-sync','--host-resolver-rules=MAP * ~NOTFOUND','--remote-debugging-port=0',`--user-data-dir=${profile}`,'about:blank'],{stdio:['ignore','ignore','pipe']});
let socket;
try {
  const wsurl = await new Promise((resolve,reject)=>{
    let buf=''; const timer=setTimeout(()=>reject(new Error('Chromium startup timeout')),15000);
    chrome.stderr.on('data',d=>{buf+=d; const m=buf.match(/DevTools listening on (ws:\/\/[^\s]+)/); if(m){clearTimeout(timer);resolve(m[1]);}});
    chrome.on('error',reject);chrome.on('exit',code=>reject(new Error('Chromium exited '+code+': '+buf.slice(-1200))));
  });
  socket = new WebSocket(wsurl);
  await new Promise((resolve,reject)=>{socket.onopen=resolve;socket.onerror=reject;});
  let id=0; const pending=new Map(); let sessionId; const blocked=[];
  const send=(method,params={},session=sessionId)=>new Promise((resolve,reject)=>{
    const req={id:++id,method,params};if(session)req.sessionId=session;
    pending.set(req.id,{resolve,reject});socket.send(JSON.stringify(req));
  });
  socket.onmessage=ev=>{
    const msg=JSON.parse(ev.data);
    if(msg.id){const p=pending.get(msg.id);pending.delete(msg.id);msg.error?p.reject(new Error(JSON.stringify(msg.error))):p.resolve(msg.result);}
    else if(msg.method==='Fetch.requestPaused'){
      const url=msg.params.request.url;
      const file = url==='https://nutritionhub101.com/rewards/' ? 'rewards/index.html' : url==='https://nutritionhub101.com/analytics-consent.js' ? 'analytics-consent.js' : url==='https://nutritionhub101.com/assets/portfolio-measurement.js' ? 'assets/portfolio-measurement.js' : null;
      if(file) fs.readFile(path.join(root,file)).then(body=>send('Fetch.fulfillRequest',{requestId:msg.params.requestId,responseCode:200,responseHeaders:[{name:'Content-Type',value:file.endsWith('.js')?'application/javascript':'text/html'}],body:body.toString('base64')},msg.sessionId)).catch(()=>{});
      else { blocked.push({method:msg.params.request.method,host:new URL(url).hostname}); send('Fetch.failRequest',{requestId:msg.params.requestId,errorReason:'BlockedByClient'},msg.sessionId).catch(()=>{}); }
    }
  };
  const {targetInfos}=await send('Target.getTargets',{},null);
  ({sessionId}=await send('Target.attachToTarget',{targetId:targetInfos.find(t=>t.type==='page').targetId,flatten:true},null));
  await send('Page.enable');await send('Runtime.enable');
  await send('Fetch.enable',{patterns:[{urlPattern:'*',requestStage:'Request'}]});
  await send('Network.enable'); await send('Network.setCookie',{name:'nh_measurement_consent',value:'denied',url:'https://nutritionhub101.com/'});
  const evaluate=async expression=>{
    const result=await send('Runtime.evaluate',{expression: expression.includes('await ') ? '(async()=>{'+expression+'})()' : expression,returnByValue:true,awaitPromise:true});
    if(result.exceptionDetails)throw new Error(JSON.stringify(result.exceptionDetails));
    return result.result.value;
  };
  await send('Page.navigate',{url:'https://nutritionhub101.com/rewards/'});
  for(let i=0;i<100;i++){ if(await evaluate("typeof checkIn==='function' && typeof NHAnalytics==='object'")) break; await new Promise(r=>setTimeout(r,20)); }
  await send('Emulation.setDeviceMetricsOverride',{width:390,height:844,deviceScaleFactor:1,mobile:true});

  const initial = await evaluate(`({unchecked:!$('offerConsent').checked,offerVisible:getComputedStyle($('offerBox')).display!=='none',submitDisabled:$('offerSubmit').disabled,noEmail:!document.querySelector('input[autocomplete=email]'),savedChoice:document.cookie.includes('nh_measurement_consent=denied'),metaPageViewQueued:(window.fbq?.queue||[]).some(x=>x[0]==='track'&&x[1]==='PageView')})`);
  assert(initial.unchecked && initial.offerVisible && initial.submitDisabled && initial.noEmail && initial.savedChoice && !initial.metaPageViewQueued, 'initial optional consent/privacy');
  record('optional consent upfront, no email/name prerequisites, saved decline', initial);
  const privacy = await evaluate(`$('privacyChoices').click(); ({controlVisible:$('privacyChoices').getBoundingClientRect().height>0,bannerReopened:!!document.getElementById('nh-consent-banner'),policyVisible:document.querySelector('.privacy-links a').getBoundingClientRect().height>0})`);
  assert(privacy.controlVisible && privacy.bannerReopened && privacy.policyVisible, 'privacy reopen');
  record('persistent privacy controls', privacy);
  await evaluate(`document.querySelector('#nh-consent-banner [data-choice=denied]').click();true`);
  await evaluate(`
    window.auditRequests=[]; window.auditGeoCalls=0; window.auditConfig={};
    window.auditReset=()=>{resetVisit();auditRequests=[];auditGeoCalls=0;auditConfig={};};
    getPosition=async()=>{auditGeoCalls++;return {lat:29.5,lng:-95.3,accuracy:10};};
    window.fetch=async(url,options={})=>{
      const pathname=new URL(url).pathname;
      const body=options.body?JSON.parse(options.body):null;
      auditRequests.push({path:pathname,body,credentials:options.credentials,headers:options.headers});
      if(auditConfig.throwPath===pathname)throw new Error('Synthetic offline connection failure');
      if(auditConfig.badJson===pathname)return {ok:true,status:200,json:async()=>{throw new Error('Synthetic invalid JSON');}};
      let data={};let status=200;
      if(pathname==='/api/verification/status') data={verificationRequired:true,trusted:!!auditConfig.trusted};
      else if(pathname==='/api/verification/start') data={sent:true};
      else if(pathname==='/api/verification/check') data={verified:!auditConfig.badCode};
      else if(pathname==='/api/points-checkin')data=auditConfig.newRewards&&!auditConfig.created?{found:false}:{found:true,contactId:'synthetic-contact',sessionToken:'synthetic-session',firstName:'Test',needsProfile:true,points:auditConfig.points??3,awarded:!!auditConfig.awarded,refused:auditConfig.refused};
      else if(pathname==='/api/sms-optin'){
        data={success:true,contactId:'synthetic-contact',sessionToken:'synthetic-session',isNew:!!auditConfig.newRewards};auditConfig.created=true;
      } else if(pathname==='/api/consent/winback'){
        status=201;data={ok:true,receipt:{status:'captured',handoff_status:auditConfig.pending?'pending_reconciliation':'queued'}};
      }
      if(auditConfig.failPath===pathname){status=503;data={error:'Synthetic rejected request'};}
      return {ok:status>=200&&status<300,status,json:async()=>data};
    };
    true
  `);
  const inspect = () => evaluate(`({requests:auditRequests,geoCalls:auditGeoCalls,verifyVisible:!$('s-verify').classList.contains('hide'),joinVisible:!$('s-join').classList.contains('hide'),balanceVisible:!$('s-balance').classList.contains('hide'),offersVisible:!$('s-offers').classList.contains('hide'),offerResult:$('offerResult').textContent,staffVisible:!$('staffVerifyBox').classList.contains('hide'),staffPin:state.staffPin,staffInput:$('staffVerifyPin').value,offerCaptured:state.offerCaptured,checkboxDisabled:$('offerConsent').disabled,submitDisabled:$('offerSubmit').disabled,checked:$('offerConsent').checked,points:$('ptsNum').textContent,award:$('awardToast').textContent,joinError:$('joinErr').textContent,phoneError:$('phoneErr').textContent})`);
  const counts = (report, pathname) => report.requests.filter(x=>x.path===pathname).length;
  const chooseOffers = `$('phone').value='2025550101';$('offerConsent').checked=true;$('offerConsent').dispatchEvent(new Event('change'));await startFlow('offers');`;
  await evaluate(`auditReset();${chooseOffers}true`);
  let report = await inspect();
  assert(report.verifyVisible && !report.staffVisible && report.geoCalls===0 && counts(report,'/api/verification/start')===1 && counts(report,'/api/consent/winback')===0, 'offers must require exact-phone proof without staff bypass');
  await evaluate(`$('verifyCode').value='123456';await verifyCodeAndCheckIn();true`);
  report = await inspect();
  const offerAccount = report.requests.find(x=>x.path==='/api/sms-optin');
  const consent = report.requests.find(x=>x.path==='/api/consent/winback');
  assert(report.offersVisible && report.offerCaptured && report.geoCalls===0 && counts(report,'/api/points-checkin')===0 && counts(report,'/api/verification/check')===1 && counts(report,'/api/verification/start')===1, 'new offers one OTP no checkin');
  assert(JSON.stringify(offerAccount.body)===JSON.stringify({phone:'2025550101',sms_consent:false,purpose:'offers'}) && offerAccount.credentials==='include', 'minimal offers payload');
  assert(consent.credentials==='include' && consent.headers['X-Rewards-Session']==='synthetic-session' && consent.body.affirmative_opt_in===true && !('pin' in consent.body), 'consent separate and proof bound');
  record('new offers: one code, no profile/geolocation/points, separate consent',report);
  await evaluate(`await startFlow('offers');true`);
  assert(counts(await inspect(),'/api/consent/winback')===1,'no repeated capture after success');
  await evaluate(`auditReset();auditConfig.trusted=true;${chooseOffers}true`);
  report=await inspect();
  assert(report.offerCaptured && report.geoCalls===0 && counts(report,'/api/verification/start')===0 && counts(report,'/api/consent/winback')===1,'trusted returning offers no OTP');
  record('trusted returning offers skip OTP',report);
  await evaluate(`auditReset();auditConfig.trusted=true;auditConfig.pending=true;${chooseOffers}true`);
  report=await inspect();
  assert(report.offerCaptured && report.offerResult.includes('ask a team member') && report.checkboxDisabled && report.submitDisabled && counts(report,'/api/consent/winback')===1,'pending handoff no repeated capture');
  record('pending handoff: recorded, no promise of delivery or automatic retry',report);
  await evaluate(`auditReset();auditConfig.trusted=true;$('phone').value='2025550102';await checkIn();true`);
  report=await inspect();
  assert(report.balanceVisible && !report.joinVisible && counts(report,'/api/complete-profile')===0 && counts(report,'/api/consent/winback')===0 && !report.checked,'returning rewards bypass profile');
  record('returning rewards: balance directly, no profile or marketing enrollment',report);
  await evaluate(`auditReset();auditConfig.newRewards=true;$('phone').value='2025550103';await checkIn();$('verifyCode').value='123456';await verifyCodeAndCheckIn();true`);
  report=await inspect();
  assert(report.joinVisible && counts(report,'/api/consent/winback')===0,'new rewards join');
  await evaluate(`auditConfig.points=0;auditConfig.refused='closed';$('fname').value='';$('joinBtn').click();while(busy)await new Promise(r=>setTimeout(r,5));true`);
  report=await inspect();
  const joined=report.requests.find(x=>x.path==='/api/sms-optin');
  assert(report.balanceVisible && report.points==='0' && report.award.includes('closed') && counts(report,'/api/points-checkin')===2 && counts(report,'/api/consent/winback')===0,'new rewards real checkin no synthetic point');
  assert(joined.credentials==='include' && joined.body.purpose==='rewards' && joined.body.sms_consent===false && joined.body.first_name==='' && !('email' in joined.body) && !('last_name' in joined.body),'minimal rewards join');
  record('new rewards: optional name, real second check-in, server refusal respected',report);
  await evaluate(`auditConfig.trusted=true;$('offerConsent').checked=true;await startFlow('offers');true`);
  report=await inspect();
  assert(report.offerCaptured && counts(report,'/api/verification/start')===1 && counts(report,'/api/verification/check')===1 && counts(report,'/api/points-checkin')===2,'reuse verified phone for offers without a second OTP or checkin');
  record('rewards verification reused for optional offers without a second OTP',report);
  await evaluate(`auditReset();auditConfig.newRewards=true;$('phone').value='2025550104';await checkIn();$('staffVerifyPin').value='offline-staff-pin';await staffCheckIn();true`);
  report=await inspect();
  assert(report.joinVisible && report.staffPin==='offline-staff-pin' && report.staffInput==='','staff PIN only held for pending join');
  await evaluate(`auditConfig.points=1;auditConfig.awarded=true;$('joinBtn').click();while(busy)await new Promise(r=>setTimeout(r,5));true`);
  report=await inspect();
  assert(report.balanceVisible && report.points==='1' && report.geoCalls===0 && report.staffPin==='' && report.staffInput==='' && counts(report,'/api/consent/winback')===0,'staff rewards preserved and cleared');
  assert(report.requests.filter(x=>x.path==='/api/points-checkin'||x.path==='/api/sms-optin').every(x=>x.body.pin==='offline-staff-pin'),'staff PIN forwarded narrowly');
  assert(report.requests.filter(x=>x.body&&x.body.pin).every(x=>['/api/points-checkin','/api/sms-optin'].includes(x.path)),'staff PIN never in consent or verification');
  record('staff new rewards: transient PIN survives join then clears, no consent',report);
  await evaluate(`$('offerConsent').checked=true;await startFlow('offers');true`);
  report=await inspect();
  assert(report.verifyVisible && !report.staffVisible && counts(report,'/api/consent/winback')===0,'staff session cannot bypass offer verification');
  record('staff account still requires phone proof for optional offers',report);
  await evaluate(`$('verifyBackBtn').click();true`);
  report=await inspect();
  assert(report.staffPin==='' && report.staffInput==='' && !report.checked,'back resets identity/consent');
  record('back clears staff authority and opt-in choice',report);
  await evaluate(`auditReset();auditConfig.trusted=true;auditConfig.failPath='/api/sms-optin';${chooseOffers}true`);
  report=await inspect();
  assert(!report.offerCaptured && counts(report,'/api/consent/winback')===0 && report.offerResult.includes('rejected'),'account failure prevents consent');
  record('failed account setup cannot claim captured consent',report);
  await evaluate(`auditReset();auditConfig.trusted=true;auditConfig.throwPath='/api/consent/winback';${chooseOffers}true`);
  report=await inspect();
  assert(!report.offerCaptured && counts(report,'/api/consent/winback')===1 && !report.offerResult.includes('recorded'),'uncertain consent cannot claim success/retry');
  record('uncertain consent result has no success claim or automatic retry',report);
  await evaluate(`auditReset();auditConfig.failPath='/api/verification/status';${chooseOffers}true`);
  report=await inspect();
  assert(counts(report,'/api/sms-optin')===0 && counts(report,'/api/consent/winback')===0,'failed trust lookup blocks all later writes');
  record('failed verification lookup stops signup',report);
  await evaluate(`auditReset();${chooseOffers}auditConfig.badCode=true;$('verifyCode').value='123456';await verifyCodeAndCheckIn();true`);
  report=await inspect();
  assert(report.verifyVisible && counts(report,'/api/sms-optin')===0,'bad code blocks account/consent');
  record('bad OTP blocks account creation and consent',report);
  await evaluate(`auditReset();auditConfig.trusted=true;${chooseOffers}$('offerDoneBtn').click();true`);
  report=await inspect();
  assert(!report.checked && !report.checkboxDisabled && report.submitDisabled && report.staffPin==='','fresh visit unchecked and enabled');
  record('Done resets the next visit to unchecked optional consent',report);
  const tracker = await evaluate(`({advancedMatching:(window.fbq?.queue||[]).some(x=>x[0]==='init'&&x[2]),pageView:(window.fbq?.queue||[]).some(x=>x[0]==='track'&&x[1]==='PageView')})`);
  assert(!tracker.advancedMatching && !tracker.pageView && blocked.length===0,'saved-decline tracking guard');
  const screenshot=await send('Page.captureScreenshot',{format:'png'});
  await fs.writeFile('/tmp/nh-rewards-one-page.png',Buffer.from(screenshot.data,'base64'));
  const final={mode:'isolated Chromium, synthetic API fixtures, all requests intercepted, DNS disabled',liveProviderRequests:0,scenariosPassed:scenarios.length,scenarios,tracker,blockedRequests:blocked};
  console.log(JSON.stringify(final,null,2));
} finally {
  socket?.close();chrome.kill('SIGTERM');
  await new Promise(resolve=>{if(chrome.exitCode!==null)resolve();else{chrome.once('exit',resolve);setTimeout(resolve,3000);}});
  await fs.rm(profile,{recursive:true,force:true});
}
