// Exercise the published search script without adding a browser dependency.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');

function element(text = '') {
  const listeners = {};
  let ownText = text;
  return {
    get textContent() { return ownText + this.children.map(child => child.textContent).join(''); },
    set textContent(value) { ownText = value; this.children = []; },
    children: [],
    hidden: false,
    classList: { toggle() {}, remove() {} },
    addEventListener(type, handler) { listeners[type] = handler; },
    dispatch(type, event = {}) { listeners[type]?.(event); },
    append(...children) { this.children.push(...children); },
    replaceChildren(...children) { this.children = children; },
    setAttribute(name, value) { this[name] = value; },
    focus() { document.activeElement = this; },
    querySelector(selector) {
      if (this.parts?.[selector]) return this.parts[selector];
      for (const child of this.children) {
        if (child.tagName === selector.toUpperCase()) return child;
        const found = child.querySelector(selector);
        if (found) return found;
      }
      return null;
    },
  };
}

const search = element();
search.value = '';
const count = element();
const results = element();
const empty = element();
const clear = element();
const reset = element();
const selection = element();
const filters = ['all', 'common', 'spring'].map(name => {
  const button = element();
  button.dataset = { filter: name };
  return button;
});
function card(id, title, scope, meaning, searchable, category) {
  const item = element();
  item.id = id;
  item.dataset = { search: searchable, category };
  const heading = element();
  heading.firstChild = element(title);
  heading.parts = { span: element('English name') };
  item.parts = {
    h3: heading,
    'h3 span': heading.parts.span,
    '.term-meta .eyebrow': element(scope),
    p: element(meaning),
  };
  return item;
}
const cards = [
  card('domain-boundary', '도메인 경계', '공통', '도메인의 책임을 나누는 기준입니다.', '도메인 경계', 'common'),
  card('domain-model', '도메인 모델', 'Spring 예시', '비즈니스 규칙을 표현합니다.', '도메인 모델', 'spring'),
  card('api-contract', 'API 계약', '공통', '입출력의 약속입니다.', 'api 계약', 'common'),
];
const selectors = {
  '#search': search, '#count': count, '#search-results': results, '#empty': empty,
  '#clear-search': clear, '#reset-search': reset, '#graph-selection': selection,
};
const document = {
  activeElement: null,
  listeners: {},
  querySelector(selector) { return selectors[selector]; },
  querySelectorAll(selector) { return selector === '.term-card' ? cards : selector === '.filter' ? filters : []; },
  createElement(tag) { const node = element(); node.tagName = tag.toUpperCase(); return node; },
  getElementById(id) { return cards.find(item => item.id === id); },
  addEventListener(type, handler) { this.listeners[type] = handler; },
  dispatch(type, event) { this.listeners[type]?.(event); },
};
vm.runInNewContext(fs.readFileSync(path.join(__dirname, '../site/app.js'), 'utf8'), { document });

// Regression: matching card titles and context must be visible beside the search field.
search.value = '도메인';
search.dispatch('input');
assert.equal(count.textContent, '2개 검색 결과');
assert.equal(results.hidden, false);
assert.equal(results.children.length, 2);
assert.equal(results.children[0].children[0].href, '#domain-boundary');
assert.match(results.children[0].children[0].textContent, /도메인 경계/);
assert.match(results.children[0].children[0].textContent, /도메인의 책임/);
assert.equal(cards[2].hidden, true);

// A filtered scope also keeps only relevant results in the nearby list.
filters[2].dispatch('click');
assert.equal(results.children.length, 1);
assert.equal(results.children[0].children[0].href, '#domain-model');

search.value = '존재하지 않는 용어';
search.dispatch('input');
assert.equal(count.textContent, '0개 검색 결과');
assert.equal(results.hidden, true);
assert.equal(empty.hidden, false);
reset.dispatch('click');
assert.equal(search.value, '');
assert.equal(empty.hidden, true);
assert.equal(results.hidden, true);
assert.equal(count.textContent, '3 / 3개 용어');

search.value = '도메인';
search.dispatch('input');
search.dispatch('keydown', { key: 'ArrowDown', preventDefault() {} });
assert.equal(document.activeElement, results.children[0].children[0]);
results.children[0].children[0].dispatch('click');
assert.equal(document.activeElement, cards[0]);
search.focus();
document.dispatch('keydown', { key: 'Escape' });
assert.equal(search.value, '');
assert.equal(results.hidden, true);
clear.dispatch('click');
assert.equal(search.value, '');
assert.equal(results.hidden, true);
console.log('Nearby search results, filters, reset, and keyboard checks OK');
