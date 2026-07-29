/**
 * Lazy mount for <model-viewer>.
 *
 * The rules this exists to enforce:
 *  - the 3D module never competes with the LCP image (IntersectionObserver,
 *    200 px root margin, and never on page load)
 *  - it never mounts at all where it cannot work (WebGL2 probe first)
 *  - a metered or slow connection is asked, not charged 2 MB silently
 *  - auto-rotation respects prefers-reduced-motion, live
 */

const VENDOR = '/vendor/model-viewer-4.3.1.min.js';

let loading: Promise<void> | null = null;

function hasWebGL2(): boolean {
  try {
    const canvas = document.createElement('canvas');
    return !!canvas.getContext('webgl2');
  } catch {
    return false;
  }
}

function isMetered(): boolean {
  const conn = (navigator as Navigator & {
    connection?: { saveData?: boolean; effectiveType?: string };
  }).connection;
  if (!conn) return false;
  return Boolean(conn.saveData) || ['slow-2g', '2g'].includes(conn.effectiveType ?? '');
}

function loadVendor(): Promise<void> {
  if (loading) return loading;
  loading = new Promise((resolve, reject) => {
    if (customElements.get('model-viewer')) return resolve();
    const script = document.createElement('script');
    script.type = 'module';
    script.src = VENDOR;
    script.onload = () => resolve();
    script.onerror = () => reject(new Error(`failed to load ${VENDOR}`));
    document.head.append(script);
  });
  return loading;
}

function mount(root: HTMLElement) {
  const src = root.dataset.src;
  const stage = root.querySelector<HTMLElement>('.mv__stage');
  const tpl = root.querySelector<HTMLTemplateElement>('[data-mv-template]');
  const progress = root.querySelector<HTMLElement>('[data-mv-progress]');
  const bar = root.querySelector<HTMLElement>('.mv__progress-rule span');
  const pct = root.querySelector<HTMLElement>('[data-mv-percent]');
  if (!src || !stage) return;

  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  const poster = root.querySelector<HTMLImageElement>('.mv__poster');

  const viewer = document.createElement('model-viewer') as HTMLElement & {
    resetTurntableRotation?: () => void;
    cameraOrbit?: string;
  };
  viewer.setAttribute('src', src);
  viewer.setAttribute('alt', poster?.alt ?? '');
  viewer.setAttribute('camera-controls', '');
  // Without pan-y the model swallows vertical swipes and the page cannot be
  // scrolled past it on a phone.
  viewer.setAttribute('touch-action', 'pan-y');
  viewer.setAttribute('disable-pan', '');
  viewer.setAttribute('environment-image', 'neutral');
  // The machines are painted near-black; the studio renders beside this viewer
  // read mid-grey only because the Cycles rig throws real light at them. The
  // `neutral` environment is much dimmer, so at exposure 1 the same machine
  // turns up as a silhouette and the 3D tab contradicts the photographs.
  viewer.setAttribute('exposure', '1.45');
  viewer.setAttribute('shadow-intensity', '1');
  viewer.setAttribute('shadow-softness', '0.8');
  viewer.setAttribute('camera-orbit', '35deg 75deg auto');
  viewer.setAttribute('field-of-view', '30deg');
  viewer.setAttribute('min-camera-orbit', 'auto 15deg auto');
  viewer.setAttribute('max-camera-orbit', 'auto 95deg auto');
  viewer.setAttribute('interaction-prompt', 'none');
  viewer.setAttribute('ar', '');
  viewer.setAttribute('ar-modes', 'webxr scene-viewer quick-look');
  viewer.setAttribute('ar-scale', 'fixed');

  const applyMotion = () => {
    if (reduce.matches) viewer.removeAttribute('auto-rotate');
    else viewer.setAttribute('auto-rotate', '');
  };
  applyMotion();
  reduce.addEventListener('change', applyMotion);

  if (tpl) viewer.append(tpl.content.cloneNode(true));

  progress?.removeAttribute('hidden');
  viewer.addEventListener('progress', (event) => {
    const detail = (event as CustomEvent<{ totalProgress: number }>).detail;
    const value = Math.round(detail.totalProgress * 100);
    if (bar) bar.style.width = `${value}%`;
    if (pct) pct.textContent = `%${value}`;
    if (detail.totalProgress >= 1) {
      progress?.setAttribute('hidden', '');
      root.dataset.mvReady = 'true';
    }
  });

  viewer.addEventListener('error', () => {
    // Leave the poster in place; a broken canvas is worse than a still image.
    progress?.setAttribute('hidden', '');
    viewer.remove();
    root.dataset.mvFailed = 'true';
  });

  stage.append(viewer);

  root.querySelector('[data-mv-reset]')?.addEventListener('click', () => {
    viewer.setAttribute('camera-orbit', '35deg 75deg auto');
    viewer.resetTurntableRotation?.();
  });

  root.querySelectorAll<HTMLButtonElement>('[data-mv-focus]').forEach((btn) => {
    btn.addEventListener('click', () => {
      const key = btn.dataset.mvFocus;
      const hotspot = viewer.querySelector<HTMLElement>(`[slot="hotspot-${key}"]`);
      viewer.querySelectorAll<HTMLElement>('[slot^="hotspot-"]').forEach((h) => {
        h.dataset.active = String(h === hotspot);
      });
    });
  });

  root.dataset.mvMounted = 'true';
}

export function mountModelViewers() {
  const roots = document.querySelectorAll<HTMLElement>('[data-model-viewer]');
  if (!roots.length) return;

  if (!hasWebGL2()) {
    // Never mount. The poster and the numbered hotspot list already carry the
    // information; a failed WebGL context would only replace them with a hole.
    roots.forEach((root) => { root.dataset.mvUnsupported = 'true'; });
    return;
  }

  const start = (root: HTMLElement) => {
    if (root.dataset.mvMounted) return;
    root.dataset.mvMounted = 'pending';
    loadVendor()
      .then(() => mount(root))
      .catch(() => { root.dataset.mvFailed = 'true'; });
  };

  roots.forEach((root) => {
    const prompt = root.querySelector<HTMLElement>('[data-mv-prompt]');
    const button = root.querySelector<HTMLButtonElement>('[data-mv-load]');

    if (isMetered()) {
      prompt?.removeAttribute('hidden');
      button?.addEventListener('click', () => {
        prompt?.setAttribute('hidden', '');
        start(root);
      }, { once: true });
      return;
    }

    if (!('IntersectionObserver' in window)) return start(root);

    const io = new IntersectionObserver((entries) => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        io.disconnect();
        start(entry.target as HTMLElement);
      }
    }, { rootMargin: '200px' });
    io.observe(root);
  });
}
