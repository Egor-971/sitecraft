# Sitecraft QA

Apply to changed pages and core journeys. Keep checks proportionate: one spacing fix does not require a large suite. Substantial creation/redesign requires running and visually inspecting the result. A screenshot-only audit reports only available image evidence and its limits.

## Baseline

- Define acceptance criteria: clear purpose, functional main action, preserved important data, accessible mobile navigation, no overlap or repetitive decoration under [design rules](design-rules.md).
- Before redesign, record routes, forms, links, integrations and states. Preserve useful baseline screenshots when allowed. Keep personal data out of public evidence.

## Run and inspect

1. Use the project's actual commands for required dependencies, build/types and server. Do not invent a successful command result.
2. Complete the primary journey in a browser. Examples: extension features → authorized install destination; service/provider → inquiry; shop search/filter → product → cart/checkout within scope. Do not make real payments merely for QA.
3. Test changed states: menu, filters, hover/focus, invalid input, success, loading/error and empty result. Check Tab, Enter and Escape where applicable, accessible names, visible focus and semantics. After rerendering or removing a control, retain logical keyboard focus rather than losing it to the document body.
4. Start with 390 px narrow and 1440 px wide when unspecified, adding other widths for complex layouts. Record the actual CSS viewport, not only the requested override. A sized iframe can test responsive CSS when browser resizing is unavailable; identify that method and do not call it a physical device test.
5. Capture and actually view first screens and affected sections/states. Inspect clipping, wrapping, density, demonstration size, alignment, empty space, repetitive panels and hierarchy. Unviewed captures are not visual QA.
6. Check that fixed navigation, cookie notices, chats and contact controls do not cover text, fields or actions. Inspect unintended document overflow, enlarged text and zoom.
7. Check actual font loading/weights, language coverage, computed contrast, missing-image behavior and reduced motion. Critical content cannot depend on animation.
8. Inspect Console and request errors within the tested path. Fix errors introduced by the change. Do not hide third-party blockers or claim an integration works because a local mock succeeded.
9. Fix material findings and retest affected paths. Do not repeat passed checks without changes or unresolved concerns.

## Product checks

Use the applicable [profile](product-patterns.md) and [product workflow](product-workflow.md). Test the entire scoped journey, not screen existence. Promotion and the application have different readiness criteria.

- Commerce/marketplaces: search/filter → item → size/color or seller offer → cart → authorized checkout. Check stock, quantity/caps, totals, removal, empty cart, persistence and changed price/stock. Separate seller permissions. A mock does not validate payments.
- Communication: new dialog/post → input → send → observable response/state → history. Check reopen, draft, cancellation, failure and duplicates. A local message array does not prove multi-user realtime or real AI inference.
- Learning: choose → lesson/task → attempt → feedback → progress after refresh. Algorithms need differing solutions and execution errors; hardcoded "Accepted" is not a judge. Tutor inquiries need format/time, validation and an observable request with double-booking behavior appropriate to their mode. Preserve selected slots when restoring drafts or editing a prior inquiry. Numeric day, weekday, label and stored timestamp must agree in the intended timezone; test another client timezone when dates cross boundaries.
- Music/film: catalog → detail → licensed actual media → play/pause/seek → queue/resume. Check one active player, ending, resource failure, audio and captions. Covers or animated progress do not prove playback; autoplay/fullscreen can depend on the browser.
- Documents/diaries/boards: open → edit → save → refresh/return → recover. Check roles, undo/redo, coordinates after zoom/pan and accessible drag alternatives as applicable. A local document does not establish collaboration.
- Translation/asynchronous search: fast new input, parameter changes, empty input, delay/error and stale-response prevention. Delivery needs addresses, selected method, calculation and the actual-order boundary; courier recruitment needs its own inquiry path.
- Financial UI: accurate sums, request status, repeated submission, recovery and server permissions within scope. Do not perform real transfers for testing. Frontend does not supply banking infrastructure.

Extend for new niches. Choose meaningful tests for persistence, permissions, stale responses or duplicate submissions when those risks change. A spacing fix does not need them. Distinguish verified functionality, external blockers, local/demo mode and connected service behavior.

## Professional-stage checks

Apply only to relevant changes; do not require a carousel or animation on every site.

- Review the system across scoped pages/states: type, colors, components, spacing, behavior and mobile layouts. Compare actual reference qualities, such as product legibility, rhythm and clear actions. Identify and repair material weaknesses.
- View motion in the browser: start/end, rapid repeat input, forward/back scroll and mid-page reload. No hidden content, lost focus, blocked actions or final-state errors.
- Enable reduced motion using available tools and verify equivalent content/actions. Check without JavaScript when new motion could hide content, without promising an entire app works without JavaScript unless the stack supports it.
- For horizontal collections, check beginning/middle/end, next item, buttons and available keyboard/touch controls. Avoid drag-only control, focus traps and page overflow. Record real-touch limits.
- For vertical narratives, check native scroll, anchors, sticky exit, narrow layout and reachable actions. Route transitions need URL, history, Back/Forward, focus and direct links. Do not intercept the wheel for decoration.
- Interactive demonstrations must be useful and honest about scope. Hover needs keyboard/touch alternatives. Consider error/loading/empty states, controllable automatic motion and unexpected audio.
- Inspect primary material loading, layout shifts, responsiveness and repeated open/close. Record measurement conditions; local observations are not universal performance claims.

## Evidence

For substantial work, record in the project's `docs/design/SITECRAFT.md`: goal and acceptance criteria; version/state and actual launch commands; pages, actual viewports, inputs/results; viewed screenshot paths; defects, fixes and retests; static/browser/mock verification and untested limits; references, fonts and asset licenses. For an additional stage, include the concrete direction, authorization/scope, system/components and observed motion/scroll/reduced-motion behavior.

Do not claim complete accessibility from one contrast measurement, functionality from an image, conversion growth from appearance, or undetectable AI authorship. If browser tooling is unavailable, complete available static checks and state the runtime/visual limit. With browser access, a build alone does not finish substantial redesign.
