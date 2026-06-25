# UI Prototype

Use this branch to generate several structurally different UI variations on a
single route or host page. The user compares variants, chooses one, and the rest
are deleted.

If the question is about logic, state, or data shape, use `LOGIC.md` instead.

## Good fit

- "What should this page look like?"
- "Show a few options for the overview page before committing."
- "Try different layouts for the resources index."
- "Explore alternative ways to explain a complex project concept."

## Two shapes

### Shape A: adjustment to an existing page, preferred

Use an existing route when possible. Variants should render on the same route,
controlled by a `?variant=` URL search parameter. Keep existing data, imports,
route structure, and source notices intact; only the rendered subtree changes.

If the prototype is for a new section that would naturally live inside an
existing page, mount the variants inside that page.

### Shape B: new throwaway page, last resort

Create a clearly named prototype route only when there is no sensible host page.
Follow the repo's Astro routing convention, and include `prototype` in the path
or filename.

Before using this shape, check whether an existing page would expose more useful
constraints.

## Process

### 1. State the question and variant count

Default to three variants. More than five usually adds noise.

Write a one-line plan near the prototype:

```text
Three variants of the project overview page, switchable via ?variant= on /project/overview/.
```

### 2. Generate meaningfully different variants

Each variant should differ in structure, information hierarchy, and primary
affordance. Do not produce three slight color or copy changes.

Hold every variant to:

- the page purpose;
- available source-backed content;
- existing Astro, CSS, and component conventions;
- the Source Authority Boundary.

Use clear component names such as `VariantA`, `VariantB`, and `VariantC`.

### 3. Wire variants together

Use the framework's routing and URL APIs. In Astro, read the variant from
`Astro.url.searchParams` when static generation permits the route to render the
same page for all query values.

The switcher shape:

```tsx
const variant = searchParams.get("variant") ?? "A";

return (
  <>
    {variant === "A" && <VariantA {...data} />}
    {variant === "B" && <VariantB {...data} />}
    {variant === "C" && <VariantC {...data} />}
    <PrototypeSwitcher variants={["A", "B", "C"]} current={variant} />
  </>
);
```

Adapt the sketch to Astro rather than adding React unless the project already
uses React for that surface.

### 4. Build the floating switcher

The switcher should sit fixed at the bottom center of the viewport and include:

- previous variant button;
- current variant label;
- next variant button.

Behavior:

- Clicking changes the `variant` URL search parameter.
- Left and right arrow keys cycle variants.
- Do not intercept arrow keys while an input, textarea, or editable element is
  focused.
- Make the switcher visually distinct from the design being evaluated.
- Do not leave the switcher in production-bound output.

### 5. Hand it over

Surface the URL and variant keys. The useful feedback is often compositional:
"use the header from B with the resource grouping from C."

### 6. Capture the answer and clean up

Once a variant wins, write down which one and why. Then:

- For Shape A, delete losing variants and the switcher, then fold the winner
  into the existing page.
- For Shape B, promote the winner to a real route, then delete the throwaway
  route and switcher.

## Anti-patterns

- Variants that differ only in color or copy.
- Excessively shared layout code between variants.
- Wiring variants to real mutations.
- Promoting the prototype directly to production without rewriting it to normal
  project quality standards.
