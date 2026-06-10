/**
 * Injiziert ein echtes ActiveCampaign-Formular in eine Freebie-Landingpage,
 * ersetzt den Platzhalter-Block und legt das Brand-Styling drüber.
 *
 * Run: node scripts/landing-pages/inject-ac-form.js <slug> <formId> <token> "<title>" "<buttonLabel>"
 * Danach: regeneriert auch wp-custom-html-block.html
 */
import { readFile, writeFile } from 'node:fs/promises';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..', '..');
const [slug, formId, token, title, buttonLabel] = process.argv.slice(2);
if (!slug || !formId || !token || !title || !buttonLabel) {
  console.error('Args: <slug> <formId> <token> "<title>" "<buttonLabel>"'); process.exit(1);
}

const F = formId;
const embed = `      <!-- ===== AC-Embed #${F} (Original von Patricia) ===== -->
      <style>
      #_form_${F}_{font-size:14px;line-height:1.6;font-family:arial,helvetica,sans-serif;margin:0;box-shadow:none}#_form_${F}_ input[type="text"],#_form_${F}_ textarea{padding:8px;height:auto;border:#979797 1px solid;border-radius:4px;color:#000 !important;font-size:14px;box-sizing:border-box}#_form_${F}_ input::placeholder{color:#142341}#_form_${F}_ ._submit{cursor:pointer;font-family:arial,sans-serif;font-size:14px;text-align:center;background:#ffffff !important;border:0 !important;border-radius:4px !important;color:#080808 !important;padding:10px !important}#_form_${F}_ ._submit:disabled{cursor:not-allowed;opacity:0.4}#_form_${F}_ ._form-branding{color:#fff;font-size:10px;clear:both;text-align:left;margin-top:30px;font-weight:100}#_form_${F}_ ._form-branding ._logo{display:block;width:130px;height:14px;margin-top:6px;background-image:url("https://d226aj4ao1t61q.cloudfront.net/hh9ujqgv5_aclogo_li.png");background-size:130px auto;background-repeat:no-repeat}#_form_${F}_ .form-sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);border:0}#_form_${F}_ ._form-label,#_form_${F}_ ._form_element ._form-label{font-weight:bold;margin-bottom:5px;display:block}#_form_${F}_ ._form_element{position:relative;margin-bottom:10px;max-width:100%}#_form_${F}_ ._form_element input[type="text"]{display:block;width:100%;box-sizing:border-box;font-family:inherit}#_form_${F}_ ._field-wrapper{position:relative}#_form_${F}_ ._full_width{width:100%}#_form_${F}_ input[type="text"]._has_error{border:#F37C7B 1px solid}#_form_${F}_ ._error{display:block;position:absolute;font-size:14px;z-index:10000001}#_form_${F}_ ._error._above{padding-bottom:4px;bottom:39px;right:0}#_form_${F}_ ._error._below{padding-top:8px;top:100%;right:0}#_form_${F}_ ._error-inner{padding:8px 12px;background-color:#FFDDDD;font-size:13px;font-family:arial,sans-serif;font-weight:600;line-height:16px;color:#000;border-radius:4px}#_form_${F}_ ._error-inner._form_error{margin-bottom:5px;text-align:left}#_form_${F}_ ._error-inner._no_arrow{margin-bottom:10px}#_form_${F}_ ._error-arrow{position:absolute;width:0;height:0}#_form_${F}_ ._form-title{font-family:sans-serif;font-size:24px;font-weight:400;color:black}#_form_${F}_ .field-required{color:#FF0000}#_form_${F}_{position:relative;text-align:left;margin:25px auto 0;padding:20px;box-sizing:border-box;background:#dc822e !important;border:0 !important;max-width:500px;border-radius:0 !important;color:#000000}#_form_${F}_ ._form-thank-you{position:relative;left:0;right:0;text-align:center;font-size:18px}#_form_${F}_ .g-recaptcha{margin-top:10px}
      </style>
      <form method="POST" action="https://mumlifebalance.activehosted.com/proc.php" id="_form_${F}_" class="_form _form_${F} _inline-form  " novalidate data-styles-version="5">
        <input type="hidden" name="u" value="${F}" />
        <input type="hidden" name="f" value="${F}" />
        <input type="hidden" name="s" />
        <input type="hidden" name="c" value="0" />
        <input type="hidden" name="m" value="0" />
        <input type="hidden" name="act" value="sub" />
        <input type="hidden" name="v" value="2" />
        <input type="hidden" name="or" value="${token}" />
        <div class="_form-content">
          <div class="_form_element _x07614776 _full_width _clear">
            <h2 class="_form-title">${title}</h2>
          </div>
          <div class="_form_element _x85148327 _full_width">
            <label for="fullname" class="_form-label">Vorname<span class="field-required">*</span></label>
            <div class="_field-wrapper"><input type="text" id="fullname" name="fullname" placeholder="Dein Vorname" required/></div>
          </div>
          <div class="_form_element _x44803942 _full_width">
            <label for="email" class="_form-label">E-Mail<span class="field-required">*</span></label>
            <div class="_field-wrapper"><input type="text" id="email" name="email" placeholder="Deine beste E-Mail-Adresse" required/></div>
          </div>
          <div class="_form_element _x25783284 _full_width">
            <fieldset class="_form-fieldset">
              <div class="_row"><legend for="field[1][]" class="_form-label">Datenschutz</legend></div>
              <input data-autofill="false" type="hidden" id="field[1][]" name="field[1][]" value="~|">
              <div class="_row _checkbox-radio">
                <input id="consent_${F}" type="checkbox" name="field[1][]" value="Ich möchte Patricias E-Mails mit Wissen und Angeboten rund ums Thema Onlinebusiness und Networkmarketing erhalten. Ich kann mich jederzeit abmelden." checked>
                <span><label for="consent_${F}">Ich möchte Patricias E-Mails mit Wissen und Angeboten rund ums Thema Onlinebusiness und Networkmarketing erhalten. Ich kann mich jederzeit abmelden.</label></span>
              </div>
            </fieldset>
          </div>
          <div class="_form_element _x47057123 _full_width">
            <label for="g-recaptcha-response" class="_form-label">Bitte bestätige hier deine Anfrage.<span class="field-required">*</span></label>
            <div class="g-recaptcha" data-sitekey="6LcwIw8TAAAAACP1ysM08EhCgzd6q5JAOUR1a0Go"></div>
          </div>
          <div class="_button-wrapper _full_width">
            <button id="_form_${F}_submit" class="_submit" type="submit">${buttonLabel}</button>
          </div>
          <div class="_clear-element"></div>
        </div>
        <div class="_form-thank-you" style="display:none;"></div>
        <div class="_form-branding"><div class="_marketing-by">Marketing von</div><a href="https://www.activecampaign.com/?utm_medium=referral&utm_campaign=acforms" class="_logo"><span class="form-sr-only">ActiveCampaign</span></a></div>
      </form>
      <script>
      window.cfields = {"1":"datenschutz"};
      window._show_thank_you = function(id, message, trackcmp_url, email) { var form = document.getElementById('_form_' + id + '_'), thank_you = form.querySelector('._form-thank-you'); form.querySelector('._form-content').style.display = 'none'; thank_you.innerHTML = message; thank_you.style.display = 'block'; if (typeof(trackcmp_url) != 'undefined' && trackcmp_url) { _load_script(trackcmp_url); } if (typeof window._form_callback !== 'undefined') window._form_callback(id); };
      window._show_error = function(id, message, html) { var form = document.getElementById('_form_' + id + '_'), err = document.createElement('div'), button = form.querySelector('button[type="submit"]'), old_error = form.querySelector('._form_error'); if (old_error) old_error.parentNode.removeChild(old_error); err.innerHTML = message; err.className = '_error-inner _form_error _no_arrow'; var wrapper = document.createElement('div'); wrapper.className = '_form-inner _show_be_error'; wrapper.appendChild(err); button.parentNode.insertBefore(wrapper, button); var submitButton = form.querySelector('[id^="_form"][id$="_submit"]'); submitButton.disabled = false; submitButton.classList.remove('processing'); };
      window._load_script = function(url, callback, isSubmit) { var head = document.querySelector('head'), script = document.createElement('script'), r = false; var submitButton = document.querySelector('#_form_${F}_submit'); script.charset = 'utf-8'; script.src = url; if (callback) { script.onload = script.onreadystatechange = function() { if (!r && (!this.readyState || this.readyState == 'complete')) { r = true; callback(); } }; } script.onerror = function() { if (isSubmit) { _show_error("${F}", "Ihre Übermittlung konnte nicht gesendet werden. Bitte versuchen Sie es erneut."); submitButton.disabled = false; submitButton.classList.remove('processing'); } } head.appendChild(script); };
      (function() {
          if (window.location.search.search("excludeform") !== -1) return false;
          var addEvent = function(el, ev, fn) { if (el.addEventListener) { el.addEventListener(ev, fn); } }
          var form_to_submit = document.getElementById('_form_${F}_');
          var allInputs = form_to_submit.querySelectorAll('input, select, textarea'), tooltips = [];
          var remove_tooltips = function() { for (var i = 0; i < tooltips.length; i++) { tooltips[i].tip.parentNode.removeChild(tooltips[i].tip); } tooltips = []; };
          var remove_tooltip = function(elem) { for (var i = 0; i < tooltips.length; i++) { if (tooltips[i].elem === elem) { tooltips[i].tip.parentNode.removeChild(tooltips[i].tip); tooltips.splice(i, 1); return; } } };
          var create_tooltip = function(elem, text) { var t = document.createElement('div'), a = document.createElement('div'), inr = document.createElement('div'), nt = {}; if (elem.type != 'radio' && elem.type != 'checkbox') { t.className = '_error'; a.className = '_error-arrow'; inr.className = '_error-inner'; inr.innerHTML = text; t.appendChild(a); t.appendChild(inr); elem.parentNode.appendChild(t); } else { t.className = '_error-inner _no_arrow'; t.innerHTML = text; elem.parentNode.insertBefore(t, elem); nt.no_arrow = true; } nt.tip = t; nt.elem = elem; tooltips.push(nt); return nt; };
          var validate_field = function(elem, remove) { var tooltip = null, value = elem.value, no_error = true; remove ? remove_tooltip(elem) : false; if (elem.type != 'checkbox') elem.className = elem.className.replace(/ ?_has_error ?/g, ''); if (elem.getAttribute('required') !== null) { if (elem.type == 'checkbox') { var elems = form_to_submit.elements[elem.name], found = false, err = []; for (var i = 0; i < elems.length; i++) { if (elems[i].getAttribute('required') === null) continue; if (!found && elems[i] !== elem) return true; found = true; elems[i].className = elems[i].className.replace(/ ?_has_error ?/g, ''); if (!elems[i].checked) { no_error = false; elems[i].className += ' _has_error'; err.push("Die Markierung von %s ist erforderlich.".replace("%s", elems[i].value)); } } if (!no_error) tooltip = create_tooltip(elem, err.join('<br/>')); } else if (value === undefined || value === null || value === '') { elem.className += ' _has_error'; no_error = false; tooltip = create_tooltip(elem, "Bitte füllen Sie das markierte Pflichtfeld aus."); } } if (no_error && elem.name == 'email') { if (!value.match(/^[\\+_a-z0-9-'&=]+(\\.[\\+_a-z0-9-']+)*@[a-z0-9-]+(\\.[a-z0-9-]+)*(\\.[a-z]{2,})$/i)) { elem.className += ' _has_error'; no_error = false; tooltip = create_tooltip(elem, "Geben Sie eine gültige E-Mail-Adresse ein."); } } return no_error; };
          var needs_validate = function(el) { if (el.getAttribute('required') !== null) return true; if (el.name === 'email' && el.value !== "") return true; return false; };
          var validate_form = function(e) { var no_error = true; remove_tooltips(); for (var i = 0, len = allInputs.length; i < len; i++) { var elem = allInputs[i]; if (needs_validate(elem)) { if (elem.tagName.toLowerCase() !== "select") { elem.value = elem.value.trim(); } validate_field(elem) ? true : no_error = false; } } if (!no_error && e) { e.preventDefault(); } return no_error; };
          window['recaptcha_callback'] = function() { var rcs = document.getElementsByClassName("g-recaptcha"); for (var i in rcs) { var rid = "recaptcha_" + i; rcs[i].id = rid; var el = document.getElementById(rid); if (el != null) { grecaptcha.render(rid, {"sitekey": el.getAttribute("data-sitekey")}); } } };
          _load_script("https://www.google.com/recaptcha/api.js?onload=recaptcha_callback&render=explicit");
          var _form_serialize = function(form){if(!form||form.nodeName!=="FORM"){return }var i,q=[];for(i=0;i<form.elements.length;i++){if(form.elements[i].name===""){continue}switch(form.elements[i].nodeName){case"INPUT":switch(form.elements[i].type){case"text":case"hidden":case"submit":q.push(form.elements[i].name+"="+encodeURIComponent(form.elements[i].value));break;case"checkbox":case"radio":if(form.elements[i].checked){q.push(form.elements[i].name+"="+encodeURIComponent(form.elements[i].value))}break}break}}return q.join("&")};
          var form_submit = function(e) { e.preventDefault(); if (validate_form()) { var submitButton = e.target.querySelector('#_form_${F}_submit'); submitButton.disabled = true; submitButton.classList.add('processing'); var serialized = _form_serialize(document.getElementById('_form_${F}_')).replace(/%0A/g, '\\\\n'); _load_script('https://mumlifebalance.activehosted.com/proc.php?' + serialized + '&jsonp=true', null, true); } return false; };
          addEvent(form_to_submit, 'submit', form_submit);
      })();
      </script>
      <!-- ===== Brand-Override (steht NACH dem Embed → gewinnt) ===== -->
      <style>
      #_form_${F}_ { max-width: 520px !important; margin: 0 auto !important; background: #f1ecdd !important; padding: 36px 32px !important; border-radius: 18px !important; color-scheme: light only; box-shadow: 0 10px 30px rgba(12,28,48,0.18) !important; text-align: left; }
      #_form_${F}_ ._form-title { font-family: 'Philosopher', Georgia, serif !important; color: #29556d !important; font-size: 20px !important; font-weight: 700 !important; line-height: 1.3 !important; text-align: center !important; margin-bottom: 18px !important; }
      #_form_${F}_ ._form-label, #_form_${F}_ legend._form-label { color: #29556d !important; font-weight: 700 !important; }
      #_form_${F}_ input[type="text"] { background: #ffffff !important; border: 1.5px solid rgba(41,85,109,0.2) !important; border-radius: 10px !important; padding: 12px !important; color: #0c1c30 !important; }
      #_form_${F}_ input::placeholder { color: #8a93a0 !important; }
      #_form_${F}_ ._submit { background: #dc822e !important; color: #ffffff !important; font-family: 'Source Sans 3', sans-serif !important; font-weight: 700 !important; font-size: 18px !important; padding: 16px 28px !important; border-radius: 14px !important; width: 100% !important; margin-top: 12px !important; cursor: pointer !important; }
      #_form_${F}_ ._submit:hover { transform: translateY(-2px); box-shadow: 0 8px 22px rgba(220,130,46,0.4); }
      #_form_${F}_ ._row._checkbox-radio { display: flex !important; align-items: flex-start !important; gap: 10px !important; padding: 10px 0 !important; }
      #_form_${F}_ ._row._checkbox-radio input[type="checkbox"] { margin-top: 3px !important; flex-shrink: 0 !important; width: 18px !important; height: 18px !important; }
      #_form_${F}_ ._row._checkbox-radio span { flex: 1 !important; }
      #_form_${F}_ ._row._checkbox-radio label { color: #0c1c30 !important; font-size: 13px !important; line-height: 1.55 !important; font-weight: 400 !important; }
      #_form_${F}_ legend._form-label { font-size: 14px !important; margin-bottom: 4px !important; }
      #_form_${F}_ ._form-branding { color: rgba(12,28,48,0.45) !important; margin-top: 18px !important; }
      </style>`;

const file = resolve(ROOT, 'outputs/funnels', slug, 'landing/index.html');
let html = await readFile(file, 'utf-8');
// Platzhalter-Block ersetzen: vom Platzhalter-Kommentar bis zum schliessenden </form>
const re = /      <!-- ⚠️ ActiveCampaign-Platzhalter[\s\S]*?<\/form>/;
if (!re.test(html)) { console.error('❌ Platzhalter nicht gefunden in ' + slug); process.exit(1); }
html = html.replace(re, embed);
await writeFile(file, html, 'utf-8');

// wp-custom-html-block.html neu erzeugen
const style = html.match(/<style>([\s\S]*?)<\/style>/)[0];
const body = html.match(/<body[^>]*>([\s\S]*?)<\/body>/)[1];
await writeFile(resolve(ROOT, 'outputs/funnels', slug, 'landing/wp-custom-html-block.html'),
  `<!-- Mum Life Balance · ${slug} · in Elementor "HTML"-Widget einfuegen -->\n${style}\n${body}`);
console.log('✓ ' + slug + ' → Form #' + F + ' eingebaut + Block regeneriert');
