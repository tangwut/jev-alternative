import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { createContext, runInContext } from 'node:vm';

test('replay renders recorded decisions without a backend and resets when switching scenarios', () => {
  const source = new URL('../replay.js', import.meta.url);
  assert.ok(existsSync(source), 'Missing offline replay interface');
  const element = () => ({ textContent:'', value:'support', disabled:false, style:{}, dataset:{},
    children:[], className:'', setAttribute() {}, replaceChildren() { this.children=[]; },
    append(...items) { this.children.push(...items); } });
  const elements = new Map();
  const document = { getElementById(id) { if (!elements.has(id)) elements.set(id, element()); return elements.get(id); }, createElement:element };
  const timers = new Map();
  let timerId = 0;
  const record = (id, choice) => ({ id, request:{ state:{message:id}, questions:{route:{type:'choice',criteria:{a:'first',b:'second'}}} },
    response:{answers:{route:{choice,probabilities:{a:0.75,b:0.25}}},routing:{model:'multilingual'}}, elapsed_ms:20 });
  const context = createContext({ document, window:{LayaRecordings:{metadata:{recorded_on:'2026-10-10',device:'cpu',platform:'test'},records:[record('support','a'),record('agent','b')]}},
    setTimeout(callback) { timers.set(++timerId,callback); return timerId; }, clearTimeout(id) { timers.delete(id); },
    fetch() { assert.fail('offline replay must not send network requests'); } });
  runInContext(readFileSync(source,'utf8'),context);
  assert.match(elements.get('request').textContent,/support/);
  elements.get('replay').onclick();
  for (let i=0; i<2; i++) { const [id,callback]=timers.entries().next().value; timers.delete(id); callback(); }
  assert.equal(elements.get('decision').textContent,'a');
  assert.equal(elements.get('replay').disabled,false);
  elements.get('replay').onclick();
  elements.get('scenario').value='agent';
  elements.get('scenario').onchange();
  assert.equal(timers.size,0,'switching must cancel the previous replay');
  assert.match(elements.get('request').textContent,/agent/);
  assert.equal(elements.get('decision').textContent,'Ready to replay');
});
