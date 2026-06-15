# Profile Floating Menu + Settings/Profile Popups + DE/EN i18n

- **Date:** 2026-06-15
- **Status:** Approved (design)
- **Area:** `src/frontend/dashboard` (dashboard microfrontend)
- **Branch:** `frontend-websocket-ready`

## Background

The dashboard header (`DashboardHeader.svelte`) renders the user avatar as a
static, non-interactive `<span>`, plus a standalone light/dark theme-toggle
button. Mockups (provided by the user) introduce a click-to-open floating menu
anchored to the avatar, a Settings popup, and a My Profile popup.

A full profile edit page already exists at hash route `/profile`
(`ProfileEditPage.svelte`) and a theme system already exists (`theme.ts`). The
dashboard has **no** i18n; the sibling `app/` frontend does (custom async
stores + `en.ts`/`de.ts` catalogs), which we mirror in shape only.

## Goals

1. Clicking the header avatar opens a floating dropdown menu matching the
   "profile menu" mockup.
2. Menu entries: profile header (avatar + name + email), **My Profile**,
   **Settings**, **Notification** (Allow + Allow/Mute flyout), **Log Out**.
3. **My Profile** opens a popup modal (per `MyProfilePopup` mockup) — avatar
   with edit pencil, Name field, Email account display, Save Change — backed by
   the existing profile REST API.
4. **Settings** opens a popup modal (per `SettingsPopup` mockup) with a working
   **Theme** control and a working **Language** control.
5. Build DE/EN i18n infrastructure for the dashboard and apply it to the new
   surfaces + visible header/footer chrome (breadth **A**, see Non-goals).
6. Remove the standalone header theme-toggle button (theme now lives in
   Settings).

## Non-goals

- **i18n breadth B:** translating every existing dashboard page/panel body
  (Dashboard, Quiz, Content, CourseChat). Deferred; the infra built here makes
  it an incremental follow-up.
- Notification delivery backend — there is none. Allow/Mute is a cosmetic local
  placeholder only.
- Avatar image cropping/resizing.
- Changes to `theme.ts` internals or to `ProfileEditPage.svelte`.

## Locked decisions

| Decision | Choice |
|---|---|
| My Profile target | New popup modal (not navigation to `/profile`) |
| Settings scope | Theme **and** Language functional; Notification = local placeholder |
| Standalone header theme-toggle | Removed |
| i18n breadth | A — new surfaces + header/footer chrome only |
| i18n store style | Native Svelte `derived` store, static catalog import |

## Architecture

### New components — `src/frontend/dashboard/src/components/app-frame/`

**`ProfileMenu.svelte`** — floating dropdown anchored beneath the avatar.
- Props: `user: DashboardUser | null`, `open: boolean`.
- Emits (callback props): `onClose`, `onOpenProfile`, `onOpenSettings`,
  `onLogout`.
- Contents: header block (avatar + `fullName` + `email`), rows for My Profile
  (chevron), Settings (chevron), Notification (label + Allow/Mute flyout),
  Log Out.
- Behavior: closes on outside-click, on `Escape`, and after any row action.
  Initial focus moves into the menu; focus returns to the avatar on close.
- Notification flyout state (`allow` | `mute`) persisted to `localStorage`
  (key `openbook-dashboard-notify`); cosmetic only — commented as such.

**`SettingsModal.svelte`** — centered modal (uses `Modal.svelte`).
- Theme control bound to `theme` store → `setTheme("light"|"dark")`.
- Language control bound to `language` store (English / Deutsch).
- Title + labels via `$i18n`. X button closes.

**`ProfileModal.svelte`** — centered modal (uses `Modal.svelte`), per mockup.
- Loads current user (reuse `fetchCurrentUser`), shows avatar + edit pencil
  (file input), editable **Name**, read-only **Email account** display.
- **Save Change** → `saveProfile(username, {firstName,lastName,description},
  pictureFile)` from `api/profile.ts`. On success: refresh `dashboardStore`,
  close.
- Mockup shows a single "Name" field; map to `firstName` (keep `lastName`/
  `description` passed through unchanged from the loaded user so we don't wipe
  them). Email is display-only here (full email-change flow stays on
  `/profile`).

**`Modal.svelte`** — shared modal primitive.
- Backdrop, centered card, X close button, `Escape` to close, focus on open,
  scroll-lock while open. Slot for body. Keeps the two modals DRY.

### Modified components

**`DashboardHeader.svelte`**
- Replace static `avatar-mark` span with a `<button class="avatar-button">`
  that toggles the menu (`aria-haspopup="menu"`, `aria-expanded`).
- Remove the `theme-toggle` button and its styles.
- Render `<ProfileMenu>` anchored to the avatar; wire its emits up to the app
  (via callback props passed down from `DashboardApp`).
- Static text (`pageLabel`, `statusLabel`) sourced from `$i18n` where it is
  UI chrome (brand stays literal).

**`DashboardApp.svelte`**
- Owns modal open-state: `profileOpen`, `settingsOpen` (`$state`).
- Passes `onOpenProfile`/`onOpenSettings`/`onLogout` handlers to
  `DashboardHeader` → `ProfileMenu`.
- Renders `<SettingsModal>` and `<ProfileModal>` at shell root (correct overlay
  stacking, above header `z-index: 50`).

**`data/dashboard.ts`**
- Add `email: string | null` to `DashboardUser`.
- `mapUser`: `email: user.email ?? null` (DTO already exposes `email?`).

**`index.ts` (bootstrap)**
- Apply the persisted language at startup next to `initTheme()` (e.g.
  `initI18n()` if the store needs an explicit kick; with a self-initializing
  `language` store this may be a no-op import).

### i18n — `src/frontend/dashboard/src/i18n/`

- **`index.ts`** — `export const languages = ["en","de"]`, `defaultLanguage`,
  `fallbackLanguage` (`"en"`), `export type I18N = typeof en`.
- **`lang/en.ts`** — master catalog (no type import).
- **`lang/de.ts`** — German; `import type {I18N}` for completeness checking.
- **`stores/i18n.store.ts`**
  - `language`: `writable<LanguageCode>` initialized from
    `localStorage.getItem("openbook-dashboard-language")` ?? `defaultLanguage`;
    `.subscribe` persists changes.
  - `i18n`: `derived(language, $lang => catalogs[$lang] ?? catalogs.en)` with
    both catalogs statically imported. Synchronous, no dynamic import.
- Consumption: `$i18n.Menu.Profile`, etc.

Initial key tree (breadth A surfaces only):

```
Menu:        { Profile, Settings, Notification, Logout, Allow, Mute }
Settings:    { Title, Theme, ThemeLight, ThemeDark, Language }
Profile:     { Title, Name, Email, Save }
Header:      { StatusOnline }   // page labels remain prop-driven
Footer:      { Copyright }
```

## Data flow

```
avatar <button> click
  -> DashboardHeader toggles ProfileMenu(open)
     -> row click emits intent
        -> DashboardApp sets profileOpen / settingsOpen, or runs logout
           -> SettingsModal / ProfileModal render at shell root
```

Theme: SettingsModal -> setTheme() -> theme store -> data-theme attribute.
Language: SettingsModal -> language store -> i18n derived store -> all $i18n
consumers re-render. Persisted via localStorage on both stores.

## Accessibility

- Avatar button: `aria-haspopup`, `aria-expanded`, `aria-label`.
- Menu: `role="menu"`, rows `role="menuitem"`; `Escape` closes; focus returns
  to the avatar.
- Modals: `role="dialog"`, `aria-modal="true"`, labelled by title; `Escape`
  closes; focus moves into the dialog on open.

## Logout

The `app/` frontend links `#/accounts/logout` (allauth). The dashboard is a
separate bundle, so Log Out navigates the browser to the allauth logout
endpoint (`window.location.href = "/accounts/logout/"`). **Impl-time check:**
confirm the exact URL and whether a GET confirmation page or a POST is required;
adjust to a form-POST if allauth rejects GET.

## Testing

- Dashboard build passes (`npm run build` for the dashboard package; TS strict).
- Manual (Playwright or browser): open menu via avatar; Escape + outside-click
  close it; My Profile saves a name change and reflects it in the header;
  Settings toggles theme (data-theme flips) and language (visible chrome +
  menu/modals switch DE/EN); Notification Allow/Mute persists across reload;
  Log Out navigates to the logout endpoint.

## File change summary

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

## Open items (resolve during implementation)

1. Exact allauth logout URL/method (GET vs POST).
2. Whether `index.ts` needs an explicit i18n init call or the store
   self-initializes from localStorage on import.
