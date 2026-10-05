/* HM Contact: ?topic= preselect, order number field toggle, per-field checks before the native submit. */
(function () {
  'use strict';

  function init(root) {
    if (!root || root._hmContact) return;
    var form = root.querySelector('form.ct-form');
    if (!form) return;
    var topic = form.querySelector('[data-ct-topic]');
    var orderField = form.querySelector('[data-ct-order-field]');
    var status = form.querySelector('[data-ct-status]');
    var reqs = [].slice.call(form.querySelectorAll('[data-ct-req]'));

    var key = new URLSearchParams(location.search).get('topic');
    if (key && topic) {
      [].some.call(topic.options, function (o) {
        if (o.getAttribute('data-key') === key) { topic.value = o.value; return true; }
        return false;
      });
    }

    function syncOrder() {
      if (!topic || !orderField) return;
      var o = topic.options[topic.selectedIndex];
      var anyOrder = topic.querySelector('option[data-order]');
      orderField.hidden = !!anyOrder && !(o && o.hasAttribute('data-order'));
    }
    syncOrder();

    function errEl(i) { return document.getElementById(i.getAttribute('aria-describedby')); }
    function check(i) {
      var ok = i.value.trim() !== '' && i.checkValidity();
      i.setAttribute('aria-invalid', ok ? 'false' : 'true');
      var er = errEl(i);
      if (er) er.textContent = ok ? '' : (er.getAttribute('data-msg') || '');
      return ok;
    }

    function onSubmit(e) {
      var bad = reqs.filter(function (i) { return !check(i); });
      if (!bad.length) return;
      e.preventDefault();
      if (status) {
        status.className = 'ct-status full is-err';
        status.textContent = status.getAttribute('data-msg') || form.querySelector('.ct-err[data-msg]').getAttribute('data-msg');
      }
      bad[0].focus();
    }
    function onBlur(e) {
      var i = e.target;
      if (i.hasAttribute && i.hasAttribute('data-ct-req') && i.getAttribute('aria-invalid') === 'true') check(i);
    }

    if (topic) topic.addEventListener('change', syncOrder);
    form.addEventListener('submit', onSubmit);
    form.addEventListener('focusout', onBlur);

    /* after a native post, move focus to the result so screen readers hear it */
    var result = form.querySelector('[data-ct-success], [data-ct-server-error]');
    if (result) {
      result.focus();
      var first = form.querySelector('[aria-invalid="true"]');
      if (first && result.hasAttribute('data-ct-server-error')) first.focus();
    }

    root._hmContact = function () {
      if (topic) topic.removeEventListener('change', syncOrder);
      form.removeEventListener('submit', onSubmit);
      form.removeEventListener('focusout', onBlur);
      root._hmContact = null;
    };
  }

  function each(scope, fn) { [].forEach.call((scope || document).querySelectorAll('[data-hm-contact]'), fn); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { each(null, init); });
  else each(null, init);
  document.addEventListener('shopify:section:load', function (e) { each(e.target, init); });
  document.addEventListener('shopify:section:unload', function (e) { each(e.target, function (r) { if (r._hmContact) r._hmContact(); }); });
})();
