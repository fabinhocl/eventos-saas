---
name: Eventos Flex
colors:
  surface: '#f7f9fb'
  surface-dim: '#d8dadc'
  surface-bright: '#f7f9fb'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f2f4f6'
  surface-container: '#eceef0'
  surface-container-high: '#e6e8ea'
  surface-container-highest: '#e0e3e5'
  on-surface: '#191c1e'
  on-surface-variant: '#3d4947'
  inverse-surface: '#2d3133'
  inverse-on-surface: '#eff1f3'
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
  tertiary: '#4d5d73'
  on-tertiary: '#ffffff'
  tertiary-container: '#66768d'
  on-tertiary-container: '#fdfcff'
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
  tertiary-fixed: '#d3e4fe'
  tertiary-fixed-dim: '#b7c8e1'
  on-tertiary-fixed: '#0b1c30'
  on-tertiary-fixed-variant: '#38485d'
  background: '#f7f9fb'
  on-background: '#191c1e'
  surface-variant: '#e0e3e5'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.3'
  headline-sm:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: '1.4'
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.5'
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: '1'
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: '1'
    letterSpacing: 0.05em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 28px
    fontWeight: '600'
    lineHeight: '1.2'
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  2xl: 48px
  3xl: 64px
  gutter: 24px
  margin: 32px
  max-width: 1440px
---

## Brand & Style
The design system is engineered for a high-end B2B enterprise environment, focusing on clarity, precision, and a "quietly powerful" aesthetic. It targets professional event planners and corporate administrators who require a tool that reduces cognitive load while managing complex data. 

The style is **Modern Corporate** with a heavy emphasis on **Minimalism**. It utilizes a "Utility-First" visual hierarchy where whitespace is treated as a functional element to separate disparate data streams. The interface avoids unnecessary flourishes, relying instead on exquisite typography, precise alignment, and a sophisticated monochromatic foundation to make the primary Teal accents feel intentional and high-value.

## Colors
The palette is anchored by a sophisticated **Teal (#0d9488)**, used sparingly for primary actions and critical path indicators. The background architecture is built on a range of cool neutrals (`#f8fafc` to `#f1f5f9`) to create a "paper-like" layering effect. 

Secondary actions and deep text nodes use a Slate palette to maintain high contrast without the harshness of pure black. Status colors are desaturated to ensure they provide necessary feedback without disrupting the professional composure of the application. 
- **Primary:** High-engagement nodes and main CTAs.
- **Surface:** Subtle shifts in light grays to define container boundaries.
- **Feedback:** Discrete signaling for system states.

## Typography
**Inter** is utilized across all levels to leverage its exceptional legibility in data-heavy SaaS environments. The type scale is strictly mathematical to ensure a vertical rhythm that feels stable and reliable.

- **Headlines:** Use tighter letter spacing and semi-bold weights to command attention without being aggressive.
- **Body:** Generous line heights (1.5x+) are applied to ensure long-form data entry and reading do not cause eye fatigue.
- **Labels:** Small labels use a slightly heavier weight and uppercase tracking to differentiate them from body text within dense forms and table headers.

## Layout & Spacing
The layout follows a **12-column Fixed Grid** model for desktop, centered within the viewport to maintain a premium "dashboard" feel. On smaller screens, the layout transitions to a fluid 4-column structure with reduced margins.

Spacing follows an 8pt grid system (with 4px increments for micro-adjustments). To achieve the "generous whitespace" requirement, containers use `xl` (32px) padding as the default for card-based layouts. Functional groupings within cards use `md` (16px) or `sm` (8px) gaps.
- **Desktop (1280px+):** 12 columns, 24px gutters, 32px margins.
- **Tablet (768px - 1279px):** 8 columns, 16px gutters, 24px margins.
- **Mobile (<767px):** 4 columns, 16px gutters, 16px margins.

## Elevation & Depth
Depth is conveyed through **Tonal Layering** supplemented by **Ambient Shadows**. This design system avoids heavy drop shadows, opting for multi-layered, low-opacity blurs that mimic a natural light source.

- **Level 0 (Base):** The main background (`#f8fafc`).
- **Level 1 (Card/Container):** White background with a subtle 1px border (`#e2e8f0`) and a very soft "Resting" shadow (Y: 2px, B: 4px, Opacity: 0.05).
- **Level 2 (Hover/Active):** Slightly more pronounced shadow to indicate interactivity (Y: 4px, B: 12px, Opacity: 0.08).
- **Level 3 (Overlay/Modal):** High-diffusion shadow with a background backdrop-blur (12px) to focus user attention on the task at hand.

## Shapes
The shape language is consistently **Rounded**, using a 0.5rem (8px) base radius for standard components like inputs and buttons. For larger containers and cards, we use `rounded-lg` (16px) to soften the enterprise environment. 

Interactive elements like Checkboxes use a smaller 4px radius to maintain a crisp look, while decorative elements or tags may use pill-shaping (infinite radius) to distinguish them from functional UI buttons.

## Components
- **Buttons:** Primary buttons are solid Teal with white text, using a subtle inner-glow for a tactile feel. Secondary buttons use a ghost style with a 1px slate-200 border.
- **Input Fields:** Use a white fill with a 1px `#e2e8f0` border. On focus, the border transitions to Teal with a 3px soft Teal outer glow (ring).
- **Cards:** The workhorse of the design system. Cards should have no visible borders on Level 0 backgrounds, relying on Level 1 shadows for definition. Card headers should be separated by a subtle 1px horizontal rule.
- **Tables:** Designed for high-density data. No vertical borders. Zebra striping is avoided in favor of a subtle hover-state background change (`#f1f5f9`). Headers are `label-sm` style with subtle sorting icons.
- **Chips/Badges:** Small, low-saturation backgrounds with high-saturation text of the same hue (e.g., Soft Green background with Deep Green text for "Confirmed").
- **Linear Icons:** Use 2px stroke weight for all icons. Icons should always be accompanied by labels in primary navigation to ensure clarity.