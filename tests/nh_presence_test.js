// Extracts the REAL presence functions out of menu/server.js and exercises them.
// Run:  node tests/nh_presence_test.js menu/server.js
// menu/ is gitignored (it holds live Clover + GHL credentials as fallback
// defaults), so this test lives here to make sure it is version-controlled.
// Not a re-implementation: the function bodies under test are the shipped text.
const fs = require('fs');
const src = fs.readFileSync(process.argv[2], 'utf8');

function grab(name, kind='function') {
  const start = src.indexOf(`${kind} ${name}`);
  if (start < 0) throw new Error(`could not find ${name}`);
  let i = src.indexOf('{', start), depth = 0;
  for (let j = i; j < src.length; j++) {
    if (src[j] === '{') depth++;
    else if (src[j] === '}') { depth--; if (!depth) return src.slice(start, j + 1); }
  }
  throw new Error(`unbalanced ${name}`);
}

const STORE_LAT = 29.559174207251, STORE_LNG = -95.345263434633;
let GEO_RADIUS_M = 150, GEO_MAX_ACCURACY_M = 1000, STORE_TZ = 'America/Chicago';
let STORE_HOURS = {};
const hhmmToMins = t => { const [h,m] = String(t).split(':').map(Number); return h*60+m; };
eval(grab('milesBetween'));
eval(grab('localNow'));
eval(grab('storeIsOpen'));
eval(grab('presenceVerdict'));

let P=0,F=0;
const chk=(l,c,g='')=>{ c?P++:F++; console.log(`  ${c?'✅':'❌'} ${l}` + (c?'':`  got=${JSON.stringify(g)}`)); };

STORE_HOURS = {mon:["00:00","23:59"],tue:["00:00","23:59"],wed:["00:00","23:59"],
               thu:["00:00","23:59"],fri:["00:00","23:59"],sat:["00:00","23:59"],sun:["00:00","23:59"]};

console.log('=== distance math (Pearland store) ===');
let v = presenceVerdict({lat:STORE_LAT, lng:STORE_LNG, accuracy:15});
chk('at the counter -> inside, ~0m', v.geo==='inside' && v.distance_m < 10, v);
chk('and would allow', v.wouldAllow===true, v);

v = presenceVerdict({lat:STORE_LAT+0.001, lng:STORE_LNG, accuracy:15});   // ~111 m
chk('~111m -> still inside 150m fence', v.geo==='inside', v);
v = presenceVerdict({lat:STORE_LAT+0.0027, lng:STORE_LNG, accuracy:15});  // ~300 m
chk('~300m -> outside', v.geo==='outside' && v.reason==='far', v);
v = presenceVerdict({lat:29.7604, lng:-95.3698, accuracy:15});            // downtown Houston
chk('downtown Houston -> outside', v.geo==='outside', v);
chk('  and the distance is sane (~22km)', v.distance_m>19000 && v.distance_m<26000, v.distance_m);

console.log('=== degraded location must never read as "far" ===');
v = presenceVerdict({});
chk('no coords -> no_location', v.reason==='no_location' && v.wouldAllow===false, v);
v = presenceVerdict({lat:29.7604, lng:-95.3698, accuracy:3000});
chk('vague fix far away -> no_location, NOT far', v.reason==='no_location', v);
v = presenceVerdict({lat:'abc', lng:'def', accuracy:10});
chk('junk coords -> no_location', v.reason==='no_location', v);

console.log('=== store hours (Central, not UTC) ===');
STORE_HOURS = {};
chk('no hours configured -> not blocked', presenceVerdict({lat:STORE_LAT,lng:STORE_LNG,accuracy:10}).open===true);
STORE_HOURS = {mon:["06:30","17:00"]};   // only Mondays
const isMon = new Intl.DateTimeFormat('en-US',{timeZone:STORE_TZ,weekday:'short'}).format(new Date()).toLowerCase().startsWith('mon');
v = presenceVerdict({lat:STORE_LAT,lng:STORE_LNG,accuracy:10});
chk(`only-Monday schedule, today is ${isMon?'Monday':'not Monday'} -> open=${v.open}`, v.open===isMon, v);
if (!isMon) chk('  at the counter but closed -> refused as "closed"', v.reason==='closed', v);

console.log(`\n${P} passed, ${F} failed`);
process.exit(F?1:0);
