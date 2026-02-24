# Beeswax Pat — Website Project

## Project Info
- **Domain:** beeswaxpat.com
- **Deployed at:** Render (static site) → GitHub repo: beeswaxpat-com
- **Render URL:** (update after first deploy)
- **Stack:** Static HTML/CSS/JS — no build step, no framework

## Contact & Business
- **Email:** beeswaxpat@gmail.com
- **Product:** Golden Sanctuary Beeswax Candle — 11 oz, $28
- **Made in:** Severn, Maryland
- **Tagline:** "Pure Light, Honestly Made"

## Images
All images in `/images/` — originals at `C:\Users\pscol\Desktop\Beeswax Pat\`
- `hero-candle.jpeg` — lit candle hero shot (GloriaPics)
- `product-main.jpeg` — unlit with bamboo lid (GloriaPics BeeswaxCandle1)
- `product-secondary.jpeg` — slightly wider angle (GloriaPics BeeswaxCandle2)
- `product-lifestyle.jpg` — outdoor marble table shot (New Label Pics 1000014001)
- `beeswax-melting.jpg` — process/Our Story shot (New Label Pics)
- `logo.avif` — brand logo (add PNG fallback if Safari issues arise)

## Stripe Setup (buy buttons)
1. Go to Stripe Dashboard → Products → Create product (Golden Sanctuary, $28)
2. Create a Payment Link for the product
3. Click "Buy Button" tab → configure → copy embed code
4. In index.html and funnel.html, find `<!-- STRIPE BUY BUTTON -->` comments and replace placeholder with embed code
5. For bundles: create additional Payment Links at bundle prices, repeat above

## Formspree Setup (email capture)
1. Go to formspree.io → create free account → New Form
2. Copy the form endpoint (e.g. `https://formspree.io/f/xabcdefg`)
3. In index.html, find `YOUR_FORMSPREE_ID` and replace with your form ID

## DNS — Pointing beeswaxpat.com to Render
Domain is at Hostinger (hpanel.hostinger.com → Domains → Domain portfolio).
1. In Render: Site Settings → Custom Domains → add beeswaxpat.com + www.beeswaxpat.com
2. Render gives you a CNAME value (e.g. beeswaxpat.onrender.com) and A record IP
3. In Hostinger: click ⋮ next to beeswaxpat.com → Edit DNS zone
4. Delete existing A records pointing to Hostinger
5. Add: CNAME www → [Render CNAME value]
6. Add: A @ → [Render IP — typically 216.24.57.1]
7. Save — propagation usually under 1 hour. SSL auto-provisioned by Render.

## Deploy Workflow
```
git add .
git commit -m "update"
git push origin main
```
Render auto-deploys on push. No build command, publish directory is `.`

## Messaging Rules (permanent)
ALLOWED: purity, burn time, soot levels, no synthetics, American-sourced, hand-poured, father & son, natural honey scent
BANNED: "purifies air", "negative ions", "neutralizes allergens" — no health claims of any kind

## Blog Posts
5 posts in `/blog/` folder:
- `beeswax-vs-paraffin-vs-soy.html`
- `most-beeswax-candles-arent-pure.html`
- `how-long-does-beeswax-candle-burn.html`
- `what-does-beeswax-smell-like.html`
- `american-vs-imported-beeswax.html`
