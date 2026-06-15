# Profile Floating Menu + Settings/Profile Popups + DE/EN i18n

- **Date:** 2026-06-15
- **Status:** Approved (design) — revised to build on the `app/` frontend
- **Area:** `src/frontend/dashboard` (dashboard microfrontend)
- **Branch:** `frontend-websocket-ready`

## Background

The dashboard header (`DashboardHeader.svelte`) renders the user avatar as a
static, non-interactive `<span>`, plus a standalone light/dark theme-toggle
button. Mockups (provided by the user) introduce a click-to-open floating menu
anchored to the avatar, a Settings popup, and a My Profile popup.

The sibling `app/` frontend **already has** a reusable dropdown menu (DaisyUI
`dropdown` via `<details>/<summary>`) with working **language change**, in
`app/src/components/basic/dropdown-menu/` and driven from
`app/src/components/app-frame/NavigationBar.svelte`. Per user direction we
**build on that** rather than reinventing: port its generic dropdown-menu
primitives and reuse its i18n catalogue shape.

A full profile edit page already exists at hash route `/profile`
(`ProfileEditPage.svelte`); the theme system already exists (`theme.ts`).

### Why port (copy) rather than cross-import

Each frontend (`admin`/`app`/`dashboard`) is an **independent esbuild bundle**
(`bin/frontend/build.js`, entry `<pkg>/src/index.ts`, output
`<pkg>/dist/...`, per-package `tsconfig.json` that only `include`s `./src`).
There is no shared package. A relative import into `../../app/src/...` would
bundle at build time but breaks package isolation and falls outside the
dashboard's tsconfig/lint roots. The dropdown-menu primitives are tiny and
generic (only `import type {Snippet} from "svelte"`), so copying them into the
dashboard is the clean, low-risk way to "build on" the existing solution.

## Goals

1. Clicking the header avatar opens a floating dropdown menu (built with the
   ported app primitives) matching the "profile menu" mockup.
2. Menu entries: profile header (avatar + name + email), **My Profile**,
   **Settings**, **Notification** (Allow/Mute submenu), **Log Out**.
3. **My Profile** opens a popup modal (per `MyProfilePopup` mockup), backed by
   the existing profile REST API.
4. **Settings** opens a popup modal (per `SettingsPopup` mockup) with a working
   **Theme** control and a working **Language** control; Language uses the same
   `language` store that drives the rest of the dashboard i18n.
5. Build DE/EN i18n for the dashboard (breadth **A**) using a lighter native
   Svelte store but the **same catalogue shape** as `app/` (`en.ts` master +
   `de.ts`).
6. Remove the standalone header theme-toggle button (theme now lives in
   Settings).

## Non-goals

- **i18n breadth B:** translating every existing dashboard page/panel body
  (Dashboard, Quiz, Content, CourseChat). Deferred; the infra here makes it an
  incremental follow-up.
- Porting the app's full i18n machinery (`utils/store.ts`
  `ReadableStore`/`WritableStore` + async dynamic catalogue import). We adopt
  the catalogue shape only; the store is a lighter native `derived`.
- Notification delivery backend — none exists. Allow/Mute is cosmetic local
  state only.
- Avatar cropping; changes to `theme.ts` internals or `ProfileEditPage.svelte`;
  the app's multi-theme `stores/theme.ts` (dashboard stays light/dark).

## Locked decisions

| Decision | Choice |
| --- | --- |
| Menu structure | **Hybrid**: app dropdown primitives + mockup's separate Settings/Profile popups |
| Dropdown primitives | **Ported** from `app/` into dashboard (copy, not cross-import) |
| My Profile target | New popup modal (not navigation to `/profile`) |
| Settings scope | Theme **and** Language functional; Notification = local placeholder |
| Standalone header theme-toggle | Removed |
| i18n breadth | A — new surfaces + header/footer chrome only |
| i18n store style | **Native Svelte `derived`** store, static catalogue import; app-shaped catalogues |
| Icons | Add `bootstrap-icons` to dashboard (match app `bi bi-*` + mockup line icons) |

## Architecture

### Ported components — `src/frontend/dashboard/src/components/basic/dropdown-menu/`

Copied verbatim (generic, only `Snippet` import) from `app/`:
`DropdownMenu.svelte`, `MenuItem.svelte`, `MenuTitle.svelte`, `SubMenu.svelte`.
They rely on DaisyUI `dropdown`/`menu` classes, which the dashboard already
uses (present in its Tailwind/DaisyUI setup). Behavior matches the app
(`<details>`-based). License header retained.

### New components — `src/frontend/dashboard/src/components/app-frame/`

**`ProfileMenu.svelte`** — composes the ported primitives into the avatar
dropdown. `DropdownMenu align="end"` triggered by the avatar; profile header
block (avatar + `fullName` + `email`); `MenuItem` rows:

- My Profile → `onOpenProfile`
- Settings → `onOpenSettings`
- Notification → `SubMenu` with Allow / Mute (`menuitemradio`), persisted to
  `localStorage` (`openbook-dashboard-notify`); cosmetic only.
- Log Out → `onLogout`

Icons via `bi bi-*` (person-circle, gear, bell, box-arrow-right, chevron-right)
to mirror NavigationBar.

**`SettingsModal.svelte`** — centered modal (uses `Modal.svelte`), per mockup.

- Theme control → `setTheme("light"|"dark")` (existing `theme` store).
- Language control → `$language = "en"|"de"`.
- Title/labels via `$i18n`; X closes.

**`ProfileModal.svelte`** — centered modal (uses `Modal.svelte`), per mockup.

- Loads current user (`fetchCurrentUser`); avatar + edit pencil (file input);
  editable **Name** (→ `firstName`); read-only **Email account** display.
- **Save Change** → `saveProfile(username, {firstName,lastName,description},
  pictureFile)`; `lastName`/`description` passed through from the loaded user so
  they aren't wiped. On success: refresh `dashboardStore`, close.
- Full email-change flow stays on `/profile`.

**`Modal.svelte`** — shared modal primitive: backdrop, centered card, X close,
`Escape` to close, focus-on-open, scroll-lock, body slot. Keeps both modals DRY.
(The dropdown primitives cover menus; modals are a separate concern not provided
by the app, hence this small base.)

### i18n — `src/frontend/dashboard/src/i18n/` + store

- **`i18n/index.ts`** — `languages=["en","de"]`, `defaultLanguage`/
  `fallbackLanguage="en"`, `export type I18N = typeof en` (mirrors app/index.ts).
- **`i18n/lang/en.ts`** — master catalogue (no type import).
- **`i18n/lang/de.ts`** — German; `import type {I18N}` for completeness checks.
- **`stores/i18n.store.ts`**
  - `language`: `writable<LanguageCode>` from
    `localStorage.getItem("openbook-dashboard-language") ?? defaultLanguage`;
    subscription persists changes (same UX as app's `language` store).
  - `i18n`: `derived(language, $lang => catalogs[$lang] ?? catalogs.en)` with
    both catalogues statically imported. No async dynamic import.
- Consumption: `$i18n.Menu.Profile`, `$language = "de"`, etc. — same call sites
  shape as the app.

Initial key tree (breadth A surfaces only):

```text
Menu:     { Profile, Settings, Notification, Logout, Allow, Mute }
Settings: { Title, Theme, ThemeLight, ThemeDark, Language }
Profile:  { Title, Name, Email, Save }
Header:   { StatusOnline }
Footer:   { Copyright }
```

### Modified components

**`DashboardHeader.svelte`** — replace static `avatar-mark` span with the
`ProfileMenu` (avatar is the dropdown trigger; `aria-haspopup`/`aria-expanded`
handled by the dropdown). Remove the `theme-toggle` button + styles. Chrome
text via `$i18n`. Emits `onOpenProfile`/`onOpenSettings`/`onLogout` upward.

**`DashboardApp.svelte`** — owns `profileOpen`/`settingsOpen` `$state`; passes
handlers down to the header; renders `SettingsModal` + `ProfileModal` at shell
root (above header `z-index: 50`).

**`data/dashboard.ts`** — add `email: string | null` to `DashboardUser`;
`mapUser`: `email: user.email ?? null` (DTO already exposes `email?`).

**`index.ts`** — import `bootstrap-icons/font/bootstrap-icons.min.css`; ensure
persisted language applied at startup (store self-initializes from localStorage
on import; add explicit init only if needed).

**`package.json` (dashboard)** — add `bootstrap-icons` devDependency (app uses
`^1.13.1`).

## Data flow

```text
avatar (DropdownMenu trigger) -> ProfileMenu row click
  -> emits onOpenProfile / onOpenSettings / onLogout
     -> DashboardApp sets profileOpen / settingsOpen, or runs logout
        -> SettingsModal / ProfileModal render at shell root
```

Theme: SettingsModal -> setTheme() -> theme store -> data-theme.
Language: SettingsModal (or future menu) -> `$language` -> i18n derived store ->
all `$i18n` consumers re-render. Both persisted to localStorage.

## Accessibility

- Dropdown: app primitives provide `role="menu"`/`menuitem(radio)`; keyboard
  arrow-nav is a known app TODO (not in scope to fix here).
- Avatar trigger labelled; modals `role="dialog"` `aria-modal="true"` labelled
  by title; `Escape` closes; focus moves into the dialog on open.

## Logout

Dashboard is a separate bundle; Log Out navigates the browser to the allauth
logout endpoint (`window.location.href = "/accounts/logout/"`). The app links
`#/accounts/logout` inside its own SPA. **Impl-time check:** confirm exact URL
and GET-confirmation vs POST; switch to a form-POST if allauth rejects GET.

## Testing

- Dashboard build + `tsc` pass (`cd src/frontend/dashboard && npm run build`,
  `npm run check`).
- Manual (Playwright/browser): avatar opens menu; My Profile saves a name
  change reflected in the header; Settings toggles theme (data-theme flips) and
  language (chrome + menu/modals switch DE/EN); Notification Allow/Mute persists
  across reload; Log Out navigates to the logout endpoint.

## File change summary

Ported (copied from `app/`):

- `components/basic/dropdown-menu/DropdownMenu.svelte`
- `components/basic/dropdown-menu/MenuItem.svelte`
- `components/basic/dropdown-menu/MenuTitle.svelte`
- `components/basic/dropdown-menu/SubMenu.svelte`

New:

- `components/app-frame/ProfileMenu.svelte`
- `components/app-frame/SettingsModal.svelte`
- `components/app-frame/ProfileModal.svelte`
- `components/app-frame/Modal.svelte`
- `i18n/index.ts`, `i18n/lang/en.ts`, `i18n/lang/de.ts`
- `stores/i18n.store.ts`

Modified:

- `components/app-frame/DashboardHeader.svelte`
- `components/DashboardApp.svelte`
- `data/dashboard.ts`
- `index.ts`
- `package.json` (add `bootstrap-icons`)

## Open items (resolve during implementation)

1. Exact allauth logout URL/method (GET vs POST).
2. Whether `index.ts` needs an explicit i18n init call or the store
   self-initializes from localStorage on import.
3. Confirm DaisyUI `dropdown`/`menu` classes render correctly in the dashboard
   build (they should — DaisyUI is already active there).
