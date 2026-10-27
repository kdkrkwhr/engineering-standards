const search = document.querySelector('#search');
const cards = [...document.querySelectorAll('.term-card')];
const filters = [...document.querySelectorAll('.filter')];
const nodes = [...document.querySelectorAll('.graph-node')];
const edges = [...document.querySelectorAll('.graph-edge')];
const relations = [...document.querySelectorAll('.relation')];
const count = document.querySelector('#count');
const empty = document.querySelector('#empty');
const selection = document.querySelector('#graph-selection');
let category = 'all';

function applyFilters() {
  const query = search.value.trim().toLocaleLowerCase();
  let shown = 0;
  for (const card of cards) {
    card.hidden = (category !== 'all' && card.dataset.category !== category) || !card.dataset.search.includes(query);
    if (!card.hidden) shown++;
  }
  count.textContent = `${shown} / ${cards.length}개 용어`;
  empty.hidden = shown !== 0;
  for (const node of nodes) {
    node.classList.toggle('is-muted', cards.find(card => card.id === node.dataset.node)?.hidden ?? false);
  }
}
function setCategory(next) {
  category = next;
  for (const button of filters) {
    const active = button.dataset.filter === next;
    button.classList.toggle('is-active', active);
    button.setAttribute('aria-pressed', String(active));
  }
  applyFilters();
}
function highlight(from, to, fromLabel, toLabel) {
  for (const node of nodes) node.classList.toggle('is-selected', node.dataset.node === from || node.dataset.node === to);
  for (const edge of edges) {
    const active = edge.dataset.from === from && edge.dataset.to === to;
    edge.classList.toggle('is-selected', active);
    edge.classList.toggle('is-muted', !active);
  }
  for (const button of relations) button.classList.toggle('is-selected', button.dataset.from === from && button.dataset.to === to);
  selection.textContent = `${fromLabel} → ${toLabel} · 수동 제안 관계. 아래 용어 카드에서 근거를 확인하세요.`;
}
search.addEventListener('input', applyFilters);
for (const button of filters) button.addEventListener('click', () => setCategory(button.dataset.filter));
document.querySelector('#clear-search').addEventListener('click', () => {
  search.value = '';
  setCategory('all');
  search.focus();
});
for (const button of relations) button.addEventListener('click', () => {
  search.value = '';
  setCategory('all');
  highlight(button.dataset.from, button.dataset.to, button.dataset.fromLabel, button.dataset.toLabel);
});
for (const node of nodes) node.addEventListener('click', event => {
  const card = document.getElementById(node.dataset.node);
  if (!card) return;
  event.preventDefault();
  search.value = '';
  setCategory('all');
  for (const other of nodes) other.classList.toggle('is-selected', other === node);
  for (const edge of edges) edge.classList.remove('is-muted', 'is-selected');
  for (const button of relations) button.classList.remove('is-selected');
  selection.textContent = `${card.querySelector('h3').firstChild.textContent} 선택됨. 카드에서 뜻과 출처를 확인하세요.`;
  card.scrollIntoView({block: 'start', behavior: 'smooth'});
  card.focus({preventScroll: true});
});
document.addEventListener('keydown', event => {
  if (event.key === '/' && document.activeElement !== search && !['INPUT', 'TEXTAREA'].includes(document.activeElement?.tagName)) {
    event.preventDefault();
    search.focus();
  }
  if (event.key === 'Escape' && document.activeElement === search) {
    search.value = '';
    applyFilters();
  }
});
applyFilters();
