---
name: Agro Harvest Modernist
colors:
  surface: '#faf9f6'
  surface-dim: '#dadad7'
  surface-bright: '#faf9f6'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f4f4f0'
  surface-container: '#eeeeea'
  surface-container-high: '#e8e8e5'
  surface-container-highest: '#e2e3df'
  on-surface: '#1a1c1a'
  on-surface-variant: '#404941'
  inverse-surface: '#2f312f'
  inverse-on-surface: '#f1f1ed'
  outline: '#707970'
  outline-variant: '#c0c9be'
  surface-tint: '#2a6a3f'
  primary: '#003215'
  on-primary: '#ffffff'
  primary-container: '#004b23'
  on-primary-container: '#79bb87'
  inverse-primary: '#93d6a0'
  secondary: '#006d2f'
  on-secondary: '#ffffff'
  secondary-container: '#5dfd8a'
  on-secondary-container: '#007232'
  tertiary: '#292b2b'
  on-tertiary: '#ffffff'
  tertiary-container: '#3f4141'
  on-tertiary-container: '#acadad'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#aef2bb'
  primary-fixed-dim: '#93d6a0'
  on-primary-fixed: '#00210c'
  on-primary-fixed-variant: '#0b5229'
  secondary-fixed: '#66ff8e'
  secondary-fixed-dim: '#3de273'
  on-secondary-fixed: '#002109'
  on-secondary-fixed-variant: '#005322'
  tertiary-fixed: '#e2e2e2'
  tertiary-fixed-dim: '#c6c6c7'
  on-tertiary-fixed: '#1a1c1c'
  on-tertiary-fixed-variant: '#454747'
  background: '#faf9f6'
  on-background: '#1a1c1a'
  surface-variant: '#e2e3df'
  harvest-lime: '#25D366'
  deep-forest: '#004B23'
  field-gray: '#F4F4F4'
  surface-white: '#FFFFFF'
typography:
  display-lg:
    fontFamily: Hanken Grotesk
    fontSize: 72px
    fontWeight: '800'
    lineHeight: 80px
    letterSpacing: -0.04em
  display-lg-mobile:
    fontFamily: Hanken Grotesk
    fontSize: 48px
    fontWeight: '800'
    lineHeight: 52px
    letterSpacing: -0.03em
  headline-lg:
    fontFamily: Hanken Grotesk
    fontSize: 40px
    fontWeight: '700'
    lineHeight: 48px
  headline-md:
    fontFamily: Hanken Grotesk
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
  body-lg:
    fontFamily: Hanken Grotesk
    fontSize: 20px
    fontWeight: '400'
    lineHeight: 32px
  body-md:
    fontFamily: Hanken Grotesk
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-caps:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.1em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  base: 8px
  container-max: 1280px
  gutter: 24px
  margin-desktop: 64px
  margin-mobile: 20px
---

## Brand & Style

The design system is engineered for a high-stakes agricultural event, balancing the raw vitality of the harvest with the precision of modern industrial standards. The brand personality is **authoritative, industrious, and innovative**, aimed at stakeholders, producers, and government officials in the sugarcane sector.

The visual style is **Corporate Modern with a touch of Agricultural Brutalism**. It utilizes expansive white space to denote professionalism, punctuated by high-contrast accents of lime green to represent growth and energy. The aesthetic avoids rural cliches in favor of a clean, systematic look that suggests efficiency and technological advancement. Visual interest is generated through large-scale typography, grid-based layouts, and subtle organic patterns derived from sugarcane silhouettes.

## Colors

This color palette is anchored by **Deep Forest Green**, providing a foundation of stability and institutional trust. **Harvest Lime** serves as the primary action color, used for critical CTAs and to draw attention to growth-related data. 

**Field Gray** is used for secondary backgrounds and subtle sectioning to prevent the interface from feeling overly sterile. Text should primarily utilize the **Neutral Black** for maximum legibility against light surfaces, while white is reserved for high-contrast "Dark Mode" sections or hero overlays where the deep green background is utilized.

## Typography

The typography system relies on **Hanken Grotesk** for its sharp, contemporary geometry, which conveys a sense of engineering and precision. Display sizes use heavy weights and tight letter spacing to create high-impact, editorial-style headings that feel official and bold.

To introduce a technical, "modern agriculture" feel, **JetBrains Mono** is used for labels, data points, and small metadata. This monospaced font suggests data-driven farming and industrial logistics. For mobile devices, display sizes are scaled down aggressively to ensure the "bold" personality remains without breaking the layout.

## Layout & Spacing

The layout follows a **Rigid 12-Column Fluid Grid** with generous margins to emphasize the premium, professional nature of the event. Content should be grouped into clear horizontal bands, using "Field Gray" to differentiate logical sections like "Schedule," "Speakers," and "Logistics."

Spacing is built on an **8px linear scale**. Use large vertical padding (80px - 120px) between major sections on desktop to maintain an airy, sophisticated feel. On mobile, the grid collapses to 1 column with a 20px safe-area margin, prioritizing vertical stacking and oversized touch targets.

## Elevation & Depth

This design system uses **Tonal Layering** instead of heavy shadows to maintain a clean, flat aesthetic. Elevation is communicated through:
- **Surface Contrast:** Elements "lift" off the page by moving from a white background to a Field Gray container.
- **Micro-Shadows:** Only used for interactive elements like cards and primary buttons to indicate clickability. These shadows are sharp and low-opacity (e.g., 4% alpha).
- **Glassmorphism (Limited):** Navigation bars use a high-blur backdrop filter (20px) with a semi-transparent white fill to maintain context of the background imagery while ensuring text legibility.

## Shapes

The shape language is **Soft (0.25rem)**, bordering on sharp. This decision reflects the industrial nature of agricultural machinery and structural steel. Fully rounded or pill-shaped elements should be avoided as they feel too "consumer-tech" for an official agricultural opening.

Containers and image frames should utilize the base `roundedness` for a subtle refinement, while primary buttons may use `rounded-lg` (0.5rem) to stand out as interactive components. High-impact imagery should be clipped with sharp or very slightly softened corners to maintain the professional tone.

## Components

### Buttons
- **Primary:** Deep Forest Green background with white text. High-contrast and bold.
- **Secondary:** Harvest Lime background with Deep Forest Green text. Used for "Register" or "Primary Action" within light sections.
- **Outline:** 2px solid border of Deep Forest Green.

### Input Fields
Fields should use a 1px border of Field Gray that transitions to Deep Forest Green on focus. Labels must always use the **JetBrains Mono** label style for a technical appearance.

### Cards
Cards use a white background with a very subtle 1px border (#E0E0E0). Avoid heavy shadows; instead, use a slight vertical offset (2px) on hover to indicate interactivity.

### Data Chips
Small, rectangular tags using Harvest Lime with a 10% opacity background and full-opacity text. These are used to categorize sessions (e.g., "Field Demo," "Keynote," "Logistics").

### Agricultural Elements
Incorporate thin vertical lines or subtle repeating patterns of "diagonal stalks" to serve as section dividers, subtly nodding to the sugarcane subject matter without using literal illustrations.