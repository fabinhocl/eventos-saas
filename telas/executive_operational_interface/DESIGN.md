---
name: Executive Operational Interface
colors:
  surface: '#f8f9ff'
  surface-dim: '#cbdbf5'
  surface-bright: '#f8f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4ff'
  surface-container: '#e5eeff'
  surface-container-high: '#dce9ff'
  surface-container-highest: '#d3e4fe'
  on-surface: '#0b1c30'
  on-surface-variant: '#3d4947'
  inverse-surface: '#213145'
  inverse-on-surface: '#eaf1ff'
  outline: '#6d7a77'
  outline-variant: '#bcc9c6'
  surface-tint: '#006a61'
  primary: '#00685f'
  on-primary: '#ffffff'
  primary-container: '#008378'
  on-primary-container: '#f4fffc'
  inverse-primary: '#6bd8cb'
  secondary: '#565e74'
  on-secondary: '#ffffff'
  secondary-container: '#dae2fd'
  on-secondary-container: '#5c647a'
  tertiary: '#924628'
  on-tertiary: '#ffffff'
  tertiary-container: '#b05e3d'
  on-tertiary-container: '#fffbff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#89f5e7'
  primary-fixed-dim: '#6bd8cb'
  on-primary-fixed: '#00201d'
  on-primary-fixed-variant: '#005049'
  secondary-fixed: '#dae2fd'
  secondary-fixed-dim: '#bec6e0'
  on-secondary-fixed: '#131b2e'
  on-secondary-fixed-variant: '#3f465c'
  tertiary-fixed: '#ffdbce'
  tertiary-fixed-dim: '#ffb59a'
  on-tertiary-fixed: '#370e00'
  on-tertiary-fixed-variant: '#773215'
  background: '#f8f9ff'
  on-background: '#0b1c30'
  surface-variant: '#d3e4fe'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 36px
    fontWeight: '700'
    lineHeight: 44px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
  mono-sm:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 18px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  unit: 4px
  container-max-width: 1440px
  gutter: 24px
  sidebar-width: 280px
  margin-mobile: 16px
  margin-desktop: 32px
---

## Brand & Style

The design system is engineered for high-stakes, on-site event operations. It prioritizes clarity, speed of cognition, and a professional "command center" aesthetic. The brand personality is authoritative yet secondary to the data it presents, ensuring that event coordinators can manage complex logistics without visual fatigue.

The visual style is **Corporate / Modern** with a lean towards **Minimalism**. It utilizes a "quiet" interface where whitespace is treated as a functional tool to group related operational tasks. The emotional response is one of calm control—providing a sense of reliability and precision through structured alignment and a restrained aesthetic.

## Colors

The palette is anchored by a sophisticated **Teal (Primary)**, used specifically for high-priority actions and active states. This is balanced against a **Deep Slate (Secondary)** used for navigation and high-contrast typography, ensuring a grounded, professional feel.

The background uses a cool-toned **Slate-50**, providing a soft canvas that reduces glare during long hours of on-site use. Neutral tones are used strictly for structural elements like borders and secondary labels to maintain a clear visual hierarchy where the teal "action" color remains the undisputed focal point of the user's journey.

## Typography

The design system utilizes **Inter** exclusively to leverage its exceptional legibility in data-heavy environments. The typographic scale is optimized for information density without sacrificing readability.

- **Headlines:** Use tighter letter-spacing and heavier weights to anchor sections.
- **Labels:** Small caps or increased tracking are applied to uppercase labels (e.g., table headers) to differentiate them from interactive body text.
- **On-site Scaling:** For mobile operational views, `display-lg` should scale down to `headline-md` to ensure critical event metrics remain visible on handheld devices.

## Layout & Spacing

This design system employs a **Fixed-Fluid Hybrid Grid**. The primary navigation is a fixed sidebar, while the content area utilizes a 12-column fluid grid that caps at 1440px to prevent excessive line lengths in data tables.

A strict **4px baseline grid** governs all spacing. Vertical rhythm is maintained by using multiples of 8px (8, 16, 24, 32, 48, 64) for padding and margins. 

- **Desktop:** 32px outer margins with 24px gutters.
- **Tablet:** 24px outer margins; sidebar collapses into an icon-only rail (72px).
- **Mobile:** 16px outer margins; cards stack vertically; horizontal scrolling is permitted only for wide data tables.

## Elevation & Depth

The design system uses **Tonal Layers** and **Low-Contrast Outlines** rather than aggressive shadows to define hierarchy. This creates a "flat-plus" aesthetic that feels modern and lightweight.

- **Level 0 (Background):** `Slate-50` for the main application canvas.
- **Level 1 (Cards/Surface):** White background with a 1px border in `Slate-200`. No shadow.
- **Level 2 (Modals/Popovers):** White background with a very soft, diffused shadow (0px 10px 15px -3px rgba(0,0,0,0.05)) and a 1px `Slate-200` border.
- **Interaction:** Hover states on interactive rows or cards should use a subtle `Slate-100` background fill rather than an elevation change.

## Shapes

The shape language is **Soft (Level 1)**. This choice maintains a professional, geometric rigor while removing the harshness of sharp corners.

- **Standard (4px):** Used for input fields, checkboxes, and small buttons.
- **Large (8px):** Used for cards, containers, and modal windows.
- **Extra Large (12px):** Reserved for primary layout wrappers or featured "Quick Action" dashboard modules.
- **Strictness:** Do not use pill-shaped buttons; maintain the professional 4px corner radius for all primary calls to action.

## Components

### Data Tables
Tables are the heart of the operational experience. Use a "borderless" internal style with 1px `Slate-100` horizontal dividers only. Row height should be set to 56px for "Comfortable" or 40px for "Compact" views. Headers must use `label-md` with a subtle `Slate-50` background.

### KPI Cards
Standardized containers for event vitals (e.g., Check-in Rate). Features a `headline-sm` value, a `label-md` title, and a small trend indicator. KPI cards should be Level 1 surfaces.

### Primary Buttons
Solid Teal (`#0D9488`) with white text. Use 4px roundedness. For secondary actions, use a `Slate-200` border with `Slate-900` text.

### Sidebar Navigation
A deep Slate-900 background. Icons should be stroke-based (2px width) for clarity. The active state is indicated by a Teal vertical bar on the left edge and a subtle high-contrast text color.

### Form Fields
Floating labels or top-aligned labels are preferred. Input borders should be `Slate-300`, turning Teal on focus. Error states use a soft red (`#EF4444`) border and text.

### Badges / Status Chips
Used for "Registered," "Checked-in," or "VIP" status. Use a low-saturation background with a high-saturation text of the same hue (e.g., Light Teal background with Dark Teal text).