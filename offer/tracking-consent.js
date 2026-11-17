(() => {
  'use strict';
  const choiceName = 'nh_offer_tracking';
  const read = name => document.cookie.split('; ').find(c => c.startsWith(name + '='))?.split('=').slice(1).join('=');
  const write = (name, value) => { document.cookie = `${name}=${value}; Path=/offer; Max-Age=15552000; Secure; SameSite=Lax`; };
  // GHL's official embed loader recognizes cookie-config=all|essential.
  // Only an explicit offer-page choice grants tracking; missing/denied stays off.
  function sync(choice) {
    write('cookie-config', choice === 'accepted' ? 'all' : 'essential');
    // Ask the loader to re-read consent even after its polling window expires.
    document.dispatchEvent(new Event('visibilitychange'));
  }
  sync(read(choiceName));
  const panel = document.getElementById('offer-tracking-choice');
  const settings = document.getElementById('offer-tracking-settings');
  const status = document.getElementById('offer-tracking-status');
  function render() {
    const choice = read(choiceName);
    panel.hidden = choice === 'accepted' || choice === 'declined';
    status.textContent = choice === 'accepted' ? 'Ad measurement is on.' : 'Ad measurement is off.';
  }
  panel.querySelectorAll('[data-tracking-choice]').forEach(button => {
    button.addEventListener('click', () => {
      const choice = button.dataset.trackingChoice;
      if (!['accepted', 'declined'].includes(choice)) return;
      write(choiceName, choice);
      sync(choice);
      render();
      settings.focus();
    });
  });
  settings.addEventListener('click', () => { panel.hidden = false; panel.querySelector('button').focus(); });
  render();
})();
