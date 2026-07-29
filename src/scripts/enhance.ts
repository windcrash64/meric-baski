/**
 * Progressive enhancement.
 *
 * Everything here is bound to `astro:page-load`, never `DOMContentLoaded`.
 * With <ClientRouter /> the document is swapped rather than reloaded, so
 * anything wired on DOMContentLoaded works exactly once and then silently dies
 * on the second navigation — which looks like a random intermittent bug.
 *
 * Every feature also degrades: nothing here is required for the page to work.
 */

type Cleanup = () => void;
let cleanups: Cleanup[] = [];

const reduced = () => matchMedia('(prefers-reduced-motion: reduce)').matches;

/* -------------------------------------------------------------------------
   Scroll reveals. The markup is authored in its FINAL state; JS arms the
   hidden state only once it is certain it can also un-arm it. That way a
   script error or a blocked bundle leaves the content visible instead of a
   blank page — the standard failure mode of reveal-on-scroll sites.
   ------------------------------------------------------------------------- */
function reveals(): Cleanup {
  const targets = document.querySelectorAll<HTMLElement>('.reveal, .reveal-media, .stagger-line');
  if (!targets.length || !('IntersectionObserver' in window)) return () => {};

  document.documentElement.setAttribute('data-reveal-armed', '');

  if (reduced()) {
    targets.forEach((el) => el.classList.add('is-visible'));
    return () => document.documentElement.removeAttribute('data-reveal-armed');
  }

  const io = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        entry.target.classList.add('is-visible');
        io.unobserve(entry.target); // reveal once, then stop paying for it
      }
    },
    { rootMargin: '0px 0px -12% 0px', threshold: 0.01 },
  );

  targets.forEach((el) => {
    if (el.style.getPropertyValue('--reveal-delay') === '') {
      const group = el.closest('[data-stagger]');
      if (group) {
        const index = [...group.querySelectorAll('.reveal')].indexOf(el);
        if (index > 0) el.style.setProperty('--reveal-delay', `${index * 70}ms`);
      }
    }
    // Stagger index is per heading, not per page: a global counter would give
    // the last line on the page a 1.3 s delay.
    const lines = el.parentElement?.querySelectorAll(':scope > .stagger-line');
    if (lines?.length) el.style.setProperty('--line-index', String([...lines].indexOf(el)));
    io.observe(el);
  });

  // Safety net. If an observer never fires — an element inside a collapsed
  // container, a browser quirk, a mis-set rootMargin — the content would stay
  // invisible forever. Content is not allowed to depend on an animation
  // succeeding, so anything still hidden after 3 s is simply shown.
  const failsafe = setTimeout(() => {
    targets.forEach((el) => el.classList.add('is-visible'));
  }, 3000);

  return () => {
    clearTimeout(failsafe);
    io.disconnect();
    document.documentElement.removeAttribute('data-reveal-armed');
  };
}

/* -------------------------------------------------------------------------
   Sticky header: condense past a sentinel, hide on scroll down, show on up.
   Driven by IntersectionObserver + a single rAF-throttled scroll read, never
   by layout queries inside a scroll handler.
   ------------------------------------------------------------------------- */
function header(): Cleanup {
  const el = document.querySelector<HTMLElement>('.site-header');
  const sentinel = document.querySelector('[data-header-sentinel]');
  if (!el) return () => {};

  const disposers: Cleanup[] = [];

  if (sentinel && 'IntersectionObserver' in window) {
    const io = new IntersectionObserver(
      ([entry]) => el.setAttribute('data-condensed', String(!entry.isIntersecting)),
      { rootMargin: '-120px 0px 0px 0px' },
    );
    io.observe(sentinel);
    disposers.push(() => io.disconnect());
  }

  let last = window.scrollY;
  let ticking = false;
  const onScroll = () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      const y = window.scrollY;
      const menuOpen = document.documentElement.dataset.navOpen === 'true';
      const goingDown = y > last && y > 240;
      el.setAttribute('data-hidden', String(goingDown && !menuOpen));
      last = y;
      ticking = false;
    });
  };
  addEventListener('scroll', onScroll, { passive: true });
  disposers.push(() => removeEventListener('scroll', onScroll));

  return () => disposers.forEach((d) => d());
}

/* ------------------------------------------------------------------------- */
function mobileNav(): Cleanup {
  const toggle = document.querySelector<HTMLButtonElement>('[data-nav-toggle]');
  const panel = document.getElementById('mobile-nav');
  if (!toggle || !panel) return () => {};

  const setOpen = (open: boolean) => {
    toggle.setAttribute('aria-expanded', String(open));
    document.documentElement.dataset.navOpen = String(open);
    document.body.style.overflow = open ? 'hidden' : '';
    if (open) {
      panel.hidden = false;
      requestAnimationFrame(() => panel.setAttribute('data-open', 'true'));
    } else {
      panel.setAttribute('data-open', 'false');
      // Wait out the clip-path transition before removing it from the a11y tree.
      setTimeout(() => {
        if (panel.getAttribute('data-open') === 'false') panel.hidden = true;
      }, 400);
    }
  };

  const onClick = () => setOpen(toggle.getAttribute('aria-expanded') !== 'true');
  const onKey = (e: KeyboardEvent) => {
    if (e.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
      setOpen(false);
      toggle.focus();
    }
  };

  toggle.addEventListener('click', onClick);
  addEventListener('keydown', onKey);
  panel.hidden = true;

  return () => {
    toggle.removeEventListener('click', onClick);
    removeEventListener('keydown', onKey);
    document.body.style.overflow = '';
    delete document.documentElement.dataset.navOpen;
  };
}

/* -------------------------------------------------------------------------
   Number count-up. Formatted through Intl so Turkish gets 1.440, not 1,440.
   ------------------------------------------------------------------------- */
function counters(): Cleanup {
  const els = document.querySelectorAll<HTMLElement>('[data-count-to]');
  if (!els.length) return () => {};

  const locale = document.documentElement.lang === 'tr' ? 'tr-TR' : 'en-GB';
  const write = (el: HTMLElement, value: number) => {
    const decimals = Number(el.dataset.countDecimals ?? 0);
    el.textContent = new Intl.NumberFormat(locale, {
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals,
    }).format(value);
  };

  if (reduced() || !('IntersectionObserver' in window)) {
    els.forEach((el) => write(el, Number(el.dataset.countTo)));
    return () => {};
  }

  const io = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      const el = entry.target as HTMLElement;
      io.unobserve(el);
      const target = Number(el.dataset.countTo);
      const started = performance.now();
      const step = (now: number) => {
        const t = Math.min(1, (now - started) / 1400);
        write(el, target * (1 - (1 - t) ** 3));
        if (t < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    }
  }, { threshold: 0.4 });

  els.forEach((el) => {
    write(el, 0);
    io.observe(el);
  });
  return () => io.disconnect();
}

/* -------------------------------------------------------------------------
   Gallery. The rail is a CSS scroll-snap strip that already works with no JS
   at all; this adds the arrows, the dot tabs and the live position label.
   ------------------------------------------------------------------------- */
function galleries(): Cleanup {
  const disposers: Cleanup[] = [];

  document.querySelectorAll<HTMLElement>('[data-gallery]').forEach((root) => {
    const rail = root.querySelector<HTMLElement>('[data-gallery-rail]');
    if (!rail) return;

    const slides = [...rail.children] as HTMLElement[];
    const prev = root.querySelector<HTMLButtonElement>('[data-gallery-prev]');
    const next = root.querySelector<HTMLButtonElement>('[data-gallery-next]');
    const dots = [...root.querySelectorAll<HTMLButtonElement>('[data-gallery-dot]')];
    const status = root.querySelector<HTMLElement>('[data-gallery-status]');

    root.querySelectorAll<HTMLElement>('[data-gallery-controls]')
      .forEach((c) => c.removeAttribute('hidden'));

    const scrollTo = (index: number) => {
      const clamped = Math.max(0, Math.min(slides.length - 1, index));
      rail.scrollTo({
        left: slides[clamped].offsetLeft - rail.offsetLeft,
        behavior: reduced() ? 'auto' : 'smooth',
      });
    };

    const current = () => {
      const mid = rail.scrollLeft + rail.clientWidth / 2;
      let best = 0;
      let bestDist = Infinity;
      slides.forEach((s, i) => {
        const d = Math.abs(s.offsetLeft - rail.offsetLeft + s.clientWidth / 2 - mid);
        if (d < bestDist) { bestDist = d; best = i; }
      });
      return best;
    };

    const sync = () => {
      const i = current();
      dots.forEach((d, di) => d.setAttribute('aria-selected', String(di === i)));
      if (status) status.textContent = `${i + 1} / ${slides.length}`;
      if (prev) prev.disabled = i === 0;
      if (next) next.disabled = i === slides.length - 1;
    };

    const onPrev = () => scrollTo(current() - 1);
    const onNext = () => scrollTo(current() + 1);
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'ArrowLeft') { e.preventDefault(); onPrev(); }
      if (e.key === 'ArrowRight') { e.preventDefault(); onNext(); }
    };

    prev?.addEventListener('click', onPrev);
    next?.addEventListener('click', onNext);
    rail.addEventListener('scroll', sync, { passive: true });
    rail.addEventListener('keydown', onKey);
    dots.forEach((d, i) => d.addEventListener('click', () => scrollTo(i)));
    sync();

    disposers.push(() => {
      prev?.removeEventListener('click', onPrev);
      next?.removeEventListener('click', onNext);
      rail.removeEventListener('scroll', sync);
      rail.removeEventListener('keydown', onKey);
    });
  });

  return () => disposers.forEach((d) => d());
}

/* -------------------------------------------------------------------------
   Rail navigation.

   A snapped rail is swipeable, but a swipe is invisible: nothing on the page
   says the row continues. The buttons make it explicit, and they are the only
   way to move it with a keyboard or a trackpad that does not scroll sideways.
   They are hidden whenever the rail is not actually scrollable, so the same
   markup can serve a phone rail and a desktop grid.
   ------------------------------------------------------------------------- */
function rails(): Cleanup {
  const disposers: Cleanup[] = [];

  document.querySelectorAll<HTMLElement>('[data-rail-group]').forEach((group) => {
    const rail = group.querySelector<HTMLElement>('[data-rail]');
    const nav = group.querySelector<HTMLElement>('[data-rail-nav]');
    const prev = group.querySelector<HTMLButtonElement>('[data-rail-prev]');
    const next = group.querySelector<HTMLButtonElement>('[data-rail-next]');
    if (!rail || !nav || !prev || !next) return;

    const step = () => {
      const first = rail.firstElementChild as HTMLElement | null;
      if (!first) return rail.clientWidth * 0.8;
      const gap = parseFloat(getComputedStyle(rail).columnGap || '0') || 0;
      return first.getBoundingClientRect().width + gap;
    };

    const sync = () => {
      const scrollable = rail.scrollWidth > rail.clientWidth + 4;
      nav.hidden = !scrollable;
      if (!scrollable) return;
      prev.disabled = rail.scrollLeft <= 2;
      next.disabled = rail.scrollLeft + rail.clientWidth >= rail.scrollWidth - 2;
    };

    const go = (dir: number) => rail.scrollBy({
      left: step() * dir,
      behavior: reduced() ? 'auto' : 'smooth',
    });

    const onPrev = () => go(-1);
    const onNext = () => go(1);

    prev.addEventListener('click', onPrev);
    next.addEventListener('click', onNext);
    rail.addEventListener('scroll', sync, { passive: true });

    const ro = 'ResizeObserver' in window ? new ResizeObserver(sync) : null;
    ro?.observe(rail);
    sync();

    disposers.push(() => {
      prev.removeEventListener('click', onPrev);
      next.removeEventListener('click', onNext);
      rail.removeEventListener('scroll', sync);
      ro?.disconnect();
    });
  });

  return () => disposers.forEach((d) => d());
}

/* -------------------------------------------------------------------------
   Hero slider.

   Autoplays because the design calls for a rotating hero, which makes the
   visible pause control mandatory rather than optional (WCAG 2.2.2). It also
   stops on hover, on keyboard focus inside the hero, when the tab is hidden,
   and permanently the moment the user touches any control — once someone has
   taken over, moving the content under them is hostile.
   ------------------------------------------------------------------------- */
function heroSlider(): Cleanup {
  const hero = document.querySelector<HTMLElement>('[data-hero]');
  const root = hero;
  if (!root || !hero) return () => {};

  const slides = [...root.querySelectorAll<HTMLElement>('[data-hero-slide]')];
  const frames = [...hero.querySelectorAll<HTMLElement>('[data-hero-frame]')];
  const dots = [...hero.querySelectorAll<HTMLButtonElement>('[data-hero-dot]')];
  const count = hero.querySelector<HTMLElement>('[data-hero-count]');
  const pause = hero.querySelector<HTMLButtonElement>('[data-hero-pause]');
  const pauseIcon = hero.querySelector<HTMLElement>('[data-hero-pause-icon]');
  const pauseLabel = hero.querySelector<HTMLElement>('[data-hero-pause-label]');
  if (slides.length < 2) return () => {};

  const INTERVAL = 6500;
  let index = 0;
  let timer: number | undefined;
  let stopped = reduced();

  const show = (next: number) => {
    index = (next + slides.length) % slides.length;
    slides.forEach((el, i) => {
      const on = i === index;
      el.dataset.active = String(on);
      el.toggleAttribute('inert', !on);
      if (on) el.removeAttribute('aria-hidden');
      else el.setAttribute('aria-hidden', 'true');
    });
    frames.forEach((el, i) => { el.dataset.active = String(i === index); });
    dots.forEach((d, i) => d.setAttribute('aria-selected', String(i === index)));
    if (count) {
      count.textContent =
        `${String(index + 1).padStart(2, '0')} / ${String(slides.length).padStart(2, '0')}`;
    }
  };

  const stop = () => {
    window.clearInterval(timer);
    timer = undefined;
  };

  const start = () => {
    stop();
    if (stopped) return;
    timer = window.setInterval(() => show(index + 1), INTERVAL);
  };

  const setPaused = (value: boolean) => {
    stopped = value;
    pause?.setAttribute('aria-pressed', String(value));
    // CSS reads this to freeze the meter's fill.
    hero.setAttribute('data-hero-paused', String(value));
    if (pauseIcon) pauseIcon.textContent = value ? 'play' : 'pause';
    if (pauseLabel) {
      pauseLabel.textContent = value
        ? (document.documentElement.lang === 'tr' ? 'Oynat' : 'Play')
        : (document.documentElement.lang === 'tr' ? 'Duraklat' : 'Pause');
    }
    if (value) stop();
    else start();
  };

  const onPause = () => setPaused(!stopped);
  const onPrev = () => { setPaused(true); show(index - 1); };
  const onNext = () => { setPaused(true); show(index + 1); };
  const onEnter = () => stop();
  const onLeave = () => { if (!stopped) start(); };
  const onVisibility = () => (document.hidden ? stop() : onLeave());
  const onMotion = (e: MediaQueryListEvent) => setPaused(e.matches);

  pause?.addEventListener('click', onPause);
  hero.querySelector('[data-hero-prev]')?.addEventListener('click', onPrev);
  hero.querySelector('[data-hero-next]')?.addEventListener('click', onNext);
  dots.forEach((d, i) => d.addEventListener('click', () => { setPaused(true); show(i); }));
  hero.addEventListener('mouseenter', onEnter);
  hero.addEventListener('mouseleave', onLeave);
  hero.addEventListener('focusin', onEnter);
  hero.addEventListener('focusout', onLeave);
  document.addEventListener('visibilitychange', onVisibility);

  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  motion.addEventListener('change', onMotion);

  show(0);
  setPaused(stopped);

  return () => {
    stop();
    pause?.removeEventListener('click', onPause);
    hero.removeEventListener('mouseenter', onEnter);
    hero.removeEventListener('mouseleave', onLeave);
    hero.removeEventListener('focusin', onEnter);
    hero.removeEventListener('focusout', onLeave);
    document.removeEventListener('visibilitychange', onVisibility);
    motion.removeEventListener('change', onMotion);
  };
}

/* -------------------------------------------------------------------------
   Marquee pause. Ships regardless of prefers-reduced-motion: WCAG 2.2.2 wants
   a control the user can actually see and press.
   ------------------------------------------------------------------------- */
function marquees(): Cleanup {
  const disposers: Cleanup[] = [];
  document.querySelectorAll<HTMLElement>('.marquee').forEach((el) => {
    const btn = el.querySelector<HTMLButtonElement>('[data-marquee-toggle]');
    if (!btn) return;
    const onClick = () => {
      const paused = el.getAttribute('data-paused') === 'true';
      el.setAttribute('data-paused', String(!paused));
      btn.setAttribute('aria-pressed', String(!paused));
    };
    btn.addEventListener('click', onClick);
    disposers.push(() => btn.removeEventListener('click', onClick));
  });
  return () => disposers.forEach((d) => d());
}

/* ------------------------------------------------------------------------- */
function boot() {
  cleanups.forEach((c) => c());
  cleanups = [
    reveals(), header(), mobileNav(), counters(),
    galleries(), marquees(), heroSlider(), rails(),
  ];
}

document.addEventListener('astro:page-load', boot);
// Tear down before the swap so observers on the outgoing document are released.
document.addEventListener('astro:before-swap', () => {
  cleanups.forEach((c) => c());
  cleanups = [];
});
