(function () {
  'use strict';
  if (window.portfolioMeasurementInstalled) return;
  // /rewards/ is an in-store member utility (noindex, member/staff only), not a
  // marketing page: no analytics there, and therefore no consent prompt. Added
  // 9/11/2026 after NCN's members hit the consent box on the check-in screen —
  // that club's members are largely in their 70s-90s. Kiosk traffic is noise in
  // the site's real analytics anyway: one device, repeat check-ins, no acquisition.
  if (/^\/rewards(\/|$)/.test(location.pathname)) return;
  const sites = {
    'casagrandenutrition.com': ['G-JLK792RFT7', true],
    'nebraskacitynutrition.com': ['G-REDP4GDLT1', true],
    'route66nutritionspot.com': ['G-7EEMSETNP8', true],
    'nutritionhub101.com': ['G-8ETNVVHQCD', false],
    'broadwaynutrition.com': ['G-2YK4E9G7MQ', false],
    'houstoncarecompass.com': ['G-QDXZSDMGSW', false]
  };
  const host = location.hostname.replace(/^www\./, '');
  const site = sites[host];
  if (!site) return;
  window.portfolioMeasurementInstalled = true;
  const key = 'site_analytics_choice_v1';
  let choice = null;
  try { choice = localStorage.getItem(key); } catch (_) {}
  let loaded = false;
  function permitted() {
    if (site[1]) return choice === 'granted';
    if (host === 'nutritionhub101.com') return /(?:^|;\s*)nh_measurement_consent=granted(?:;|$)/.test(document.cookie);
    return typeof window.gtag === 'function';
  }
  function startMeasurement() {
    if (loaded || !permitted()) return;
    loaded = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
    window.gtag('consent', 'default', {analytics_storage:'granted', ad_storage:'denied', ad_user_data:'denied', ad_personalization:'denied'});
    window.gtag('js', new Date());
    // Exclude URL queries and fragments from the page context.
    window.gtag('config', site[0], {page_location:location.origin + location.pathname, page_referrer:document.referrer ? new URL(document.referrer).origin : '', allow_google_signals:false, allow_ad_personalization_signals:false});
    const script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=' + site[0];
    document.head.appendChild(script);
  }
  function setChoice(value) {
    choice = value;
    try { localStorage.setItem(key, value); } catch (_) {}
    if (value === 'granted') {
      if (loaded) window.gtag('consent','update',{analytics_storage:'granted'});
      else startMeasurement();
    } else if (loaded) {
      window.gtag('consent','update',{analytics_storage:'denied'});
      // Stop the loaded tag after withdrawal; the saved choice prevents reloading it.
      location.reload();
    }
    document.getElementById('site-analytics-choice')?.remove();
  }
  function showChoice() {
    if (document.getElementById('site-analytics-choice')) return;
    const box = document.createElement('section');
    box.id = 'site-analytics-choice';
    box.setAttribute('aria-label','Analytics choices');
    box.innerHTML = '<strong>Website analytics</strong><p>Allow Google Analytics to measure visits and contact-button clicks? You can change your choice using Analytics choices at the bottom of the page.</p><button type="button" data-choice="denied">Decline</button> <button type="button" data-choice="granted">Allow analytics</button>';
    box.style.cssText = 'position:fixed;z-index:100000;bottom:16px;left:16px;right:16px;max-width:640px;margin:auto;padding:18px;background:white;color:#182a25;border:1px solid #61796d;border-radius:12px;box-shadow:0 4px 24px #0003;font:15px/1.5 system-ui';
    box.querySelectorAll('button').forEach(b => {
      b.style.cssText = 'padding:10px 14px;background:#fff;color:#183e31;border:1px solid #183e31;border-radius:6px;font:inherit;cursor:pointer';
      b.addEventListener('click', () => setChoice(b.dataset.choice));
    });
    document.body.appendChild(box);
  }
  function start() {
    if (site[1]) {
      const prefs = document.createElement('button');
      prefs.type = 'button';
      prefs.textContent = 'Analytics choices';
      prefs.style.cssText = 'display:block;margin:16px auto;padding:8px 12px;background:#fff;color:#183e31;border:1px solid #183e31;border-radius:6px;cursor:pointer';
      prefs.addEventListener('click', showChoice);
      document.body.appendChild(prefs);
      if (choice === 'granted') startMeasurement();
      else if (choice !== 'denied') showChoice();
    }
    document.addEventListener('click', function (event) {
      const a = event.target.closest?.('a[href]');
      if (!a || !permitted() || typeof window.gtag !== 'function') return;
      const href = a.getAttribute('href') || '';
      let name;
      if (/^tel:/i.test(href)) name = 'phone_click';
      else if (/^mailto:/i.test(href)) name = 'email_click';
      else if (/^sms:/i.test(href)) name = 'sms_click';
      else {
        let url; try { url = new URL(href, location.href); } catch (_) { return; }
        if (url.hostname === 'www.google.com' && url.pathname.startsWith('/maps/dir')) name = 'directions_click';
        else if (host === 'nutritionhub101.com' && url.hostname === 'order.nutritionhub101.com') name = 'order_site_click';
      }
      if (host === 'houstoncarecompass.com') {
        if (name === 'phone_click') name = 'directory_phone_click';
        if (name === 'sms_click') name = 'directory_sms_click';
        if (name === 'email_click') name = /^mailto:advertise@houstoncarecompass\.com(?:\?|$)/i.test(href) ? 'advertising_email_click' : 'directory_email_click';
      }
      if (name) window.gtag('event', name, {send_to:site[0], transport_type:'beacon'});
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start, {once:true});
  else start();
})();
