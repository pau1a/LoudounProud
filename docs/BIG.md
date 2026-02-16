# Compressed Brand Identity Foundation

**For a dual-town regional publication covering Ayr and Kilmarnock**

This is intentionally tight. Enough structure to create authority, not so much that it slows execution.

---

# 1. Brand Positioning (Non-Negotiable)

**You are not a fan site.**
You are regional infrastructure.

Design must communicate:

* editorial seriousness
* geographic ownership
* continuity
* commercial viability

Avoid anything that feels supporter-made.

Working mental model:

> Build it so a bank would be comfortable advertising on it.

---

# 2. Colour System (Exact, Deployable)

## Core Palette (90% of UI)

| Role               | Colour     | HEX       | Usage       |
| ------------------ | ---------- | --------- | ----------- |
| Primary background | Soft white | `#FAFAFA` | Page canvas |
| Primary text       | Graphite   | `#1C1F24` | Body text   |
| Secondary text     | Slate      | `#4B5563` | Metadata    |
| Dividers           | Mist grey  | `#E5E7EB` | Borders     |
| Panels             | Cold grey  | `#F3F4F6` | Cards       |

**Effect:** quiet authority.

---

## Club Signal Colours (Use Sparingly)

| Club                  | Colour     | HEX       | Rule             |
| --------------------- | ---------- | --------- | ---------------- |
| Kilmarnock            | Royal blue | `#0057B8` | Tags, scorelines |
| Ayr                   | True black | `#000000` | Tags only        |
| Optional Ayr heritage | Muted gold | `#C7A646` | Rare highlight   |

### Hard Rule:

**Accent colours must never exceed ~8–10% of any viewport.**

Colour is signalling, not wallpaper.

---

# 3. Typography (High Signal Choice)

Do not experiment here. Pick proven editorial faces.

## Recommended Pairing (Extremely Safe)

**Headings:**
👉 `Source Serif 4`

* intellectual
* newspaper-adjacent
* calm authority

**Body:**
👉 `Inter`

* highly readable
* modern
* exceptional on mobile

This pairing is widely used in serious digital publications for a reason.

---

# 4. Layout Philosophy

## Density Level: Medium-Airy

Avoid:

* cramped local-paper look
* oversized lifestyle-magazine padding

Target:

> structured calm

### Spacing Scale (use consistently)

```
4px   micro
8px   tight
16px  base
24px  breathing
32px  section
48–64px hero separation
```

Consistency here quietly signals professionalism.

Most amateur sites fail on spacing.

---

# 5. Header Strategy (Important)

Do **not** colour the header blue or black.

Use:

**White header + graphite text**

Optional:

* thin graphite underline
* or subtle shadow

Result: resembles national press rather than supporter media.

---

# 6. Tagging System (Where Club Colours Live)

Example behaviour:

* Blue pill → Kilmarnock
* Black pill → Ayr
* Grey pill → General / civic

Readers subconsciously learn the system within minutes.

This is how serious publications encode information.

---

# 7. Logo Direction (Do Not Overbuild)

Characteristics:

* wordmark first
* symbol optional later
* avoid shields, balls, crests

You are building a media asset, not a team.

### Strong stylistic direction:

Upper/lowercase hybrid.

Example feel (not literal):

> LoudounProud
> Ayrshire Ledger
> WestSound

Clean. Geographical. Durable.

---

# 8. Image Treatment

Apply a very light editorial discipline:

* slightly desaturate overly vivid photos
* avoid heavy filters
* prefer natural contrast

Creates visual cohesion across mixed sources.

---

# 9. What To Avoid (Critical)

Do **not**:

* split pages by club colour
* run gradients
* use sports-app neon palettes
* over-animate
* deploy carousels everywhere

Motion should be rare.

Stillness reads as confidence.

---

# 10. Monetisation Readiness Signal

Design for advertisers from day one.

Reserve:

* clean sidebar zones
* inline ad rhythm
* sponsor banner slots

If ads feel bolted on later, the site instantly looks small.

Infrastructure sites plan for revenue early.

---

# 11. Fast Implementation Stack (Pragmatic)

Given you are using Django:

* Define colours as SCSS variables immediately.
* Create utility classes for tag colours.
* Lock typography into base template.
* Build one reusable card component.
* Never allow rogue styling in templates.

Control is brand.

