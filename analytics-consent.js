(function () {
  'use strict';

  const GA_MEASUREMENT_ID = 'G-8ETNVVHQCD';
  const META_PIXEL_ID = '915336731481586';
  const CONSENT_COOKIE = 'nh_measurement_consent';
  const COOKIE_MAX_AGE = 60 * 60 * 24 * 180;
  const ALLOWED_EVENTS = new Set(['add_to_cart', 'begin_checkout', 'purchase', 'rewards_join']);

  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
  window.gtag('consent', 'default', {
    analytics_storage: 'denied',
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied',
    wait_for_update: 500,
  });

  let measurementLoaded = false;

  function readChoice() {
    const match = document.cookie.match(new RegExp('(?:^|; )' + CONSENT_COOKIE + '=([^;]*)'));
    return match ? decodeURIComponent(match[1]) : null;
  }

  function saveChoice(choice) {
    document.cookie = `${CONSENT_COOKIE}=${encodeURIComponent(choice)}; Max-Age=${COOKIE_MAX_AGE}; Path=/; Domain=.nutritionhub101.com; SameSite=Lax; Secure`;
  }

  function appendScript(src, id) {
    if (document.getElementById(id)) return;
    const script = document.createElement('script');
    script.async = true;
    script.id = id;
    script.src = src;
    document.head.appendChild(script);
  }

  function loadMetaPixel() {
    const rewardsPage = location.hostname === 'nutritionhub101.com' && /^\/rewards\/?$/.test(location.pathname || '');
    if (location.hostname !== 'order.nutritionhub101.com' && !rewardsPage) return;
    if (window.fbq) {
      window.fbq('consent', 'grant');
      return;
    }
    const fbq = window.fbq = function () {
      fbq.callMethod ? fbq.callMethod.apply(fbq, arguments) : fbq.queue.push(arguments);
    };
    if (!window._fbq) window._fbq = fbq;
    fbq.push = fbq;
    fbq.loaded = true;
    fbq.version = '2.0';
    fbq.queue = [];
    appendScript('https://connect.facebook.net/en_US/fbevents.js', 'nh-meta-pixel');
    fbq('consent', 'grant');
    fbq('init', META_PIXEL_ID);
    fbq('track', 'PageView');
  }

  function loadMeasurement() {
    window.gtag('consent', 'update', {
      analytics_storage: 'granted',
      ad_storage: 'granted',
      ad_user_data: 'denied',
      ad_personalization: 'denied',
    });
    if (measurementLoaded) {
      loadMetaPixel();
      return;
    }
    measurementLoaded = true;
    appendScript(`https://www.googletagmanager.com/gtag/js?id=${GA_MEASUREMENT_ID}`, 'nh-ga4');
    window.gtag('js', new Date());
    window.gtag('config', GA_MEASUREMENT_ID, {
      allow_google_signals: false,
      allow_ad_personalization_signals: false,
      cookie_domain: 'nutritionhub101.com',
      linker: {domains: ['nutritionhub101.com', 'order.nutritionhub101.com']},
    });
    loadMetaPixel();
  }

  function ecommerceItems(items) {
    if (!Array.isArray(items)) return [];
    return items.slice(0, 100).map(item => ({
      item_id: String(item.item_id || '').slice(0, 100),
      price: Number(item.price) || 0,
      quantity: Math.max(1, Math.round(Number(item.quantity) || 1)),
    })).filter(item => item.item_id);
  }

  function track(eventName, parameters) {
    if (readChoice() !== 'granted' || !ALLOWED_EVENTS.has(eventName)) return false;
    if (eventName === 'rewards_join') {
      // Only an aggregate event: never pass form values or caller parameters.
      window.gtag('event', 'rewards_join', {content_name: 'rewards_join'});
      if (window.fbq) window.fbq('track', 'Lead', {content_name: 'rewards_join'});
      return true;
    }
    const input = parameters || {};
    const event = {
      currency: input.currency === 'USD' ? 'USD' : undefined,
      value: Number.isFinite(Number(input.value)) ? Number(input.value) : undefined,
      items: ecommerceItems(input.items),
    };
    if (eventName === 'purchase') {
      event.transaction_id = String(input.transaction_id || '').slice(0, 100);
      if (!event.transaction_id) return false;
    }
    window.gtag('event', eventName, event);
    return true;
  }

  function removeBanner() {
    document.getElementById('nh-consent-banner')?.remove();
  }

  function setChoice(choice) {
    saveChoice(choice);
    removeBanner();
    if (choice === 'granted') {
      loadMeasurement();
    } else {
      window.gtag('consent', 'update', {
        analytics_storage: 'denied',
        ad_storage: 'denied',
        ad_user_data: 'denied',
        ad_personalization: 'denied',
      });
      if (window.fbq) window.fbq('consent', 'revoke');
    }
  }

  function showPreferences() {
    if (document.getElementById('nh-consent-banner')) return;
    const banner = document.createElement('section');
    banner.id = 'nh-consent-banner';
    banner.setAttribute('role', 'dialog');
    banner.setAttribute('aria-label', 'Privacy choices');
    banner.innerHTML = `
      <div class="nh-consent-copy">
        <strong>Privacy choices</strong>
        <span>With your permission, Nutrition Hub uses analytics and advertising measurement to understand site visits and completed orders. We do not send your form entries to these tools. <a href="https://nutritionhub101.com/privacy-policy/">Privacy policy</a></span>
      </div>
      <div class="nh-consent-actions">
        <button type="button" data-choice="denied">Decline</button>
        <button type="button" data-choice="granted" class="nh-consent-accept">Accept</button>
      </div>`;
    banner.querySelectorAll('[data-choice]').forEach(button => {
      button.addEventListener('click', () => setChoice(button.dataset.choice));
    });
    document.body.appendChild(banner);
  }

  function addStyles() {
    if (document.getElementById('nh-consent-styles')) return;
    const styles = document.createElement('style');
    styles.id = 'nh-consent-styles';
    styles.textContent = `
      #nh-consent-banner{position:fixed;z-index:2147483646;left:16px;right:16px;bottom:16px;max-width:760px;margin:auto;padding:16px;border:1px solid #d8d8d8;border-radius:12px;background:#fff;color:#171717;box-shadow:0 8px 30px rgba(0,0,0,.2);font:14px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;display:flex;gap:18px;align-items:center}
      #nh-consent-banner .nh-consent-copy{display:grid;gap:4px;flex:1}#nh-consent-banner a{color:#0f5c29;text-decoration:underline}
      #nh-consent-banner .nh-consent-actions{display:flex;gap:8px}#nh-consent-banner button{border:1px solid #0f5c29;border-radius:8px;background:#fff;color:#0f5c29;padding:9px 14px;font-weight:700;cursor:pointer}
      #nh-consent-banner .nh-consent-accept{background:#0f5c29;color:#fff}@media(max-width:640px){#nh-consent-banner{align-items:stretch;flex-direction:column}#nh-consent-banner .nh-consent-actions{justify-content:flex-end}}
    `;
    document.head.appendChild(styles);
  }

  window.NHAnalytics = {track, showPreferences};

  function start() {
    addStyles();
    const choice = readChoice();
    if (choice === 'granted') loadMeasurement();
    else if (choice !== 'denied') showPreferences();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start, {once: true});
  else start();
})();
