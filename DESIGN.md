# DESIGN.md — FireRiskApp Design System

> Design reference for the CHICHORRO fire risk assessment platform.
> Stack: React 18 + TypeScript + Vite + Tailwind CSS (with custom config).
> Last updated: 2026-05-12

---

## 1. Design Philosophy

FireRiskApp is an **engineering analysis tool**, not a consumer product.
Every UI decision should serve the engineer running a fire-risk assessment.

### Guiding principles

**Clarity over decoration.**
Data is the product. Chrome, gradients, and animations exist only to aid comprehension —
never as ornamentation. When in doubt, remove.

**Hierarchy through typography, not color.**
Use size, weight, and spacing to establish importance.
Reserve color for semantic communication (risk level, status, state).

**Density with breathing room.**
Engineering workflows are data-dense. Layouts should pack meaningful information
without feeling cramped. Consistent whitespace creates structure.

**Predictability.**
Every button, card, and input behaves the same across all modules.
Engineers build mental models fast — break the pattern only with intention.

**Accessibility is not optional.**
Focus states, ARIA roles, and color-contrast ratios are requirements.
Screen-reader users and keyboard navigators are first-class.

### What this tool is NOT

- Not a dashboard product (avoid KPI-card overload, chart-as-decoration)
- Not a mobile-first consumer app (desktop-first, data-dense layouts are correct)
- Not a startup landing page (no hero sections, gradients as decorative, big taglines)
- Not a gaming or gamification product (no progress bars for engagement, no confetti)

---

## 2. Design Tokens

### 2.1 Color Palette

All colors are defined in `tailwind.config.js` under `theme.extend.colors`.

#### Brand (Fire Red)

Used for primary actions, active navigation, calculated result values, and brand identity.

| Token | Hex | Usage |
|-------|-----|-------|
| `brand-50` | `#fef2f2` | Lightest tint — result card backgrounds |
| `brand-100` | `#fee2e2` | Light backgrounds for brand-tinted panels |
| `brand-500` | `#ef4444` | Mid-range (rarely used directly) |
| `brand-600` | `#dc2626` | Focus ring accent |
| `brand-700` | `#b91c1c` | Button hover state |
| `brand-800` | `#991b1b` | **Primary brand color** — active nav, primary buttons, result values |
| `brand-900` | `#7f1d1d` | Auth page background, darkest brand |

> `brand-800` is the canonical brand color. Use it for CTAs and primary data values.

#### Ink (Neutral Slate)

All text, borders, backgrounds, and structural UI elements use the ink scale.

| Token | Hex | Usage |
|-------|-----|-------|
| `ink-50` | `#f8fafc` | App shell background (`bg-ink-50`) |
| `ink-100` | `#f1f5f9` | Hover backgrounds, subtle fills |
| `ink-200` | `#e2e8f0` | Borders, dividers, card edges |
| `ink-400` | `#94a3b8` | Placeholder text, icons at rest |
| `ink-500` | `#64748b` | Secondary/muted text, overline labels |
| `ink-600` | `#475569` | Body text |
| `ink-700` | `#334155` | Medium-weight UI text, nav labels |
| `ink-800` | `#1e293b` | Strong body text |
| `ink-900` | `#0f172a` | **Primary text color** — headings, labels |
| `ink-950` | `#020617` | Modal overlay (`bg-ink-950/40`) |

> Never use raw Tailwind `gray-*` or `slate-*` tokens in new code. Use `ink-*` exclusively.

#### Semantic Colors (Tailwind defaults — use as-is)

These communicate state and risk. Do not invent new colors for new states — map to this set.

| Semantic | Token family | Use case |
|----------|-------------|----------|
| Success | `emerald-*` | Acceptable risk, confirmed state, compliant data |
| Warning | `amber-*` | Stale data, mid-risk classification (B scale) |
| Caution | `orange-*` | Elevated risk classification (C scale) |
| Error | `red-*` | Calculation errors, not-acceptable risk, field validation |
| Critical | `rose-*` | Highest risk classifications (E, F scale) |
| Extreme | `fuchsia-*` | D classification on the RI scale |
| Info | `sky-*` | Secondary data panels, cost displays, VHE scenario tinting |
| Accent green | `emerald-50/30` with `emerald-300` border | VVE scenario group |

#### Risk Scale Color Map

Used in `RiPage.tsx` and `InterventionsPage.tsx`. Always use this mapping — never ad-hoc colors.

| RI Class | Color token | Rationale |
|----------|------------|-----------|
| A++, A+, A | `text-emerald-700` | Low risk — safe green |
| B+, B, B- | `text-amber-600` | Medium risk — cautionary amber |
| C+, C, C- | `text-orange-600` | Elevated risk — warning orange |
| D | `text-fuchsia-700` | High risk — visual break from warm palette |
| E | `text-rose-700` | Very high risk — strong red |
| F | `text-rose-800` | Critical — darkest red |

---

### 2.2 Typography

**Font:** DM Sans (loaded via `@fontsource/dm-sans` or equivalent). Fallback: `system-ui, sans-serif`.

The typographic scale is fixed. Do not introduce new sizes outside this set.

#### Scale

| Role | Classes | Size / Weight |
|------|---------|---------------|
| Page title | `text-2xl font-bold text-ink-900` | 24px / 700 |
| Card / section header | `text-lg font-semibold text-ink-900` | 18px / 600 |
| Form label | `text-sm font-medium text-ink-700` | 14px / 500 |
| Body text | `text-sm text-ink-600` | 14px / 400 |
| Section overline | `text-xs font-semibold uppercase tracking-wide text-ink-500` | 12px / 600 / uppercase |
| Nav group label | `text-[10px] font-semibold uppercase tracking-widest text-ink-400` | 10px / 600 / uppercase |
| Button | `text-sm font-semibold` | 14px / 600 |
| Primary metric (large) | `text-4xl font-bold` | 36px / 700 |
| Primary metric (medium) | `text-3xl font-bold` | 30px / 700 |
| Secondary metric | `text-2xl font-semibold` | 24px / 600 |
| Tertiary metric | `text-lg font-semibold` | 18px / 600 |
| Code / monospace | `font-mono text-sm text-ink-500 rounded bg-ink-100 px-1` | 14px / mono |

#### Rules

- **Never** set `text-base` (16px) in the UI — the baseline is `text-sm` (14px).
- **Never** use raw `font-bold` on body paragraphs — only on metrics and headings.
- Overlines (`uppercase tracking-wide text-xs`) are for section labels and result card labels only.
- Use `tabular-nums` on any displayed numeric value that may change dynamically.
- Line height: default Tailwind `leading-5` (20px) for body, `leading-6` (24px) for descriptive paragraphs.

---

### 2.3 Spacing

All spacing follows the Tailwind 4px base grid. The following values are canonical in this project.

#### Padding

| Context | Classes |
|---------|---------|
| Card body | `px-6 py-5` |
| Card header | `px-6 py-4` |
| Form / result box | `px-4 py-3` |
| Large result box | `px-5 py-4` |
| Input field | `px-3 py-2.5` |
| Button | `px-4 py-2.5` |
| Nav link | `px-3 py-2` |
| Sidebar brand area | `px-4 py-5` |
| Modal | `p-6` |

#### Gaps and stacking

| Context | Classes |
|---------|---------|
| Page section spacing | `space-y-6` |
| Card inner spacing | `space-y-4` or `space-y-5` |
| Form field grid gap | `gap-5` |
| Result card grid gap | `gap-4` |
| Intervention list gap | `gap-6` |
| Button row gap | `gap-3` |
| Inline icon + label gap | `gap-2` |

---

### 2.4 Border Radius

Two canonical radii. Do not introduce new values.

| Radius | Token | Usage |
|--------|-------|-------|
| 12px | `rounded-xl` | Inputs, buttons, result boxes, small panels |
| 16px | `rounded-2xl` | Cards, modals, the `Card` component |

Sidebar nav links use `rounded-lg` (8px) — an intentional exception for tighter nav items.

---

### 2.5 Shadows

| Token | Definition | Usage |
|-------|-----------|-------|
| `shadow-soft` | `0 1px 2px rgba(15,23,42,.06), 0 8px 24px rgba(15,23,42,.06)` | All `Card` components |
| `shadow-sm` | Tailwind default | Primary buttons, active nav items |
| `shadow-xl` | Tailwind default | Modals |

> Define `shadow-soft` in `tailwind.config.js`. Never replace it with Tailwind's built-in `shadow-md` or `shadow-lg` for cards — the custom token is intentionally less dramatic.

---

## 3. Layout System

### 3.1 Shell

```
┌──────────────────────────────────────────────────┐
│  Sidebar (fixed, w-56 = 224px, full height)      │
│  bg-white · border-r border-ink-200              │
│  ┌────────────────────────────────────────────┐  │
│  │  Main content area (ml-56, flex-1)         │  │
│  │  px-6 py-8                                 │  │
│  │  ┌──────────────────────────────────────┐  │  │
│  │  │  Content wrapper (mx-auto max-w-5xl) │  │  │
│  │  └──────────────────────────────────────┘  │  │
│  └────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────┘
```

- **Shell background:** `bg-ink-50` (not white — provides depth for white cards)
- **Sidebar:** `fixed inset-y-0 left-0 z-10 w-56` — never change the fixed width
- **Content offset:** `ml-56` — matches sidebar width exactly
- **Content padding:** `px-6 py-8`
- **Max content width:** `max-w-5xl` (64rem / 1024px) — enforce on every page

### 3.2 Page Structure

Every module page follows this vertical structure:

```
Page heading row          (flex, space-between, col→row at lg:)
  ├── Title + description
  └── ModuleGlobalValueCard (max-w-[17rem], lg:ml-auto)

space-y-6

Card 1 (form inputs)
  ├── CardHeader
  └── CardBody
        └── grid gap-5 sm:grid-cols-2

Card 2 (results)
  ├── CardHeader
  └── CardBody
        └── grid gap-4 sm:grid-cols-2 lg:grid-cols-N
```

### 3.3 Responsive Grid

| Context | Mobile | Tablet (sm: 640px) | Desktop (lg: 1024px) |
|---------|--------|---------------------|----------------------|
| Form fields | 1 col | 2 col | 2 col |
| Module status cards (RiPage) | 1 col | 2 col | 4 col |
| Main result cards | 1 col | 1 col | 3 col |
| Intervention panels | 1 col | 1 col | 2 col |

> Only two breakpoints are used: `sm:` and `lg:`. Do not add `md:` or `xl:` unless there is a specific, documented reason.

### 3.4 Auth Pages

Auth pages (Login, SignUp, ForgotPassword, ResetPassword) use a distinct layout:
- Full-viewport gradient background: `bg-gradient-to-br from-brand-900 via-brand-800 to-ink-900`
- Centered card: `min-h-screen flex items-center justify-center px-4 py-12`
- Card max-width: `max-w-lg w-full`
- Decorative radial overlay: `[background-image:radial-gradient(circle_at_20%_20%,white_0,transparent_45%)]`

This is the only place gradient backgrounds are used. All other pages use `bg-ink-50`.

---

## 4. Component Specifications

### 4.1 Button

**File:** `src/components/ui/Button.tsx`

Three variants only. Do not add variants without updating this spec.

| Variant | Use case | Key classes |
|---------|----------|-------------|
| `primary` (default) | Main CTA — one per view | `bg-brand-800 text-white hover:bg-brand-700 shadow-sm` |
| `secondary` | Cancel, secondary actions | `bg-white border border-ink-200 text-ink-900 hover:bg-ink-50` |
| `ghost` | Tertiary, inline, icon-adjacent | `text-ink-700 hover:bg-ink-100` |

**Base classes (all variants):**
```
inline-flex items-center justify-center gap-2
rounded-xl px-4 py-2.5 text-sm font-semibold
transition focus:outline-none
focus-visible:ring-2 focus-visible:ring-offset-2
disabled:cursor-not-allowed disabled:opacity-50
```

**Loading state:**
- Set `disabled` attribute
- Change label text to "A processar…" (or context-specific equivalent)
- Never use a spinner unless the wait exceeds ~3s

**Icon buttons (square):**
```
size-11 aspect-square rounded-xl border border-ink-200 bg-ink-50
text-ink-500 hover:bg-ink-100
```

### 4.2 Card

**File:** `src/components/ui/Card.tsx`

The fundamental layout unit for all content sections.

```
Card:       rounded-2xl border border-ink-200/80 bg-white shadow-soft
CardHeader: border-b border-ink-100 px-6 py-4  (flex items-center justify-between)
CardBody:   px-6 py-5
```

- **Title** in CardHeader: `text-lg font-semibold text-ink-900`
- **Description** in CardHeader: `mt-1 text-sm text-ink-500`
- **Right slot** in CardHeader: for action buttons or toggle controls

Cards should not be nested. If a sub-panel is needed inside a card, use a Result Box (§4.5).

### 4.3 Form Fields

**File:** `src/components/ui/Field.tsx`

#### Label

```tsx
<label className="block text-sm font-medium text-ink-700">
```

Always `block` (not inline). Always above the field, never beside it (except in narrow inline contexts).

#### Select

```
mt-1 w-full max-w-md rounded-xl border border-ink-200 bg-white
px-3 py-2.5 text-sm text-ink-900 shadow-sm outline-none
transition focus:border-brand-700 focus:ring-2 focus:ring-brand-700/20
```

#### Text Input (inline in pages, not via Field component)

```
mt-1 w-full max-w-md rounded-xl border border-ink-200 bg-white
px-3 py-2.5 text-sm text-ink-900 outline-none ring-brand-800/0
transition focus:border-brand-800 focus:ring-4 focus:ring-brand-800/15
```

#### Error / Missing Field State

Add `ring-2 ring-red-400` to the input/select element when validation fails.
Show an error message immediately below using the Error Alert (§4.8).

#### Disabled State

Add Tailwind `disabled:opacity-50 disabled:cursor-not-allowed` — never hide a disabled field.

### 4.4 Password Input

**File:** `src/components/ui/PasswordInput.tsx`

Extends Text Input with an absolute-positioned toggle button:
```
absolute inset-y-0 right-0 flex items-center px-3
text-ink-400 hover:text-ink-600
```

Toggle uses SVG inline (no icon library). `tabIndex={-1}` to keep tab order on the field.
Use wherever passwords are entered: Login, SignUp, ResetPassword.

### 4.5 Result Box

An inline display panel for a single computed value. Used inside CardBody.

```
rounded-xl border px-4 py-3

Label: text-xs font-semibold uppercase tracking-wide [color]
Value: mt-1 tabular-nums text-2xl font-semibold [color]
```

Color variants:

| State | Border | Background | Label / Value color |
|-------|--------|------------|---------------------|
| Primary result | `border-brand-200` | `bg-brand-50` | `text-brand-700` / `text-brand-800` |
| Neutral | `border-ink-200` | `bg-ink-50` | `text-ink-500` / `text-ink-900` |
| Success | `border-emerald-200` | `bg-emerald-50` | `text-emerald-700` / `text-emerald-800` |
| Warning | `border-amber-200` | `bg-amber-50` | `text-amber-700` / `text-amber-800` |
| Error | `border-red-200` | `bg-red-50` | `text-red-700` / `text-red-800` |
| Info | `border-sky-200` | `bg-sky-50` | `text-sky-700` / `text-sky-900` |

**Stale state:** Value becomes `color: rgba(100, 116, 139, 0.55)` (inline style). This communicates the value is outdated without removing it. Show a "Valor desatualizado" overline label.

### 4.6 ModuleGlobalValueCard

**File:** `src/components/ui/ModuleGlobalValueCard.tsx`

Standalone result card displayed in the page header. Shows the current module's global computed value.

```
w-full max-w-[17rem] lg:ml-auto
rounded-2xl border border-ink-200 bg-white px-6 py-5 shadow-sm

Label: text-center text-xs font-semibold uppercase tracking-wide text-ink-500
Value: mt-2 text-center text-4xl font-bold tabular-nums
  - Fresh: text-brand-800
  - Stale: rgba(100, 116, 139, 0.55)
```

Subscribes to `MODULE_RESULTS_UPDATED_EVENT`. Shows "Valor desatualizado" when stale.
One per module page, always in the page header row.

### 4.7 Collapsible Section

Used inside factor section pages (POI, DPI, ESCI). Groups related fields under a toggleable header.

**Header:**
```
flex items-center justify-between px-0 py-2 cursor-pointer select-none
```

**Chevron icon:**
```
transition-transform duration-300
rotate-180 (when collapsed) → no rotation (when expanded)
```

**Collapse animation (CSS grid trick):**
```
grid transition-[grid-template-rows] duration-300 ease-in-out
grid-rows-[0fr] (collapsed) → grid-rows-[1fr] (expanded)
```

State persisted in `sessionStorage` with key `collapse:{formKey}`.

### 4.8 Alert / Banner Messages

Used for inline status feedback within pages. Four semantic types:

| Type | Classes |
|------|---------|
| Error | `rounded-xl border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-800` |
| Warning | `rounded-xl border border-amber-200 bg-amber-50 px-3 py-2 text-sm text-amber-800` |
| Success | `rounded-xl border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-800` |
| Info | `rounded-xl border border-sky-200 bg-sky-50 px-4 py-3 text-sm text-sky-700` |

Always add `role="alert"` to error messages. Use `role="status"` for non-critical notices.

Auto-dismiss success banners: fade out after 3s using `transition-opacity duration-500 opacity-0`.

### 4.9 Modal / Dialog

Triggered from `AppLayout.tsx`. Three modals currently: session expired, clear session, logout confirm.

**Overlay:**
```
fixed inset-0 z-50 flex items-center justify-center bg-ink-950/40 px-4
```

**Panel:**
```
w-full max-w-lg rounded-2xl border border-ink-200 bg-white p-6 shadow-xl
role="dialog" aria-modal="true" aria-labelledby="modal-title"
```

**Structure inside panel:**
```
h2 (id="modal-title"): text-xl font-bold text-ink-900
p (description):        mt-3 text-sm leading-6 text-ink-600
action row:             mt-6 flex flex-wrap justify-end gap-3
```

Use `z-[60]` only for the session-expired modal (must always appear on top). All others use `z-50`.

### 4.10 Navigation Sidebar

**File:** `src/components/AppLayout.tsx`

```
fixed inset-y-0 left-0 z-10 flex w-56 flex-col border-r border-ink-200 bg-white
```

**Sections (top to bottom):**
1. Brand area (`border-b border-ink-200 px-4 py-5`) — logo + app name
2. Navigation (`flex-1 px-3 py-4 space-y-3`) — grouped nav links
3. Session actions (`px-3 pb-4`) — buttons at bottom

**Nav group label:**
```
px-3 mb-1 text-[10px] font-semibold uppercase tracking-widest text-ink-400
```

**Nav link states:**
```
Active:   bg-brand-800 text-white shadow-sm rounded-lg px-3 py-2
Inactive: text-ink-700 hover:bg-ink-100 rounded-lg px-3 py-2
```

**User avatar:**
```
h-8 w-8 rounded-full bg-brand-800 text-sm font-bold text-white
flex items-center justify-center
```
Displays the first letter of the username.

### 4.11 Data Table (proposed — not yet implemented)

For the `/admin/log` and `/admin/users` pages. Define now so future implementation is consistent.

**Container:**
```
w-full overflow-x-auto rounded-2xl border border-ink-200 bg-white shadow-soft
```

**Table:**
```
w-full text-sm border-collapse
```

**Header row:**
```
border-b border-ink-200 bg-ink-50
th: px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-ink-500
```

**Body rows:**
```
tr: border-b border-ink-100 hover:bg-ink-50/50 transition
td: px-4 py-3 text-sm text-ink-700
```

Do not stripe rows — use the subtle hover state for scan-ability instead.

### 4.12 Badge / Tag (proposed — not yet implemented)

For displaying role labels, status chips, and event types in the access log.

**Inline badge:**
```
inline-flex items-center rounded-md px-2 py-0.5
text-xs font-semibold
```

| Variant | Classes |
|---------|---------|
| Neutral | `bg-ink-100 text-ink-700` |
| Success | `bg-emerald-100 text-emerald-800` |
| Warning | `bg-amber-100 text-amber-800` |
| Error | `bg-red-100 text-red-800` |
| Brand | `bg-brand-100 text-brand-800` |

**ID badge (circular, as in InterventionsPage):**
```
flex h-5 w-6 shrink-0 items-center justify-center
rounded-full bg-ink-100 text-xs font-bold text-ink-700
```

---

## 5. State & Feedback Patterns

### 5.1 Loading State

- Disable the submit button immediately on click.
- Change button label to context-specific Portuguese text (e.g., "A calcular…", "A guardar…", "A iniciar sessão…").
- Never show a spinner unless the operation takes more than ~3 seconds (backend constraint).
- Do not gray out the entire form — only the button.

### 5.2 Stale Data

When inputs change after a calculation has been performed:

- The old result remains visible but fades to `rgba(100, 116, 139, 0.55)`.
- A "Valor desatualizado" label appears in amber above or beside the result.
- A red banner appears on RiPage when any module input changes.
- The stale value is stored in `module-results-stale` in sessionStorage.
- Cleared on successful recalculation.

> Do not remove stale results entirely — engineers need to see the previous value to understand the magnitude of the change.

### 5.3 Validation Errors

- Show `ring-2 ring-red-400` on the specific field that failed.
- Show an Error Alert (§4.8) immediately below the field or at the top of the section.
- Use `role="alert"` so screen readers announce the error.
- Keep the error visible until the field is corrected and re-submitted.

### 5.4 Success Confirmation

- Use a Success Alert (§4.8) that auto-dismisses after 3 seconds.
- Use `transition-opacity duration-500` for the fade.
- Do not navigate away automatically after success unless the action is destructive (e.g., account deletion).

### 5.5 Empty / No Results State

When a module has not been calculated yet:
- The result area shows `—` (em dash) in `text-ink-300`.
- No error is shown — absence of a result is normal before first calculation.
- The ModuleGlobalValueCard shows the empty state without a stale indicator.

---

## 6. Form Conventions

### 6.1 Field Grid Layout

All form sections use a 2-column responsive grid:
```
grid gap-5 sm:grid-cols-2
```

Fields that are logically wide (e.g., a text area, or a field with very long labels) may span both columns using `sm:col-span-2`.

Never use 3-column form grids.

### 6.2 Conditional Fields

Fields that depend on other field values use `visibleWhen` predicates in the definitions file. When a field is hidden:
- It is removed from the DOM (not just `opacity-0`) — avoids stale values being submitted.
- Its corresponding result is excluded from module average computation.

### 6.3 Field "Não se aplica" (Not Applicable)

`0.00` is the canonical "not applicable" sentinel. Fields with value `0.00` are excluded from module averages. This is not an error state. Do not mark `0.00` fields as invalid.

### 6.4 Label Conventions (PT-PT)

- All user-facing text, labels, and error messages: **Portuguese (PT-PT)**.
- Internal code identifiers and comments: **English**.
- Portuguese: "Não se aplica", "Valor desatualizado", "A calcular…", "Índice de Risco".

---

## 7. Scenario Section Tinting

The CTI module uses background tints to visually separate input scenario groups. This is a targeted exception to the "no background color in forms" rule.

| Scenario | Border | Background | Heading color |
|----------|--------|------------|---------------|
| CI (Main compartment) | `border-ink-200` | `bg-white` | `text-ink-700` |
| VHE (Horizontal evacuation) | `border-sky-300` | `bg-sky-50/30` | `text-sky-800` |
| VVE (Vertical evacuation) | `border-emerald-300` | `bg-emerald-50/30` | `text-emerald-800` |

This pattern is **only used in CtiPage**. Do not apply scenario tinting to other modules.

---

## 8. Accessibility Standards

### Required for every new component

- Interactive elements must have visible focus styles: `focus-visible:ring-2 focus-visible:ring-offset-2`.
- Error messages must use `role="alert"`.
- Modal dialogs must use `role="dialog"`, `aria-modal="true"`, `aria-labelledby`.
- Icon-only buttons must have `aria-label`.
- Form fields must have associated `<label>` elements (for attribute matching id).
- Color is never the sole differentiator — pair color with text or icon.

### Color contrast

- All body text (`text-ink-600` on `bg-white`) must meet WCAG AA (4.5:1 for small text).
- `brand-800` (#991b1b) on `bg-white`: confirmed to meet AA. Do not lighten brand colors below `brand-700`.

### Keyboard navigation

- Tab order must be logical (follows visual flow).
- Modals must trap focus while open.
- Collapsible sections: toggle button must be keyboard-activatable (it already is via `<button>`).

---

## 9. Anti-Patterns

The following are explicitly prohibited in this codebase:

| Anti-pattern | Reason |
|-------------|--------|
| Raw `gray-*` / `slate-*` tokens | Use `ink-*` instead — consistent palette |
| `text-base` (16px) body text | Baseline is `text-sm` (14px) |
| Nested cards | Breaks visual hierarchy — use Result Boxes (§4.5) inside cards |
| Gradient backgrounds outside auth pages | Decorative; breaks data-density aesthetic |
| Inline `style=` for colors (except stale state opacity) | Use Tailwind tokens |
| New Tailwind breakpoints (`md:`, `xl:`) without documented reason | Only `sm:` and `lg:` |
| Four or more button variants | Creates visual noise |
| Animations longer than 300ms | Slows engineering workflows |
| Conditional display via `opacity-0` (invisible but in DOM) | Use conditional rendering — avoids submitting hidden stale values |
| `text-center` on form labels | Labels are always left-aligned |

---

## 10. File Locations

| Purpose | File |
|---------|------|
| Tailwind config (tokens, font, shadow) | `app/frontend/tailwind.config.js` |
| Button component | `app/frontend/src/components/ui/Button.tsx` |
| Card component | `app/frontend/src/components/ui/Card.tsx` |
| Label + Select | `app/frontend/src/components/ui/Field.tsx` |
| Password input | `app/frontend/src/components/ui/PasswordInput.tsx` |
| Module value card | `app/frontend/src/components/ui/ModuleGlobalValueCard.tsx` |
| Shell layout + modals | `app/frontend/src/components/AppLayout.tsx` |
| Risk scale color map | `app/frontend/src/pages/RiPage.tsx` → `scaleClass()` |

---

## 11. Future Component Backlog

Components not yet built but planned:

| Component | Priority | Notes |
|-----------|----------|-------|
| Data Table | High | Needed for `/admin/log` and `/admin/users` |
| Badge / Tag | Medium | Role labels, event types in access log |
| Tooltip | Low | For explaining field abbreviations (e.g., POI_CC) |
| Loading Skeleton | Low | For async data loads > 1s |
| Pagination | Low | For access log if records exceed 50 |

---

*This document describes the current system and codifies conventions for future work.
Update it whenever a new component is introduced or a pattern changes.*
