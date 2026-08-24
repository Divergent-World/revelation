# Revelation Print Edition, Remix, and Homepage Hero

## Goal

Give the 182-page collector's print edition and the project's open-source materials distinct homes while simplifying the homepage. The result should feel like an editorial art-book presentation rather than a checkout flow or an aggressive sales funnel.

The canonical project title is **Revelation**, singular. No tracked project content should use a pluralized form of the title.

## Information architecture

The global navigation becomes:

1. **Movements** — the existing movement reader.
2. **Read** — the existing Revelation text.
3. **Print Edition** — a new internal route at `/print-edition/`.
4. **Remix** — a new internal route at `/remix/`.

The current external **Source** navigation item is removed. GitHub and archive access move to the Remix page.

The existing archive, print preview, source, export summary, and compatibility-download block is removed completely from the homepage. The homepage points visitors toward the three distinct experiences through the global navigation: explore the images, read the text, or learn about the physical edition and remixable source.

## Homepage hero carousel

The first homepage artwork becomes a six-slide carousel. It uses one existing canonical scene from each movement to show the project's narrative and visual range:

1. `T1-B04` — Fourth Horseman
2. `T2-B03` — Fifth Trumpet: Locusts come up from the pit
3. `T3-T07` — Woman and the dragon
4. `T4-B04` — Last Harvest
5. `T5-B02` — Whore of Babylon seated on the beast
6. `T6-B03` — New Jerusalem

The first slide replaces the current static `T6-B03` feature, while the existing hero introduction, primary actions, and project facts remain.

### Carousel behavior

- Advance every eight seconds with a gentle crossfade.
- Provide previous and next buttons plus six position indicators.
- Expose the active slide and controls to assistive technology with meaningful labels.
- Pause automatic rotation while the carousel is hovered, keyboard-focused, or manually controlled.
- Restart the interval only after interaction ends; never stack multiple timers.
- When `prefers-reduced-motion: reduce` is active, do not auto-rotate or animate. Keep manual controls available.
- Preserve the existing responsive hero proportions and prevent captions or controls from obscuring the artwork.
- Use the existing artwork delivery and `ArtworkImage` conventions. Do not add a carousel dependency.

Only the timer, pause state, and active slide require a client component. The homepage itself remains server-rendered and passes the six resolved scenes to that component.

## Print Edition page

`/print-edition/` is a restrained editorial landing page for the physical collector's edition. It has no cart, checkout, lead-capture form, or displayed price. Blurb remains the source of truth for availability and current pricing.

### Page sequence

1. **Edition hero**
   - Lead with a canonical source artwork in the site's black-and-gold presentation.
   - Identify the work as *Revelation: An Illuminated Prophecy* by Ali Rahman.
   - State that this is the 182-page collector's print edition.
   - Include a restrained **View on Blurb** outbound action.

2. **Editorial introduction**
   - Explain that the project rebuilds all ninety Apocalypse tapestry compartments in their original order.
   - Preserve the existing factual distinction among surviving, fragmentary, and reconstructed scenes.
   - Describe the print edition without conventional urgency, scarcity, testimonials, or sales language.

3. **Artwork sequence**
   - Show a small curated set of canonical source artworks using the existing scene data and artwork delivery system.
   - Use the book's visual language around them: monumental landscape images, warm ivory space, serif captions, and restrained gold/red accents.
   - Caption them as artworks from the project and edition rather than implying they are photographs of the physical book.
   - Keep the layout ready for future book photography to replace or supplement the artwork without restructuring the page.

4. **Edition details**
   - 182 pages
   - Hardcover, ImageWrap
   - Large-format landscape
   - 13 × 11 in / 33 × 28 cm
   - Ninety illuminated compartments across six movements and twenty-two chapters

5. **Blurb preview**
   - Keep the existing Blurb preview capability on this page.
   - Constrain the iframe to a responsive 4:3 frame with a sensible maximum width so it does not dominate the page.
   - Give it an accessible title and lazy loading.

6. **Closing action**
   - Repeat a quiet **View on Blurb** link.
   - Do not mention Amazon until a real listing URL exists.

The page uses black and gold around the edition hero, warm ivory editorial sections for the artwork sequence, and the site's existing type and button system. It should resemble a museum catalogue or art-book colophon, not a generic ecommerce product page.

## Remix page

`/remix/` is the open-source companion and the sole home for project download/export information.

### Page sequence

1. **Open-source statement**
   - Explain that the project is intended to be studied, rebuilt, and remixed.
   - Do not claim permissions beyond the repository's actual license and terms.

2. **Archive contents**
   - Describe the self-contained master archive: the official 182-page book, fixed and reflowable EPUB editions, editable DOCX, all ninety artworks, canonical content, portable InDesign sources, fonts, and rebuild instructions.
   - Retain the archive size and compatibility information when accurate after the singular-name rebuild.
   - Keep the standalone scripture manuscript download available as a smaller compatibility option.

3. **Primary actions**
   - **Download Master Archive** links directly to the singularly named published archive for now.
   - **View Source on GitHub** links to `https://github.com/Divergent-World/Revelation`.
   - Render the two actions as separate, consistently sized buttons with clear focus states.

Email-list gating is explicitly deferred until a provider and signup flow are chosen. The archive action should remain isolated enough that its destination can later change to a signup route without restructuring this page.

## Canonical singular-name migration

Every tracked plural project-name occurrence must become singular, including:

- Visible site copy, wordmark, accessibility labels, and page metadata.
- Repository URLs and deployment documentation.
- Package name and lockfile package name.
- Archive, DOCX, EPUB, PDF, and generated-build filenames.
- Release scripts, validation scripts, checksums, tests, and expected paths.
- R2 bucket examples, object keys, environment examples, and archive URLs.
- Contribution and publishing documentation.
- Historical design and implementation documents where the plural term names this project or one of its artifacts.

The local checkout has already been renamed externally to `/Users/alirahman/Desktop/test/Revelation`. That filesystem move is not performed by application code.

There will be no runtime fallback to plural storage keys. Before production deployment, the newly singular master archive must be built and uploaded to the singular configured bucket/key. This prevents the old title from remaining part of the public project contract.

## Data and implementation boundaries

- Reuse the existing content module and artwork delivery for scene lookup, Print Edition imagery, Blurb URLs, repository URL, edition facts, and archive URL.
- Keep the carousel's six scene IDs in one explicit ordered constant rather than introducing a new content schema.
- Use one small client carousel component; the new pages otherwise remain server components.
- Use existing CSS modules and global tokens. Add no UI, animation, or carousel dependency.
- Add route-specific metadata using **Revelation**, singular.
- The Blurb product page and preview are outbound/embedded destinations only; no purchase state or API integration is required.
- No email provider, form backend, analytics funnel, Amazon integration, inventory, or checkout is part of this change.

## Accessibility and responsive behavior

- All carousel controls must be reachable and operable by keyboard.
- Controls and iframe require meaningful accessible names.
- Focus indicators must remain visible on dark and ivory backgrounds.
- Auto-rotation pauses on hover and focus, and is disabled for reduced motion.
- Artwork captions remain available as text rather than being baked into images.
- Buttons wrap cleanly without unequal accidental heights.
- The print preview and gallery must not overflow narrow viewports.
- Decorative imagery should not create repeated or misleading screen-reader output.

## Verification

### Automated checks

- Update navigation tests for **Print Edition** and **Remix**, and remove the old external **Source** expectation.
- Verify the homepage no longer contains the archive/export block.
- Verify the carousel renders all six selected scenes and exposes usable controls.
- Test timed advancement, pause behavior, manual navigation, and reduced-motion behavior with controlled timers or the smallest reliable browser-level check.
- Verify `/print-edition/` and `/remix/` render successfully with route-specific metadata.
- Verify Blurb, GitHub, archive, and standalone manuscript destinations.
- Update release/export tests and expected filenames to singular naming.
- Run a repository-wide, case-insensitive plural-name audit over tracked files, with only genuinely unrelated English uses allowed. Project-name, repository, artifact, and storage references must have zero plural matches.
- Run the existing unit tests, lint, and production build.

### Browser checks

- Desktop and narrow mobile homepage carousel geometry.
- Visible carousel focus states and manual controls.
- Reduced-motion behavior.
- Print Edition hero artwork, artwork gallery, specifications, iframe proportions, and outbound actions.
- Remix archive copy, button sizing, and mobile wrapping.
- Global navigation at desktop and mobile widths.

## Operational note

Application changes can rename archive generation and references, but they do not by themselves move already-published R2 objects. The singular archive must be uploaded before deploying the site change, or the new download link will not resolve. This is a release prerequisite rather than a reason to retain the old plural URL.

## Non-goals

- Checkout, cart, payments, or a first-party purchase flow.
- Displaying or synchronizing the Blurb price.
- An Amazon link before a listing exists.
- Email capture or forced signup.
- A new license or permissions policy.
- A new CMS, gallery system, or animation dependency.
- Redesigning the movement reader or Revelation text reader.
