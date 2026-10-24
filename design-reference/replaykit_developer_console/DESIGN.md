---
name: ReplayKit Developer Console
colors:
  surface: '#121316'
  surface-dim: '#121316'
  surface-bright: '#38393c'
  surface-container-lowest: '#0d0e11'
  surface-container-low: '#1b1b1f'
  surface-container: '#1f1f23'
  surface-container-high: '#292a2d'
  surface-container-highest: '#343538'
  on-surface: '#e3e2e6'
  on-surface-variant: '#c8c4d6'
  inverse-surface: '#e3e2e6'
  inverse-on-surface: '#2f3034'
  outline: '#928f9f'
  outline-variant: '#474554'
  surface-tint: '#c6bfff'
  primary: '#c6bfff'
  on-primary: '#28029f'
  primary-container: '#8c80ff'
  on-primary-container: '#22008e'
  inverse-primary: '#5849cc'
  secondary: '#7bd0ff'
  on-secondary: '#00354a'
  secondary-container: '#00a6e0'
  on-secondary-container: '#00374d'
  tertiary: '#4edea3'
  on-tertiary: '#003824'
  tertiary-container: '#00a572'
  on-tertiary-container: '#00311f'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#e4dfff'
  primary-fixed-dim: '#c6bfff'
  on-primary-fixed: '#160066'
  on-primary-fixed-variant: '#402db4'
  secondary-fixed: '#c4e7ff'
  secondary-fixed-dim: '#7bd0ff'
  on-secondary-fixed: '#001e2c'
  on-secondary-fixed-variant: '#004c69'
  tertiary-fixed: '#6ffbbe'
  tertiary-fixed-dim: '#4edea3'
  on-tertiary-fixed: '#002113'
  on-tertiary-fixed-variant: '#005236'
  background: '#121316'
  on-background: '#e3e2e6'
  surface-variant: '#343538'
typography:
  headline-lg:
    fontFamily: Inter
    fontSize: 1.25rem
    fontWeight: '600'
    lineHeight: 1.75rem
    letterSpacing: -0.015em
  headline-md:
    fontFamily: Inter
    fontSize: 1rem
    fontWeight: '600'
    lineHeight: 1.5rem
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Inter
    fontSize: 0.875rem
    fontWeight: '600'
    lineHeight: 1.25rem
    letterSpacing: -0.005em
  body-md:
    fontFamily: Inter
    fontSize: 0.875rem
    fontWeight: '400'
    lineHeight: 1.375rem
  body-sm:
    fontFamily: Inter
    fontSize: 0.8125rem
    fontWeight: '400'
    lineHeight: 1.25rem
  body-xs:
    fontFamily: Inter
    fontSize: 0.75rem
    fontWeight: '400'
    lineHeight: 1.125rem
  code-md:
    fontFamily: JetBrains Mono
    fontSize: 0.8125rem
    fontWeight: '400'
    lineHeight: 1.25rem
  code-sm:
    fontFamily: JetBrains Mono
    fontSize: 0.75rem
    fontWeight: '400'
    lineHeight: 1.125rem
  code-xs:
    fontFamily: JetBrains Mono
    fontSize: 0.6875rem
    fontWeight: '400'
    lineHeight: 1rem
  label-md:
    fontFamily: Inter
    fontSize: 0.75rem
    fontWeight: '500'
    lineHeight: 1rem
    letterSpacing: 0.01em
  label-mono:
    fontFamily: JetBrains Mono
    fontSize: 0.6875rem
    fontWeight: '500'
    lineHeight: 0.875rem
    letterSpacing: 0.02em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  gutter: 0.75rem
  margin: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 0.75rem
  space-lg: 1rem
  space-xl: 1.5rem
---

## Brand & Style

This design system targets systems engineers, full-stack developers, and QA automation leads investigating complex software regressions. The aesthetic merges the disciplined spatial economy of professional IDEs with the hyper-refined micro-interactions of Linear and Raycast.

### Core Visual Philosophy
- **Instrument-Grade Precision:** The interface acts as a high-fidelity instrument panel. Density is a feature; screen real estate is preserved to maximize log output, network inspection frames, and execution traces without excessive nested scrolling.
- **Dark-First Atmosphere:** Designed exclusively for high-focus, low-fatigue developer workflows. The background layering uses strict step-wise tonal steps rather than heavy blur dynamics.
- **Structural Legibility:** Structural definition is maintained through 1px crisp, low-contrast borders rather than deep dropshadows or heavy drop elevation.
- **Keyboard-Centric Affordances:** Primary affordances emphasize immediate keyboard shortcuts, visible command glyphs, and high-visibility status states.

## Colors

The palette is engineered specifically for deep-contrast code readability, subtle panel division, and low-saturation semantic indicators.

### Background & Surface Hierarchy
- **Canvas Base (`#101114`):** The outermost viewport frame, background canvas behind tab wells, and terminal gutters.
- **Sidebar & Chrome (`#15161A`):** Activity bar, navigation sidebar, auxiliary utility panels, and top window chrome.
- **Panels & Cards (`#1B1D22`):** Primary inspectors, diff viewers, log panels, split editors, and active cards.
- **Surface Popover / Hover (`#22242B`):** Context menus, command palette dropdowns, tooltips, and active hover states on panels.

### Structural Delimiters
- **Borders & Dividers (`#30323A`):** Strict 1px borders used between panes, table rows, and panel headers.
- **Subtle Borders (`#23252C`):** Subdued inner dividers for compact list items and non-active tab separators.

### Typography & Content
- **Text Primary (`#F4F4F5`):** Titles, active tab labels, primary log messages, code syntax keywords.
- **Text Secondary (`#9B9DA7`):** Metadata, timestamps, line numbers, file paths, structural UI labels.
- **Text Muted (`#61636E`):** Disabled states, keyboard shortcut keys, inactive breadcrumbs.

### Semantic & Status
- **Accent Primary (`#8174F8`):** Active indicators, focus rings, primary actions, verification timeline markers.
- **Error (`#EF4444`):** Regression traces, failed tests, fatal assertions. Rendered primarily with muted alpha backgrounds (`rgba(239, 68, 68, 0.12)`) and crisp borders (`rgba(239, 68, 68, 0.3)`).
- **Success (`#10B981`):** Passed assertions, validated replay artifacts, clean health checks.
- **Warning (`#F59E0B`):** Non-blocking console warnings, performance thresholds, timing skews.
- **Info (`#38BDF8`):** AI assistant traces, synthetic network requests, metadata telemetry.

## Typography

The typography implements a strict bifurcation between UI structure and runtime data:

- **UI Framework (`Inter`):** Renders pane headers, buttons, navigation items, tooltips, and assistant dialogues. Clean, sans-serif shapes ensure high density without visual noise.
- **Data & Runtime Surfaces (`JetBrains Mono`):** Applied systematically to all log views, source code blocks, commit hashes, memory addresses, API endpoints, keybindings, and tabular trace rows.

### Rules for Font Weights and Sizing
- Never exceed `1.25rem` (20px) for regular window and panel chrome. The app is a dense productivity tool, not an editorial canvas.
- Maintain tabular lining numbers across all monospace tokens to avoid horizontal layout shift during live log streaming.

## Layout & Spacing

The layout is built around a multi-pane split layout calibrated for a primary desktop target of 1440px wide and above.

### Layout Model
- **Workbench Architecture:** Consists of three primary vertical divisions:
  1. **Primary Navigation Bar / Tree Rail:** 240px to 280px fixed width.
  2. **Central Stage (Timeline / Trace Graph / Code Diff):** Fluid width, occupying remaining space.
  3. **Inspection / AI Verification Panel:** 360px to 420px contextual drawer or docked pane.
- **Sub-pane Divisions:** Inner panels use vertical and horizontal splitters with a uniform 1px boundary. Margins are compact (`space-md` or `space-sm`) to maximize density.
- **Component Padding Standards:** Form elements, list items, and console entries use a baseline 4px (`space-xs`) vertical rhythm and 8px (`space-sm`) horizontal rhythm.

## Elevation & Depth

This system avoids expressive blur or diffused cloud shadows, relying instead on high-precision structural boundaries and stepped panel luminance.

### Depth Hierarchy
- **Level 0 (Base Canvas):** Background `#101114`. Receded plane for window backdrop and tab gutters.
- **Level 1 (Docked Surfaces):** Background `#15161A`, enclosed by `1px solid #30323A`. Applied to sidebars, docked bottom terminals, and collapsed docks.
- **Level 2 (Active Focus Panels & Workspaces):** Background `#1B1D22`, enclosed by `1px solid #30323A`.
- **Level 3 (Floating Overlays, Command Palette, Tooltips):** Background `#22242B` with a dual border treatment: `1px solid #383A44` and a minimal direct drop shadow `0 8px 24px -4px rgba(0, 0, 0, 0.6)`.

### Focus and Selection States
- Avoid glow halos. Focus indicators must be rendered as an explicit `1px solid #8174F8` outline with an inner `1px` transparent offset.

## Shapes

The design system enforces a compact, semi-sharp corner language (`roundedness: 1`, base radius 4px / `0.25rem`) that mirrors terminal windows and modern developer IDEs.

### Radius Assignments
- **Inner Micro Controls:** Checkboxes, badge tags, inline code snippets, and keyboard keys use `0.25rem` (4px).
- **Interactive Inputs:** Buttons, search inputs, tabs, and select triggers use `0.25rem` (4px).
- **Floating Modals & Dropdown Windows:** Use `0.5rem` (8px).
- **Full Shell Windows / Panels:** Outer frame corners use `0.5rem` (8px), inner docked sub-windows remain completely square (`0px`) against shared 1px borders.

## Components

### Buttons & Interactive Controls
- **Primary Action:** Solid background `#8174F8`, text `#FFFFFF`, font weight 500, height 28px, padding 0 10px. Hover: `#7062E5`. Active: `#6253DE`.
- **Secondary / Ghost:** Transparent background, text `#F4F4F5`, 1px border `#30323A`. Hover: background `#22242B`, border `#3E414C`.
- **Icon / Tool Button:** 24x24px or 28x28px, borderless, text `#9B9DA7`. Hover: background `#22242B`, text `#F4F4F5`.

### Status Badges & Chips
- Compact layout: height 20px, font `code-xs`, uppercase or tabular lowercase, border-radius 3px.
- **Error Tag:** Background `rgba(239, 68, 68, 0.1)`, text `#EF4444`, border `1px solid rgba(239, 68, 68, 0.25)`.
- **Success Tag:** Background `rgba(16, 185, 129, 0.1)`, text `#10B981`, border `1px solid rgba(16, 185, 129, 0.25)`.
- **Warning Tag:** Background `rgba(245, 158, 11, 0.1)`, text `#F59E0B`, border `1px solid rgba(245, 158, 11, 0.25)`.
- **Info / Trace Tag:** Background `rgba(56, 189, 248, 0.1)`, text `#38BDF8`, border `1px solid rgba(56, 189, 248, 0.25)`.

### Log Viewers & Trace Tables
- Alternating striping is forbidden. Depth is achieved via line borders `1px solid #1F2128`.
- Row height: 22px to 24px. Monospace font `code-sm`.
- Columns: Fixed-width timestamp (`#61636E`), fixed-width level badge, variable-width payload with highlighted syntax keywords.
- Active row selection: Background `rgba(129, 116, 248, 0.12)`, left border accent `2px solid #8174F8`.

### Input Fields & Search Bars
- Background `#15161A`, border `1px solid #30323A`, text `#F4F4F5`, placeholder `#61636E`.
- Focus state: Border `#8174F8`, zero blur glow.
- Embedded keyboard shortcut indicator (e.g., `⌘K`) aligned right using `label-mono`, background `#22242B`, border `1px solid #30323A`, padding 2px 4px, border radius 3px.

### Tab Bars & Window Headers
- Tab height: 32px. Inactive tabs: background `#15161A`, text `#9B9DA7`, right border `1px solid #23252C`.
- Active tab: background `#1B1D22`, text `#F4F4F5`, top border `2px solid #8174F8`, bottom border none (flush with panel interior).
- Close action visible on hover or active tab only.

### Keyboard Shortcut Chips (`<Kbd>`)
- Typography: `code-xs`, font weight 500.
- Surface: `#1B1D22`, border `1px solid #30323A`, box-shadow `0 1px 0 0 #30323A`.
- Color: `#9B9DA7`. Padding: 1px 4px, min-width 18px, text-align center.