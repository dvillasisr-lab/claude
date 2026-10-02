/* Gift Evil (sections/hm-gift-card.liquid): card amount follows the chosen variant, "Email it to them" turns on
   Shopify's native gift card recipient properties, client-side checks (email, date up to 90 days, 200 chars),
   add to cart through window.HMCart (hm-cart.js). Without HMCart, or when the store answers with a page
   instead of JSON, the form posts to /cart/add normally. */
(function () {
  'use strict';

  function iso(d) { return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0'); }

  function Gift(root) {
    this.root = root;
    this.form = root.querySelector('[data-hm-gift-form]');
    if (!this.form) return;
    var q = this.q.bind(this);
    this.btn = q('[data-hm-gift-add]');
    this.rcp = q('[data-hm-gift-rcp]');
    this.them = root.querySelector('input[name="hm_gift_who"][value="them"]');
    this.email = q('[data-hm-gift-email]');
    this.name = q('[data-hm-gift-name]');
    this.date = q('[data-hm-gift-date]');
    this.msg = q('[data-hm-gift-msg]');
    this.flag = q('[data-hm-gift-flag]');
    this.offset = q('[data-hm-gift-offset]');
    this.status = q('[data-hm-gift-status]');
    this.label = root.getAttribute('data-add-label') || 'Add to cart';

    var d0 = new Date(), d1 = new Date(); d1.setDate(d1.getDate() + 90);
    this.min = iso(d0); this.max = iso(d1);
    this.date.min = this.min; this.date.max = this.max;

    this.onChange = this.change.bind(this);
    this.onInput = this.input.bind(this);
    this.onSubmit = this.submit.bind(this);
    this.form.addEventListener('change', this.onChange);
    this.form.addEventListener('input', this.onInput);
    this.form.addEventListener('submit', this.onSubmit);
    this.who(false);
    this.sync();
  }
  Gift.prototype.q = function (s) { return this.root.querySelector(s); };
  Gift.prototype.variant = function () { return this.form.querySelector('input[name="id"]:checked'); };
  Gift.prototype.isThem = function () { return !!(this.them && this.them.checked); };

  Gift.prototype.sync = function () {
    var v = this.variant(); if (!v) return;
    var amt = this.q('[data-hm-gift-amt]'), price = this.q('[data-hm-gift-price]');
    if (amt) amt.textContent = v.getAttribute('data-amount');
    if (price) price.textContent = v.getAttribute('data-price');
    /* keep ?variant= in the URL so a shared link opens on the same amount */
    try { var u = new URL(location.href); u.searchParams.set('variant', v.value); history.replaceState(history.state, '', u.toString()); } catch (e) {}
  };

  Gift.prototype.who = function (focus) {
    var on = this.isThem();
    this.rcp.hidden = !on;
    if (this.them) this.them.setAttribute('aria-expanded', String(on));
    [this.email, this.name, this.date, this.msg, this.flag, this.offset].forEach(function (f) { if (f) f.disabled = !on; });
    if (this.offset) this.offset.value = String(new Date().getTimezoneOffset());
    if (on && focus) this.email.focus();
  };

  Gift.prototype.change = function (e) {
    var t = e.target;
    if (t.name === 'id') this.sync();
    else if (t.name === 'hm_gift_who') this.who(true);
    else if (t === this.date) this.checkDate();
  };

  Gift.prototype.input = function (e) {
    var t = e.target;
    if (t === this.msg) this.q('[data-hm-gift-cnt]').textContent = this.msg.value.length + ' / 200';
    if (t === this.email && this.email.getAttribute('aria-invalid')) this.setErr(this.email, '[data-hm-gift-email-err]', '');
    if (t === this.date && this.date.getAttribute('aria-invalid')) this.setErr(this.date, '[data-hm-gift-date-err]', '');
  };

  Gift.prototype.setErr = function (field, sel, text) {
    var el = this.q(sel);
    if (el) el.textContent = text;
    if (text) field.setAttribute('aria-invalid', 'true'); else field.removeAttribute('aria-invalid');
  };

  Gift.prototype.checkEmail = function () {
    var v = this.email.value.trim();
    var ok = v && this.email.checkValidity() && /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v);
    this.setErr(this.email, '[data-hm-gift-email-err]', ok ? '' : (v ? 'Check the email address.' : 'Enter their email so we know where to send it.'));
    return !!ok;
  };
  Gift.prototype.checkDate = function () {
    var v = this.date.value;
    var bad = v && (!/^\d{4}-\d{2}-\d{2}$/.test(v) || v < this.min || v > this.max);
    this.setErr(this.date, '[data-hm-gift-date-err]', bad ? 'Pick a day between today and 90 days from now.' : '');
    return !bad;
  };

  Gift.prototype.submit = function (e) {
    var self = this, v = this.variant();
    this.status.textContent = '';
    if (!v) { e.preventDefault(); return; }
    var props = null;
    if (this.isThem()) {
      if (!this.checkEmail()) { e.preventDefault(); this.email.focus(); return; }
      if (!this.checkDate()) { e.preventDefault(); this.date.focus(); return; }
      if (this.msg.value.length > 200) this.msg.value = this.msg.value.slice(0, 200);
      props = { __shopify_send_gift_card_to_recipient: 'on', 'Recipient email': this.email.value.trim() };
      if (this.name.value.trim()) props['Recipient name'] = this.name.value.trim();
      if (this.msg.value.trim()) props.Message = this.msg.value.trim();
      if (this.date.value) props['Send on'] = this.date.value;
      props.__shopify_offset = String(new Date().getTimezoneOffset());
    }
    if (!window.HMCart) return; /* no drawer: classic form post to /cart/add */
    e.preventDefault();
    var item = { id: Number(v.value), quantity: 1 };
    if (props) item.properties = props;
    var btn = this.btn, old = btn.innerHTML;
    btn.setAttribute('aria-busy', 'true'); btn.textContent = 'Adding…';
    window.HMCart.add([item], { returnFocus: btn }).then(function () {
      btn.removeAttribute('aria-busy'); btn.innerHTML = old;
    }).catch(function (err) {
      btn.removeAttribute('aria-busy'); btn.innerHTML = old;
      if (err && err.notJson) { self.form.submit(); return; }
      var m = (err && err.message) || '';
      if (/email/i.test(m) && self.isThem()) { self.setErr(self.email, '[data-hm-gift-email-err]', 'Check the email address.'); self.email.focus(); return; }
      if (/send.?on|date/i.test(m) && self.isThem()) { self.setErr(self.date, '[data-hm-gift-date-err]', 'Pick a day between today and 90 days from now.'); self.date.focus(); return; }
      self.status.textContent = m || 'Something went wrong. Try again.';
    });
  };

  Gift.prototype.destroy = function () {
    if (!this.form) return;
    this.form.removeEventListener('change', this.onChange);
    this.form.removeEventListener('input', this.onInput);
    this.form.removeEventListener('submit', this.onSubmit);
  };

  function init(scope) {
    [].forEach.call((scope || document).querySelectorAll('[data-hm-gift]'), function (el) {
      if (el.hmGift) return;
      el.hmGift = new Gift(el);
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { init(); }); else init();
  document.addEventListener('shopify:section:load', function (e) { init(e.target); });
  document.addEventListener('shopify:section:unload', function (e) {
    [].forEach.call(e.target.querySelectorAll('[data-hm-gift]'), function (el) { if (el.hmGift) { el.hmGift.destroy(); el.hmGift = null; } });
  });
})();
