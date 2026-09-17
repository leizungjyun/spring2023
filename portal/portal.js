/* Static catalog, DOM-only rendering; all URLs are relative to the repository root. */
(() => {
  'use strict';
  const collections = [
    ['group-meetings', 'Group meetings'], ['research-talks', 'Research talks'],
    ['projects', 'Projects'], ['external-presentations', 'External presentations'],
    ['teaching', 'Teaching'], ['music', 'Music']
  ];
  const names = Object.fromEntries(collections);
  const $ = id => document.getElementById(id);
  let entries = [];
  let collection = '';
  const el = (tag, className, text) => {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  };
  const newest = (a,b) => (b.date || '').localeCompare(a.date || '') || a.title.localeCompare(b.title);
  function card(entry) {
    const article = el('article', 'presentation-card');
    const meta = el('div', 'card-meta');
    meta.append(el('span','collection-label', entry.series ? `${entry.series} · Lesson ${entry.lessonOrder}` : names[entry.collection]));
    const date = el(entry.date ? 'time' : 'span', '', entry.date || 'Undated');
    if(entry.date) date.dateTime = entry.date;
    meta.append(date); article.append(meta, el('h3','',entry.title));
    const tags = el('div','tags');
    entry.tags.forEach(tag => tags.append(el('span','tag',tag)));
    article.append(tags);
    if(entry.reviewNote) {
      const detail = el('details','review-note');
      detail.append(el('summary','','Catalog note'),el('p','',entry.reviewNote));
      article.append(detail);
    }
    const link = el('a','open-slides','Open slides ↗');
    link.href = entry.path;
    link.setAttribute('aria-label',`Open slides: ${entry.title}`);
    article.append(link);
    return article;
  }
  function filteredEntries() {
    const words = $('search').value.trim().toLowerCase().split(/\s+/).filter(Boolean);
    return entries.filter(e => (!collection || e.collection === collection) &&
      (!$('year').value || (e.date || '').startsWith($('year').value)) &&
      (!$('topic').value || e.tags.includes($('topic').value)) &&
      words.every(word => [e.title,e.series,names[e.collection],...e.tags].filter(Boolean).join(' ').toLowerCase().includes(word)));
  }
  function saveFilters() {
    const query = new URLSearchParams();
    for (const [key,value] of [['collection',collection],['q',$('search').value.trim()],['year',$('year').value],['topic',$('topic').value]]) if(value) query.set(key,value);
    history.replaceState(null,'',location.pathname+(query.size ? '?'+query.toString() : '')+location.hash);
  }
  function render(updateURL=true) {
    const filtered = filteredEntries();
    $('results').replaceChildren();
    $('result-count').textContent = `${filtered.length} presentation${filtered.length === 1 ? '' : 's'}`;
    $('empty-state').hidden = filtered.length !== 0;
    $('collections').querySelectorAll('button').forEach(b => b.setAttribute('aria-pressed',String(b.dataset.collection === collection)));
    for (const [key,label] of collections) {
      const items = filtered.filter(e=>e.collection===key);
      if(!items.length) continue;
      const group = el('section','collection-group');
      group.append(el('h3','collection-title',label));
      // Each course is kept together and ordered by lesson, independent of date.
      const standalone = items.filter(e=>!e.series).sort(newest);
      if(standalone.length) { const grid=el('div','card-grid');standalone.forEach(e=>grid.append(card(e)));group.append(grid); }
      const series = [...new Set(items.map(e=>e.series).filter(Boolean))].sort();
      series.forEach(name => {
        group.append(el('h4','series-title',name));
        const grid=el('div','card-grid');
        items.filter(e=>e.series===name).sort((a,b)=>a.lessonOrder-b.lessonOrder).forEach(e=>grid.append(card(e)));
        group.append(grid);
      });
      $('results').append(group);
    }
    $('recent').hidden = !!(collection || $('search').value || $('year').value || $('topic').value);
    if(updateURL) saveFilters();
  }
  function readFilters() {
    const q=new URLSearchParams(location.search);
    collection=names[q.get('collection')] ? q.get('collection') : '';
    $('search').value=q.get('q') || '';
    $('year').value=q.get('year') || '';
    $('topic').value=q.get('topic') || '';
  }
  async function init() {
    try {
      const response=await fetch('portal/catalog.json');
      if(!response.ok) throw new Error(`Catalog HTTP ${response.status}`);
      const catalog=await response.json();
      entries=catalog.presentations;
      if(!Array.isArray(entries)) throw new Error('Invalid catalog');
      $('library-stats').textContent=`${entries.length} presentations · ${collections.length} collections`;
      [['','All presentations'],...collections].forEach(([key,label])=>{
        const button=el('button','',label);button.type='button';button.dataset.collection=key;
        button.append(el('span','count',String(key ? entries.filter(e=>e.collection===key).length : entries.length)));
        button.addEventListener('click',()=>{collection=key;render();});
        $('collections').append(button);
      });
      [...new Set(entries.filter(e=>e.date).map(e=>e.date.slice(0,4)))].sort().reverse().forEach(y=>$('year').append(new Option(y,y)));
      [...new Set(entries.flatMap(e=>e.tags))].sort().forEach(t=>$('topic').append(new Option(t,t)));
      entries.filter(e=>!e.series && e.date).sort(newest).slice(0,3).forEach(e=>$('recent-list').append(card(e)));
      readFilters();render(false);
      $('filters').addEventListener('submit',e=>e.preventDefault());
      ['search','year','topic'].forEach(id=>$(id).addEventListener(id==='search'?'input':'change',()=>render()));
      $('clear').addEventListener('click',()=>{collection='';$('search').value='';$('year').value='';$('topic').value='';render();});
      window.addEventListener('popstate',()=>{readFilters();render(false);});
    } catch(error) { $('load-error').hidden=false; $('library-stats').textContent='Library unavailable'; console.error(error); }
  }
  init();
})();
