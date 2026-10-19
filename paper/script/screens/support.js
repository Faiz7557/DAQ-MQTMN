// Runtime mini untuk merender file .dc.html dari kanvas mockup menjadi HTML statis.
// Hanya mendukung yang dipakai mockup Makhraj: {{lubang}}, <sc-for>, <sc-if>, <helmet>.
class DCLogic {
  constructor() { this.state = null; this.props = {}; }
  setState() {}
}

function lookup(expr, scopes) {
  const path = expr.trim().split('.');
  for (let i = scopes.length - 1; i >= 0; i--) {
    let v = scopes[i];
    if (v && Object.prototype.hasOwnProperty.call(v, path[0])) {
      for (const p of path) v = v == null ? undefined : v[p];
      return v;
    }
  }
  return undefined;
}

function interp(str, scopes) {
  return str.replace(/\{\{([^}]+)\}\}/g, (_, e) => {
    const v = lookup(e, scopes);
    return typeof v === 'function' || v == null ? '' : String(v);
  });
}

function unwrap(el) {
  const frag = document.createDocumentFragment();
  while (el.firstChild) frag.appendChild(el.firstChild);
  el.replaceWith(frag);
}

function processNode(node, scopes) {
  for (const child of [...node.childNodes]) {
    if (child.nodeType === 3) {
      if (child.nodeValue.includes('{{')) child.nodeValue = interp(child.nodeValue, scopes);
      continue;
    }
    if (child.nodeType !== 1) continue;
    const tag = child.tagName.toLowerCase();
    if (tag === 'sc-for') {
      const list = lookup(child.getAttribute('list').replace(/[{}]/g, ''), scopes) || [];
      const as = child.getAttribute('as');
      const frag = document.createDocumentFragment();
      for (const item of list) {
        const tmp = child.cloneNode(true);
        processNode(tmp, scopes.concat([{ [as]: item }]));
        while (tmp.firstChild) frag.appendChild(tmp.firstChild);
      }
      child.replaceWith(frag);
      continue;
    }
    if (tag === 'sc-if') {
      if (lookup(child.getAttribute('value').replace(/[{}]/g, ''), scopes)) {
        processNode(child, scopes);
        unwrap(child);
      } else {
        child.remove();
      }
      continue;
    }
    for (const a of [...child.attributes]) {
      if (a.name.startsWith('hint-')) { child.removeAttribute(a.name); continue; }
      if (!a.value.includes('{{')) continue;
      const whole = a.value.match(/^\{\{([^}]+)\}\}$/);
      if (whole && typeof lookup(whole[1], scopes) === 'function') {
        child.removeAttribute(a.name);
        continue;
      }
      child.setAttribute(a.name, interp(a.value, scopes));
    }
    processNode(child, scopes);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const script = document.querySelector('script[data-dc-script]');
  const Component = new Function('DCLogic', script.textContent + '\nreturn Component;')(DCLogic);
  const vals = new Component().renderVals();
  const root = document.querySelector('x-dc');
  const helmet = root.querySelector('helmet');
  if (helmet) {
    for (const n of [...helmet.childNodes]) document.head.appendChild(n);
    helmet.remove();
  }
  processNode(root, [vals]);
  unwrap(root);
});
