'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const html = fs.readFileSync(path.join(__dirname, '../sms/index.html'), 'utf8');

test('legacy SMS page redirects to the same rewards page and retains a visible fallback', () => {
  assert.match(html, /http-equiv="refresh" content="0;url=\/rewards\/"/);
  assert.match(html, /<a href="\/rewards\/">Continue to Rewards &amp; Text Offers<\/a>/);
  assert.doesNotMatch(html, /<form\b|<script\b|sms-optin|sms_consent|fetch\s*\(/i);
  assert.doesNotMatch(html, /You're Signed Up|confirmation message shortly/i);
});
