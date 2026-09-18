'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');

const page = fs.readFileSync(path.join(__dirname, '..', 'sms', 'index.html'), 'utf8');

test('SMS opt-in page requires an HTTP success and confirmed receipt', () => {
  assert.match(page, /!response\.ok/);
  assert.match(page, /receipt\.status === 'captured'/);
  assert.match(page, /result\.success === true && result\.contactId/);
});

test('SMS opt-in page keeps the form visible and actionable after failure', () => {
  const catchBody = page.match(/catch \(submissionError\) \{([\s\S]*?)\n  \}/)?.[1] || '';
  assert.doesNotMatch(catchBody, /success-section/);
  assert.match(catchBody, /error\.textContent/);
  assert.match(catchBody, /btn\.disabled = false/);
  assert.match(catchBody, /btn\.textContent = 'Sign Me Up'/);
});

test('consent checkbox remains explicit and required', () => {
  assert.match(page, /type="checkbox" id="consent" required/);
  assert.match(page, /Consent is not a condition of any purchase/);
  assert.match(page, /Reply STOP to cancel, HELP for help/);
});
