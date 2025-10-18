PWA integration notes

Files added:
- assets/manifest.json  — minimal Web App Manifest
- assets/sw.js         — minimal service worker (caches '/', manifest)
- assets/register-sw.js — small script that registers the service worker on load

How to test locally

1) Start the Reflex app locally (make sure you have reflex installed):

```bash
# from project root
pip install -r requirements.txt
reflex run
```

2) Open the app in Chrome (or Chromium-based) at the address shown by `reflex run`.

3) Register the service worker manually (if the small injector script was not included):

Open the browser DevTools Console and paste:

```javascript
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/assets/sw.js')
    .then(reg => console.log('SW registered', reg.scope))
    .catch(err => console.warn('SW reg failed', err));
}
```

4) Check PWA installability and service worker:
- In Chrome DevTools go to Application > Service Workers to view registration.
- In Application > Manifest you should see the manifest details and icons.
- To install (on desktop) look for the install icon in the address bar or Application > Manifest > 'Add to home screen'.

Notes & limitations
- I added the PWA assets to `assets/` so Reflex serves them statically. Reflex versions differ in how to inject links into the HTML head — I avoided modifying Reflex internals to keep the change low risk.
- If you want automatic registration on page load, insert the contents of `assets/register-sw.js` as a small script tag in your HTML template or use Reflex's client-side script injection API if your Reflex version supports it.

Security and cache
- The provided `sw.js` caches only a couple of items and uses a simple cache-first strategy. Adjust for your production needs.

If you want, I can:
- Attempt a version-specific `rx.head` injection to add the manifest link automatically (tell me your Reflex version), or
- Add icons into `assets/icons/` and wire those in the manifest (I included paths but not actual image files).