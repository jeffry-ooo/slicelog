# Pizzalog

A personal pizza tracking log. Static site built with Astro, deployed to GitHub Pages.

## Stack

- [Astro](https://astro.build) — static site generator
- GitHub Pages — hosting
- GitHub Actions — auto-deploy on push
- Plain JSON files — one per pizza session

## Structure

```
pizzas/          # one JSON file per pizza, named YYYYMMDD.json
places.json      # known pizza places lookup
scripts/         # CLI tools
src/pages/       # Astro pages
```

## Adding a pizza

**From the terminal:**
```bash
python scripts/add_pizza.py
```

**On mobile:** edit or add a JSON file directly via the GitHub app, push triggers a rebuild.

## Pizza JSON schema

```json
{
  "name": "Margherita",
  "place": "da-luca",
  "service": "eat-in",
  "type": "rossa",
  "stars": 4,
  "notes": "Optional notes."
}
```

- `place` — references an `id` in `places.json`
- `service` — `eat-in` | `delivery` | `take-away`
- `type` — `rossa` | `bianca` | `well-done`
- `stars` — 1–5

## Themes

- **Bianca** — green on cream
- **Margherita** — cream on red
- **Well done** — grey on black

## Dev

```bash
npm install
npm run dev
```
