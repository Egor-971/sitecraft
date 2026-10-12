# Official guidance and its use in Sitecraft

Reviewed October 12, 2026. These are original summaries of primary sources, not copied third-party skills, certification or endorsement. Consult for a substantial new direction or a concrete uncertainty; ordinary work uses [first delivery](first-delivery.md) and [design rules](design-rules.md).

## Anthropic

The official [frontend-design skill](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md) connects identity to subject, audience and content. Typography and structure express information; arbitrary eyebrows, repeated effects and interchangeable presets weaken the result. Check the plan against the brief before implementation, then critically inspect the built interface. Existing client preferences take priority.

Sitecraft applies this through task-specific composition/type, a direction check before code and visual QA before delivery. Cards, dark backgrounds and serif type are not inherently forbidden: explain why they fit this product. Anthropic's skill is not redistributed in this package.

## OpenAI

[Frontend prompt instructions](https://developers.openai.com/api/docs/guides/frontend-prompt) emphasize audience and domain, organized density for working tools, useful controls/navigation, text appropriate to containers, real content/images, stable layouts and desktop/mobile inspection. The source describes GPT-5.5 instructions; it is not a promise about every model.

Sitecraft adapts these principles to the actual brief. A particular radius, library or hero layout does not become one preset for banks, boards, shops and brand sites. Preserve the existing system and explicit user requirements. A tool does not need a marketing hero.

[Rethinking skills and prompts](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) recommends precise concise descriptions, progressive reference access and fewer unnecessary universal procedures. Entry points explain workflow selection and boundaries, while sector details remain references. The plugin does not switch model or reasoning settings.

## Google / web.dev

[Responsive design](https://web.dev/learn/design/), [typography](https://web.dev/learn/design/typography) and [accessibility](https://web.dev/learn/design/accessibility) connect adaptation with legibility, languages and input methods. Check real copy, line length, wrapping, scale, keyboard/touch access and reachable actions. Two viewports do not cover every device or constitute a full accessibility audit.

[Core Web Vitals](https://web.dev/articles/vitals) measure loading, responsiveness and stability. Good-experience thresholds are LCP ≤2.5 s, INP ≤200 ms and CLS ≤0.1 at the 75th percentile, separating mobile and desktop. When materials/performance materially change, measure with available tools and record conditions. A local measurement or Lighthouse run is not field evidence. Without measurements, do not claim these thresholds passed.

## Priority and limits

Resolve recommendations by purpose and context. A full-screen photo can support product promotion while obstructing a learning workspace. A useful product card differs from a decorative panel around every paragraph. The explicit request, chosen stack and useful functionality take priority over generic styling rules.

Here, reducing "AI-looking" output means reducing automatic template choices. These sources supply neither an authorship classifier nor a guarantee of a perfect first attempt. Evaluate new implementations by their own journeys and observable qualities, not brand-level claims.
