# Admin Bundle Loader Fix

## Problem
On the admin page, browser runtime errors appeared like:

- `Uncaught TypeError: Cannot read properties of undefined (reading 'call')`
- stack traces referenced `emittermixin.ts`, `app.js`, `simplebar.js`, and `alpine.js`

Root cause: `openbook/admin/bundle.js` is an ES module bundle but was loaded as a classic script in Django Unfold (`UNFOLD["SCRIPTS"]`).
When loaded as a classic script, top-level function names from the bundle leaked into global scope and conflicted with browser globals.

## Plan
1. Add a classic-script loader file for admin static assets.
2. Load `bundle.js` via dynamic `import()` from that loader.
3. Update Unfold config to include the loader instead of `bundle.js` directly.
4. Keep the loader in source and dist so it works immediately and remains reproducible after rebuilds.

## Progress
- [x] Added `src/frontend/admin/static/loader.js`
- [x] Added `src/frontend/admin/dist/openbook/admin/loader.js`
- [x] Updated `src/openbook/settings.py` to load `openbook/admin/loader.js`

## How It Works
`loader.js` is executed as a classic script by Unfold and then loads the admin bundle as an ES module:

```js
import("./bundle.js").catch((error) => {
    console.error("Failed to load OpenBook admin bundle", error);
});
```

This keeps bundle internals in module scope and prevents accidental global shadowing.
