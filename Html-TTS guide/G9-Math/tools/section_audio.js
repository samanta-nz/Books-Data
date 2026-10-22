/* Per-section offline audio. Source bytes are embedded only by the assembly tool. */
(function () {
  'use strict';
  function init() {
    const main = document.querySelector('main');
    const manifestNode = document.getElementById('hamyar-section-audio-manifest');
    if (!main || !manifestNode) return;
    let manifest;
    try { manifest = JSON.parse(manifestNode.textContent); } catch (_) { return; }
    const storageKey = 'hamyar.section-audio.v1:' + manifest.lesson;
    const sections = [...main.querySelectorAll('section[data-section-audio]')];
    let state = { version: 1, activeSection: null, tracks: {} }, persistent = true;
    try {
      const old = JSON.parse(localStorage.getItem(storageKey) || 'null');
      if (old && old.version === 1 && old.tracks && typeof old.tracks === 'object') state = old;
    } catch (_) { persistent = false; }
    const records = new Map();
    const fa = s => String(s).replace(/[0-9]/g, n => '۰۱۲۳۴۵۶۷۸۹'[Number(n)]);
    const time = value => {
      const n = Math.max(0, Math.floor(Number(value) || 0));
      return fa(Math.floor(n / 60)) + ':' + fa(String(n % 60).padStart(2, '0'));
    };
    function persist() { try { localStorage.setItem(storageKey, JSON.stringify(state)); } catch (_) { persistent = false; } }
    function save(record, force) {
      const now = Date.now();
      if (!force && now - record.lastSaved < 900) return;
      const a = record.audio;
      if (!record.ready || a.readyState === 0 || !Number.isFinite(a.currentTime)) return;
      state.tracks[record.id] = { time: a.currentTime, completed: a.ended, asset: a.dataset.audioSha256 || '', updatedAt: now };
      record.lastSaved = now; persist();
    }
    function update(record) {
      const a = record.audio, duration = Number.isFinite(a.duration) ? a.duration : 0;
      record.play.textContent = a.paused ? '▶ پخش' : 'Ⅱ مکث';
      record.play.setAttribute('aria-label', (a.paused ? 'پخش صدای بخش: ' : 'مکث صدای بخش: ') + record.title);
      record.play.setAttribute('aria-pressed', String(!a.paused));
      const saved = state.tracks[record.id];
      const current = !record.restored && saved && !saved.completed ? saved.time : a.currentTime;
      record.position.textContent = time(current) + ' / ' + (duration ? time(duration) : '—');
      record.seek.max = String(duration);
      if (!record.seeking) record.seek.value = String(a.currentTime || 0);
      record.seek.disabled = !record.ready || !duration;
      record.seek.setAttribute('aria-valuetext', time(a.currentTime) + ' از ' + time(duration));
    }
    function pauseOthers(except) { records.forEach(r => { if (r !== except && !r.audio.paused) { r.audio.pause(); save(r, true); } }); }
    function openSection(id, scroll) {
      const target = records.get(id); if (!target) return false;
      sections.forEach(s => {
        const d = s.querySelector(':scope > details.lesson-accordion');
        if (d && s.id !== id) d.open = false;
      });
      target.details.open = true;
      state.activeSection = id; persist(); pauseOthers(target);
      requestAnimationFrame(() => {
        window.dispatchEvent(new Event('resize'));
        if (scroll) target.section.scrollIntoView({ block: 'start', behavior: 'auto' });
      });
      return true;
    }
    sections.forEach(section => {
      const box = section.querySelector('.section-audio-player');
      const details = section.querySelector(':scope > details.lesson-accordion');
      if (!box || !details) return;
      const audio = box.querySelector('audio');
      const record = { id: section.id, title: box.dataset.audioTitle, section, details, audio,
        play: box.querySelector('[data-audio-play]'), stop: box.querySelector('[data-audio-stop]'), restart: box.querySelector('[data-audio-restart]'),
        seek: box.querySelector('[data-audio-seek]'), position: box.querySelector('[data-audio-time]'),
        status: box.querySelector('[data-audio-status-text]'), ready: /^data:audio\//.test(audio.getAttribute('src') || ''),
        seeking: false, lastSaved: 0, restored: false };
      records.set(record.id, record);
      record.play.disabled = record.stop.disabled = record.restart.disabled = !record.ready;
      const previous = state.tracks[record.id];
      if (record.ready) {
        record.status.textContent = previous && previous.time > 0 ? 'با پخش، از جای ذخیره‌شده ادامه می‌دهید.' : 'برای شنیدن این بخش، پخش را بزنید.';
      }
      audio.addEventListener('loadedmetadata', () => {
        if (!record.restored) {
          record.restored = true;
          const saved = state.tracks[record.id];
          if (saved && !saved.completed && (!saved.asset || saved.asset === (audio.dataset.audioSha256 || '')) && Number.isFinite(saved.time) && audio.duration > 0) {
            audio.currentTime = Math.max(0, Math.min(saved.time, Math.max(0, audio.duration - 0.05)));
          }
        }
        update(record);
      });
      record.play.addEventListener('click', () => {
        if (!record.ready) return;
        if (!audio.paused) { audio.pause(); return; }
        openSection(record.id, false); pauseOthers(record);
        if (audio.ended) audio.currentTime = 0;
        const result = audio.play();
        if (result && result.catch) result.catch(() => { record.status.textContent = 'پخش صدا انجام نشد؛ دوباره پخش را بزنید.'; update(record); });
      });
      record.stop.addEventListener('click', () => {
        audio.pause(); save(record, true);
        record.status.textContent = 'پخش متوقف شد؛ با پخش، از همین‌جا ادامه می‌دهید.'; update(record);
      });
      record.restart.addEventListener('click', () => {
        audio.pause(); record.restored = true;
        if (audio.readyState > 0) audio.currentTime = 0;
        state.tracks[record.id] = { time: 0, completed: false, asset: audio.dataset.audioSha256 || '', updatedAt: Date.now() };
        persist(); record.status.textContent = 'پخش متوقف شد؛ شروع بعدی از ابتدای همین بخش است.'; update(record);
      });
      record.seek.addEventListener('input', () => {
        record.seeking = true;
        if (Number.isFinite(audio.duration)) audio.currentTime = Math.max(0, Math.min(Number(record.seek.value), audio.duration));
        record.seeking = false; update(record); save(record, true);
      });
      audio.addEventListener('play', () => { pauseOthers(record); record.status.textContent = persistent ? 'در حال پخش؛ جای پخش شما ذخیره می‌شود.' : 'جای پخش تا بسته‌شدن صفحه حفظ می‌شود.'; update(record); });
      audio.addEventListener('pause', () => { save(record, true); update(record); });
      audio.addEventListener('timeupdate', () => { update(record); save(record, false); });
      audio.addEventListener('seeked', () => { update(record); save(record, true); });
      audio.addEventListener('durationchange', () => update(record));
      audio.addEventListener('ended', () => { save(record, true); record.status.textContent = 'صدای این بخش تمام شد؛ می‌توانید دوباره پخش کنید.'; update(record); });
      audio.addEventListener('error', () => { record.status.textContent = 'صدای این بخش قابل پخش نیست.'; update(record); });
      details.addEventListener('toggle', () => {
        if (details.open) {
          state.activeSection = record.id; persist(); pauseOthers(record);
          sections.forEach(s => { const other = s.querySelector(':scope > details.lesson-accordion'); if (other && other !== details) other.open = false; });
          section.dispatchEvent(new CustomEvent('hamyar-section-open', { bubbles: true, detail: { sectionId: record.id } }));
          requestAnimationFrame(() => window.dispatchEvent(new Event('resize')));
        } else { audio.pause(); save(record, true); }
      });
      update(record);
    });
    function revealTarget(hash, scroll) {
      if (!hash || hash === '#') return false;
      let id; try { id = decodeURIComponent(hash.slice(1)); } catch (_) { return false; }
      const target = document.getElementById(id); if (!target) return false;
      const section = target.closest('section[data-section-audio]'); if (!section) return false;
      openSection(section.id, false);
      // A fragment may point inside an answer or another nested disclosure.
      for (let p = target.parentElement; p && p !== section; p = p.parentElement) if (p.tagName === 'DETAILS') p.open = true;
      if (scroll) requestAnimationFrame(() => target.scrollIntoView({ block: 'start', behavior: 'auto' }));
      return true;
    }
    document.addEventListener('click', event => {
      const a = event.target.closest && event.target.closest('a[href^="#"]');
      if (a) revealTarget(a.getAttribute('href'), true);
    }, true);
    window.addEventListener('hashchange', () => revealTarget(location.hash, true));
    const first = sections[0] && sections[0].id;
    if (!revealTarget(location.hash, true)) openSection(records.has(state.activeSection) ? state.activeSection : first, false);
    window.addEventListener('pagehide', () => { records.forEach(r => { save(r, true); r.audio.pause(); }); });
    document.addEventListener('visibilitychange', () => { if (document.hidden) records.forEach(r => save(r, true)); });
    window.HamyarSectionAudio = Object.freeze({ openSection, saveAll: () => records.forEach(r => save(r, true)), manifest: () => manifest });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true }); else init();
})();
