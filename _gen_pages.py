#!/usr/bin/env python3
"""Generate Nutrition Hub local-SEO landing pages (expansion set, 7/15/2026).

Ported from broadway-nutrition-landing/_gen_pages.py. Generates the NEW pages
only — the original 4 hand-built pages (energy-teas / meal-replacement-shakes /
b12-shots / protein-shakes) are left untouched. Also regenerates sitemap.xml
covering homepage + all landing pages + blog. Edit THIS script, never the HTML.

Deploy per repo docs: scp <slug>.html -> VPS /var/www/nutritionhub-home/<slug>/index.html
"""
import glob
import json
import os
import re

DOMAIN = "nutritionhub101.com"
PIXEL = "915336731481586"          # SACRED — live ads + CAPI depend on it
ADDR_STREET = "8201 Broadway, Suite 113"
ADDR_LOC = "Pearland"; ADDR_REG = "TX"; ADDR_ZIP = "77581"
LAT = 29.559174; LNG = -95.345263
PHONE_TEL = "+1-844-748-2536"
IG = "https://instagram.com/nutritionhub101"
ORDER = "https://order.nutritionhub101.com"
GH = "https://raw.githubusercontent.com/Ronnie-Nutrition/nutritionhub-landing/main"
# Same-origin image dir on the VPS (/var/www/nutritionhub-home/img/). Use this for
# NEW images: GH raw only serves the `main` branch, so anything added on an
# unmerged branch 404s there. Deploy with: scp img/*.jpg root@VPS:/var/www/nutritionhub-home/img/
IMGV = f"https://{DOMAIN}/img"
LOGO = "https://order.nutritionhub101.com/images/logo.png"
MAPS = "https://www.google.com/maps/dir/?api=1&destination=8201+Broadway+Suite+113+Pearland+TX+77581"

# Slugs of the original hand-built pages (kept in sitemap, not regenerated)
EXISTING_SLUGS = ["energy-teas-pearland", "meal-replacement-shakes-pearland",
                  "b12-shots-pearland", "protein-shakes-pearland"]

HOURS_ROWS = """<div class="hrow"><span class="d">Mon – Thu</span><span class="t">6:30 AM – 5:00 PM</span></div>
      <div class="hrow"><span class="d">Friday</span><span class="t">6:30 AM – 3:00 PM</span></div>
      <div class="hrow"><span class="d">Saturday</span><span class="t">8:00 AM – 2:00 PM</span></div>
      <div class="hrow"><span class="d">Sunday</span><span class="t">12:00 PM – 3:00 PM</span></div>"""
HOURS_SCHEMA = """[
    { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday"], "opens": "06:30", "closes": "17:00" },
    { "@type": "OpeningHoursSpecification", "dayOfWeek": "Friday", "opens": "06:30", "closes": "15:00" },
    { "@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "08:00", "closes": "14:00" },
    { "@type": "OpeningHoursSpecification", "dayOfWeek": "Sunday", "opens": "12:00", "closes": "15:00" }
  ]"""

def card(img, tag, name, desc, price):
    media = (f'<img src="{img}" alt="{name} in Pearland" loading="lazy">' if img
             else '<div class="emoji">🥤</div>')
    pr = f'<span class="price">{price}</span>' if price else ''
    return f"""    <div class="drink">
      {media}
      <span class="tag">{tag}</span>
      <h3>{name}</h3>
      <p>{desc}</p>
      {pr}
    </div>"""

def faq_blocks(faqs):
    jsonld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        for (q, a) in faqs]}
    visible = "\n".join(
        f'    <div class="qa">\n      <h3>{q}</h3>\n      <p>{a}</p>\n    </div>'
        for (q, a) in faqs)
    return json.dumps(jsonld, indent=2), visible

def ctas(label):
    return (f'<a class="btn btn-acc" href="{ORDER}" target="_blank" onclick="fbq(\'track\',\'Lead\')">{label}</a>\n'
            f'    <a class="btn btn-ghost" href="#more">See More</a>')

PAGES = []

# ================= PAGE 1: LOADED TEAS =================
# NOTE: energy-teas-pearland targets "energy tea / lit tea"; this page owns the
# national term "loaded tea" and cross-links there rather than repeating it.
PAGES.append(dict(
 slug="loaded-teas-pearland", acc="#a64dff", acc2="#23e0ff", accglow="rgba(166,77,255,.5)",
 title="Loaded Teas in Pearland, TX \u2014 12+ Flavors, $9.15",
 desc="32oz loaded teas made to order in Pearland. Order ahead for pickup at 8201 Broadway, Suite 113. Weekdays from 6:30 AM; see weekend hours below.",
 ogimg=f"{GH}/tea_dragon_juice.png",
 schema_desc="32oz fruit-flavored iced teas made fresh to order in Pearland, TX.",
 serves=["Loaded Teas", "Energy Teas", "Lit Teas", "Smoothies"],
 h1='<span class="a">Loaded Teas</span><br>in <span class="b">Pearland, TX</span>',
 hero_sub="32oz fruit-flavored iced teas, made fresh to order. Choose a flavor from the board or order ahead for pickup.",
 intro_h2='Pearland\'s spot for <span>loaded teas</span>',
 intro=f"""<p>Searching for <strong>loaded teas in Pearland</strong>? Nutrition Hub on Broadway makes them fresh all day — 32oz fruit-flavored iced teas made to order. Around here some folks call them <a href="/energy-teas-pearland/">energy teas or lit teas</a>; same great drink, 12+ rotating flavors on the board.</p>
    <p>Choose your flavor from the current board. For questions about ingredients, caffeine, or allergens, ask our team about the drink you plan to order.</p>
    <p>Hungry too? Pair it with a <a href="/meal-replacement-shakes-pearland/">meal replacement shake</a> or see the <a href="/">full menu</a>. You can <a href="{ORDER}" target="_blank" onclick="fbq('track','Lead')">order online</a> and skip the line.</p>""",
 grid_h2='Fan-favorite <span>loaded tea flavors</span>',
 grid_lead="A taste of the board — flavors rotate, so ask what's fresh today.",
 grid="\n".join([
  card(f"{GH}/tea_dragon_juice.png", "LOADED TEA", "Dragon Juice", "32oz · bold fruit flavor", "$9.15"),
  card(f"{GH}/tea_blue_margarita.png", "LOADED TEA", "Blue Margarita", "32oz · made to order", "$9.15"),
  card(f"{GH}/tea_red.png", "12+ FLAVORS", "Ask what's fresh", "Mamacita, Blue Ocean &amp; more — rotating board of fan favorites", "$9.15"),
 ]),
 why_h2='Why our <span>loaded teas</span> hit different',
 why=[("⚡", "Made <span>to order</span>", "Choose your flavor and ask our team about ingredients and caffeine before you order."),
      ("🍓", "12+ <span>flavors</span>", "Fruity, refreshing, made fresh to order. Want it lighter or stronger? Just say the word."),
      ("🌿", "Order <span>ahead</span>", "Browse the online menu and place your pickup order before you arrive.")],
 faqs=[
  ("What is a loaded tea?",
   "At Nutrition Hub in Pearland, a loaded tea is a 32oz fruit-flavored iced tea made fresh to order. Choose from the current flavor board and ask our team about the ingredients in your drink."),
  ("Are loaded teas the same as lit teas or energy teas?",
   "Yes — loaded tea, lit tea, and energy tea are different names for the same style of drink. Whatever you call it, ours is $9.15 for a 32oz, made fresh at 8201 Broadway, Suite 113 in Pearland."),
  ("How much do loaded teas cost in Pearland?",
   "Loaded teas at Nutrition Hub are $9.15 for a 32oz. Order online at order.nutritionhub101.com for pickup, or walk in at 8201 Broadway, Suite 113."),
  ("Where can I ask about ingredients, caffeine, or allergens?",
   "Ask the Nutrition Hub team about your chosen drink before ordering, including ingredients, caffeine, and allergens. Specify any additions or substitutions you want."),
  ("Where can I get a loaded tea near me in Pearland, TX?",
   "Nutrition Hub is at 8201 Broadway, Suite 113, Pearland, TX 77581 — open 7 days a week. Order online or walk in; first visit, ask for Ronnie."),
 ],
 cta_label="🍵 Order Your Tea",
 close_h2='Your first <span>loaded tea</span> is waiting.',
 close_p="Order online and skip the line, or walk in and ask what's fresh on the board.",
))

# ================= PAGE 2: PROTEIN COFFEE =================
PAGES.append(dict(
 slug="protein-coffee-pearland", acc="#d4a24e", acc2="#ff2e88", accglow="rgba(212,162,78,.5)",
 title="Protein Coffee in Pearland, TX | Nutrition Hub",
 desc="Protein coffee in Pearland, TX — real coffee blended with protein, $9.97, made fresh from 6:30 AM. Order online or walk in at 8201 Broadway, Suite 113.",
 ogimg=f"{GH}/shake_chocolate.png",
 schema_desc="Protein coffee in Pearland, TX — real coffee blended with protein, made fresh to order from 6:30 AM.",
 serves=["Coffee", "Protein Coffee", "Protein Shakes", "Smoothies"],
 h1='<span class="a">Protein Coffee</span><br>in <span class="b">Pearland, TX</span>',
 hero_sub="Real coffee blended with protein — the morning cup that actually keeps you full. Made fresh from 6:30 AM on weekdays.",
 intro_h2='Protein coffee in <span>Pearland</span>',
 intro=f"""<p>If you want your caffeine to do more than buzz, try <strong>protein coffee in Pearland</strong>. At Nutrition Hub on Broadway we blend real coffee with protein into a creamy, dessert-flavored shake — so your morning cup fuels you instead of crashing you at 10 AM.</p>
    <p>We open at 6:30 AM on weekdays, so it's an easy grab on the way to work or after an early workout. Three protein coffee flavors on the board, all made fresh to order.</p>
    <p>Not a coffee morning? Grab a <a href="/loaded-teas-pearland/">loaded tea</a> for clean energy, a <a href="/protein-shakes-pearland/">post-workout protein shake</a>, or see the <a href="/">full menu</a>. <a href="{ORDER}" target="_blank" onclick="fbq('track','Lead')">Order online</a> and skip the line.</p>""",
 grid_h2='Ways to get your <span>protein coffee</span>',
 grid_lead="Three flavors on the board, all blended fresh with real coffee and protein.",
 grid="\n".join([
  card(f"{GH}/shake_chocolate.png", "PROTEIN COFFEE", "Mocha", "Real coffee + chocolate + protein", "$9.97"),
  card(None, "PROTEIN COFFEE", "Caramel Macchiato", "Sweet, creamy, coffee-forward", "$9.97"),
  card(None, "PROTEIN COFFEE", "House Blend", "Smooth &amp; clean classic", "$9.97"),
 ]),
 why_h2='Why <span>protein coffee</span>',
 why=[("☕", "Coffee <span>+ protein</span>", "Your caffeine comes with real fuel — a filling blend that carries you to lunch."),
      ("🍨", "Dessert <span>flavors</span>", "Mocha, caramel, vanilla — tastes like a coffee-shop treat without the sugar bomb."),
      ("🌅", "Open <span>early</span>", "We're blending from 6:30 AM on weekdays — grab it on your way in.")],
 faqs=[
  ("What is protein coffee?",
   "Protein coffee is real coffee blended with protein into a creamy shake — you get your caffeine plus protein that keeps you full, without the sugar crash of a sweetened latte. Nutrition Hub in Pearland makes it fresh to order."),
  ("How much does protein coffee cost in Pearland?",
   "Protein coffee at Nutrition Hub is $9.97, made fresh to order. Order online at order.nutritionhub101.com or walk in at 8201 Broadway, Suite 113."),
  ("What flavors of protein coffee do you have?",
   "We keep three protein coffee flavors on the board — ask what's fresh when you order. Mocha is the fan favorite."),
  ("Can protein coffee replace my breakfast?",
   "A lot of our regulars use it that way — coffee and protein in one cup is a quick, filling start. If you want a fuller breakfast, pair it with a meal replacement shake or add a boost."),
  ("Where can I get protein coffee near me in Pearland?",
   "Nutrition Hub is at 8201 Broadway, Suite 113, Pearland, TX 77581 — open from 6:30 AM Mon–Fri. Order online or walk in."),
 ],
 cta_label="☕ Order Your Coffee",
 close_h2='Upgrade <span>your morning cup.</span>',
 close_p="Order online and it's ready when you walk in — from 6:30 AM on weekdays.",
))

# ================= PAGE 3: SMOOTHIES (head term) =================
# Replaces the planned weight-loss-smoothies page — that intent is already owned
# by meal-replacement-shakes-pearland. "smoothies pearland" was uncovered.
PAGES.append(dict(
 slug="smoothies-pearland", acc="#2effb4", acc2="#23e0ff", accglow="rgba(46,255,180,.45)",
 # 8/7/2026 TITLES PASS (build item 3). The map pack surfaces NH for the BARE head
 # terms — "smoothies near me" 369, "smoothie" 256, "smoothie near me" 246 = 871 —
 # not for "protein smoothie." The old title led with "Protein Smoothie Shop", which
 # qualifies the head term away from exactly the searcher we're shown to, and ran 65
 # chars (truncating). Now leads with the bare term and spends the saved characters
 # on a CTR hook instead of a qualifier. "Protein" stays in the H2/body where it
 # differentiates without gatekeeping the click.
 title="Smoothies in Pearland, TX — 16 Fresh Flavors | Nutrition Hub",
 desc="Smoothies in Pearland, TX — 16 flavors blended fresh to order with 24–30g protein, from $7.80. Open 7 days on Broadway. Order online for pickup.",
 ogimg=f"{GH}/shake_strawberry_cheesecake.png",
 schema_desc="Smoothie shop in Pearland, TX — 16 gourmet protein smoothies with 24–30g protein, made fresh to order.",
 serves=["Smoothies", "Protein Smoothies", "Protein Shakes", "Energy Teas"],
 h1='<span class="a">Smoothies</span><br>in <span class="b">Pearland, TX</span>',
 hero_sub="16 smoothies blended fresh to order — dessert flavors with 24–30g of protein, open 7 days a week.",
 # "shop" over "spot": it's the word people actually type alongside "smoothie".
 intro_h2='Pearland\'s <span>smoothie shop</span> on Broadway',
 intro=f"""<p>Looking for <strong>smoothies in Pearland</strong>? Nutrition Hub on Broadway blends 16 gourmet protein smoothies fresh to order — every one packing <strong>24–30g of protein</strong> and tasting like dessert. Banana Pudding, Strawberry Cheesecake, Salted Caramel and more.</p>
    <p>Unlike sugar-heavy chain smoothies, ours are built to actually fill you up: real protein, controlled calories, craveable flavors. Want a lighter option? Our 20oz smoothies run about 200 calories with 24g protein at $7.80.</p>
    <p>Chasing a specific goal? See our <a href="/meal-replacement-shakes-pearland/">meal replacement shakes</a> or <a href="/protein-shakes-pearland/">post-workout protein shakes</a>, add a <a href="/loaded-teas-pearland/">loaded tea</a>, or <a href="{ORDER}" target="_blank" onclick="fbq('track','Lead')">order online</a> from the full menu.</p>""",
 grid_h2='Fan-favorite <span>smoothies</span>',
 grid_lead="A taste of the 16-smoothie board — all made fresh with 24–30g protein.",
 grid="\n".join([
  card(f"{GH}/shake_banana_pudding.png", "GOURMET", "Banana Pudding", "24–30g protein · tastes like dessert", "$9.97"),
  card(f"{GH}/shake_strawberry_cheesecake.png", "GOURMET", "Strawberry Cheesecake", "24–30g protein · creamy &amp; filling", "$9.97"),
  card(f"{GH}/shake_salted_caramel.png", "GOURMET", "Salted Caramel", "24–30g protein · sweet &amp; salty", "$9.97"),
 ]),
 why_h2='Why our <span>smoothies</span> are different',
 why=[("💪", "24–30g <span>protein</span>", "Every gourmet smoothie is protein-first — filling fuel, not a sugar bomb."),
      ("🍰", "16 <span>flavors</span>", "A full board of dessert flavors made fresh to order — there's a favorite for everyone."),
      ("📆", "Open <span>7 days</span>", "Weekday mornings from 6:30 AM through Sunday afternoons — smoothies whenever you need one.")],
 faqs=[
  ("What smoothies do you have in Pearland?",
   "Nutrition Hub keeps 16 gourmet protein smoothies on the board — flavors like Banana Pudding, Strawberry Cheesecake, and Salted Caramel — all made fresh to order with 24–30g of protein."),
  ("How much do smoothies cost in Pearland?",
   "Gourmet protein smoothies are $9.97 and 20oz smoothies are $7.80 at Nutrition Hub. Order online at order.nutritionhub101.com or walk in at 8201 Broadway, Suite 113."),
  ("Are your smoothies healthy?",
   "Ours are protein-first: 24–30g of protein with controlled calories (20oz smoothies run about 200 calories), so they fill you up instead of spiking you with sugar like typical chain smoothies."),
  ("Can I add extras to my smoothie?",
   "Yes — boost any smoothie with add-ins like BCAAs, creatine, or a B12 energy drink on the side. Just ask when you order."),
  ("Where can I get smoothies near me in Pearland, TX?",
   "Nutrition Hub is at 8201 Broadway, Suite 113, Pearland, TX 77581 — open 7 days a week. Order online for pickup or walk in; first visit, ask for Ronnie."),
 ],
 cta_label="🥤 Order a Smoothie",
 close_h2='Find your <span>favorite flavor.</span>',
 close_p="16 gourmet smoothies on the board — order online and skip the line, or walk in and let us blend it fresh.",
))

# ================= PAGE 4: HEALTHY BREAKFAST =================
PAGES.append(dict(
 slug="healthy-breakfast-pearland", acc="#ffd166", acc2="#ff7a18", accglow="rgba(255,209,102,.45)",
 title="Healthy Breakfast in Pearland, TX — Open 6:30 AM | Nutrition Hub",
 desc="Healthy breakfast in Pearland, TX from 6:30 AM — protein shake + energy tea combo, 24–30g protein, grab-and-go. Order online. 8201 Broadway, Suite 113.",
 ogimg=f"{GH}/shake_banana_pudding.png",
 schema_desc="Healthy grab-and-go breakfast in Pearland, TX — protein shakes and energy teas from 6:30 AM on weekdays.",
 serves=["Smoothies", "Protein Shakes", "Energy Teas", "Coffee"],
 h1='Healthy <span class="a">Breakfast</span><br>in <span class="b">Pearland, TX</span>',
 hero_sub="The classic combo: a 24–30g protein shake plus a loaded energy tea — grab-and-go from 6:30 AM on weekdays.",
 intro_h2='Breakfast that <span>works as hard as you do</span>',
 intro=f"""<p>Need a <strong>healthy breakfast in Pearland</strong> that isn't a drive-thru biscuit? Nutrition Hub on Broadway opens at <strong>6:30 AM on weekdays</strong> with the combo our regulars run on: a gourmet protein shake (24–30g protein, tastes like dessert) plus a loaded energy tea for a clean morning lift.</p>
    <p>It's fast, filling, and doesn't wreck your morning with a sugar crash. Order online on your way in and it's ready when you arrive — or make it a standing habit like half of Pearland's early crowd.</p>
    <p>Prefer coffee? Try our <a href="/protein-coffee-pearland/">protein coffee</a>. Watching calories? The <a href="/meal-replacement-shakes-pearland/">meal replacement shakes</a> were built for that. Full menu <a href="{ORDER}" target="_blank" onclick="fbq('track','Lead')">here</a>.</p>""",
 grid_h2='The <span>breakfast combo</span>',
 grid_lead="Shake + tea is the house move — here's how our regulars build it.",
 grid="\n".join([
  card(f"{GH}/shake_banana_pudding.png", "STEP 1", "Protein Shake", "24–30g protein · your filling 'meal'", "$9.97"),
  card(f"{GH}/tea_dragon_juice.png", "STEP 2", "Loaded Tea", "32oz clean energy · your morning lift", "$9.15"),
  card(None, "OPTIONAL", "B12 Energy Drink", "A $3 B-vitamin energy add-on", "$3.00"),
 ]),
 why_h2='Why breakfast <span>here beats the drive-thru</span>',
 why=[("⏰", "Ready <span>fast</span>", "Order online on your way and grab it at the counter — quicker than most drive-thru lines."),
      ("💪", "Actually <span>filling</span>", "24–30g of protein holds you to lunch — no 9:30 AM vending machine run."),
      ("🌅", "Open <span>6:30 AM</span>", "Earlier than most smoothie spots in Pearland — built for the work crowd.")],
 faqs=[
  ("What's a healthy breakfast option in Pearland?",
   "Nutrition Hub's shake-and-tea combo is a local favorite: a gourmet protein shake with 24–30g of protein plus a 32oz loaded energy tea for a clean morning lift. Grab-and-go from 6:30 AM on weekdays at 8201 Broadway, Suite 113."),
  ("How early are you open for breakfast?",
   "We open at 6:30 AM Monday through Friday, 8 AM Saturday, and noon on Sunday. Order online at order.nutritionhub101.com and it's ready when you walk in."),
  ("How much does the breakfast combo cost?",
   "A gourmet protein shake is $9.97 and a loaded tea is $9.15 — most regulars grab both. Lighter option: a 20oz smoothie at $7.80."),
  ("Is a protein shake enough for breakfast?",
   "With 24–30g of protein and around 300 calories, our gourmet shakes are built to stand in for a meal and keep you full through the morning. Add a tea for energy and you're set."),
  ("Where can I get a healthy breakfast near me in Pearland?",
   "Nutrition Hub is at 8201 Broadway, Suite 113, Pearland, TX 77581 — on Broadway/FM 518, easy to hit on the morning commute. Order online or walk in."),
 ],
 cta_label="🌅 Order Breakfast",
 close_h2='Make it your <span>morning habit.</span>',
 close_p="Order online on the way in — your shake and tea will be waiting at the counter.",
))

# ================= PAGE 5: NUTRITION CLUB (category term) =================
PAGES.append(dict(
 slug="nutrition-club-pearland", acc="#ff5a5a", acc2="#a64dff", accglow="rgba(255,90,90,.45)",
 title="Nutrition Club in Pearland, TX | Nutrition Hub",
 desc="Nutrition Hub is Pearland's nutrition club — protein shakes, loaded teas, and a community that knows your name. 8201 Broadway, Suite 113. Open 7 days.",
 ogimg=f"{GH}/shake_strawberry_cheesecake.png",
 schema_desc="Nutrition club in Pearland, TX serving protein shakes, meal replacement smoothies, and loaded energy teas 7 days a week.",
 serves=["Protein Shakes", "Smoothies", "Energy Teas", "Loaded Teas"],
 h1='Your <span class="a">Nutrition Club</span><br>in <span class="b">Pearland, TX</span>',
 hero_sub="Protein shakes, loaded teas, and a spot where somebody actually knows your name — that's what a nutrition club is.",
 intro_h2='What\'s a <span>nutrition club</span>?',
 intro=f"""<p>A <strong>nutrition club</strong> is part smoothie shop, part community hangout: protein shakes and loaded teas made fresh, plus people who learn your order, cheer on your goals, and notice when you don't show up. <strong>Nutrition Hub</strong> is Pearland's — right on Broadway at Suite 113.</p>
    <p>Whether you're cutting calories, fueling workouts, or just want a better daily drink than a gas-station energy can, you'll find your thing on the board: 16 gourmet protein smoothies, 12+ loaded teas, protein coffee, and add-on boosts.</p>
    <p>Start with the fan favorites — a <a href="/smoothies-pearland/">gourmet smoothie</a> and a <a href="/loaded-teas-pearland/">loaded tea</a> — or <a href="{ORDER}" target="_blank" onclick="fbq('track','Lead')">browse the full menu online</a>. First visit? Ask for Ronnie.</p>""",
 grid_h2='What\'s on <span>the board</span>',
 grid_lead="Everything is made fresh to order, 7 days a week.",
 grid="\n".join([
  card(f"{GH}/shake_strawberry_cheesecake.png", "16 FLAVORS", "Gourmet Smoothies", "24–30g protein · dessert flavors", "$9.97"),
  card(f"{GH}/tea_blue_margarita.png", "12+ FLAVORS", "Loaded Teas", "32oz clean energy · low calorie", "$9.15"),
  card(f"{GH}/shake_chocolate.png", "MORNINGS", "Protein Coffee", "Real coffee blended with protein", "$9.97"),
 ]),
 why_h2='Why Pearland <span>chooses us</span>',
 why=[("🤝", "Community <span>first</span>", "We learn your name and your order. Bring a friend — that's how most people find us."),
      ("🥤", "Something for <span>every goal</span>", "Weight goals, gym fuel, clean energy, or just a better-tasting habit — the board covers it."),
      ("📍", "Easy on <span>Broadway</span>", "8201 Broadway, Suite 113 — on FM 518 with easy parking, open 7 days a week.")],
 faqs=[
  ("What is a nutrition club?",
   "A nutrition club is a local shop serving protein shakes, meal replacement smoothies, and loaded energy teas in a community setting — a healthier alternative to fast food and energy drinks. Nutrition Hub is Pearland's nutrition club, at 8201 Broadway, Suite 113."),
  ("What does a nutrition club serve?",
   "Nutrition Hub serves 16 gourmet protein smoothies (24–30g protein, $9.97), 12+ loaded teas ($9.15), protein coffee, 20oz smoothies ($7.80), and add-on boosts like a $3 B12 energy drink."),
  ("Do I need a membership to visit a nutrition club?",
   "No — just walk in or order online like any smoothie shop. No membership, no commitment; first visit, ask for Ronnie and we'll walk you through the board."),
  ("What are your hours?",
   "Mon–Thu 6:30 AM–5 PM, Friday 6:30 AM–3 PM, Saturday 8 AM–2 PM, Sunday 12–3 PM. Order ahead online at order.nutritionhub101.com."),
  ("Is there a nutrition club near me in Pearland, TX?",
   "Yes — Nutrition Hub at 8201 Broadway, Suite 113, Pearland, TX 77581, on FM 518. We serve Pearland, Friendswood, Silverlake, and Shadow Creek Ranch, 7 days a week."),
 ],
 cta_label="🥤 See the Menu",
 close_h2='Come be a <span>regular.</span>',
 close_p="Walk in and ask for Ronnie, or order online and skip the line — either way, welcome to the club.",
))

# ================= PAGE 6: HEALTHY FOOD (map-pack head term) =================
# Built 8/6/2026 off the GBP map-pack term list, NOT off GSC. "healthy food near
# me" (665) + "healthy food pearland" (121, literal exact-match) = 911 searches =
# 26% of everything that surfaces NH in the map pack — the single largest cluster,
# and NH had zero coverage for it. See HANDOFF-2026-08-06-PM-gbp-fixes-and-reviews.md.
#
# Positioning: this is the FOOD page. The rest of the cluster is drink-led, so this
# one leads with what you can actually eat (waffle, protein balls, candied grapes)
# and treats the shake as a meal. Deliberately NOT overlapping:
#   healthy-breakfast-pearland = morning/6:30 AM combo intent
#   meal-replacement-shakes-pearland = weight-loss intent
#   smoothies-pearland = the smoothie head term
#   nutrition-club-pearland = the category term
# Food photos are served from the VPS (IMGV), not GH raw — new images on this
# unmerged branch would 404 on raw.githubusercontent.com/.../main/.
PAGES.append(dict(
 slug="healthy-food-pearland", acc="#7ed957", acc2="#2effb4", accglow="rgba(126,217,87,.45)",
 title="Healthy Food in Pearland, TX — Protein Meals | Nutrition Hub",
 desc="Healthy food in Pearland, TX — protein-packed meals and snacks from $4. Protein balls, donuts, waffles, and shakes with 24–30g protein. Open 7 days.",
 ogimg=f"{IMGV}/waffle.jpg",
 schema_desc="Healthy food in Pearland, TX — protein-first meals and snacks including loaded waffles, protein balls, and 24–30g protein shakes, made fresh 7 days a week.",
 serves=["Healthy Food", "Protein Shakes", "Smoothies", "Protein Snacks"],
 h1='Healthy <span class="a">Food</span><br>in <span class="b">Pearland, TX</span>',
 hero_sub="Protein-first food that actually fills you up — snacks from $4.50, meals with 24–30g of protein, made fresh 7 days a week.",
 intro_h2='Where to find <span>healthy food in Pearland</span>',
 intro=f"""<p>Looking for <strong>healthy food in Pearland</strong> that isn't a drive-thru bag or a sad pre-made salad? <strong>Nutrition Hub</strong> on Broadway is built around one idea: protein first. Our gourmet shakes carry <strong>24–30g of protein</strong> in about 300 calories — enough to actually work as a meal — and we keep real food and protein snacks on the counter for the grab-and-go crowd.</p>
    <p>On the food side: <strong>protein balls</strong> (4-pack, $4.50), <strong>candied protein grapes</strong> ($4.50), <strong>mini donuts</strong> (6 to a bag, $4), an <strong>acai bowl</strong> ($14.00) topped with fresh berries, banana and granola, and a loaded <strong>waffle</strong> ($12.75) topped with fresh strawberries, blueberries and granola when you want a real sit-down plate. On the drink side, 16 gourmet smoothies, 12+ teas, and protein coffee — all made fresh to order.</p>
    <p>Eating for a goal? Our <a href="/meal-replacement-shakes-pearland/">meal replacement shakes</a> were built for that, and the <a href="/healthy-breakfast-pearland/">healthy breakfast combo</a> runs from 6:30 AM. In a hurry? Everything on the <a href="/grab-and-go-pearland/">grab-and-go counter</a> starts at $4. New to us? Start with the <a href="/smoothies-pearland/">smoothie board</a> or see what a <a href="/nutrition-club-pearland/">nutrition club</a> actually is. <a href="{ORDER}" target="_blank" onclick="fbq('track','Lead')">Order online</a> and skip the line.</p>""",
 grid_h2='Real <span>food &amp; protein snacks</span>',
 grid_lead="A hot plate, a shake that works as a meal, and snacks from $4.50.",
 grid="\n".join([
  # Waffle leads as of 8/7: Ronnie's new photo (fresh strawberries, blueberries,
  # granola) actually reads as healthy food. The previous shot — whipped cream,
  # chocolate chips, caramel drizzle — was kept out of this grid on purpose because
  # it contradicted the page's promise. Photo, not product, was the blocker.
  card(f"{IMGV}/waffle.jpg", "HOT PLATE", "Loaded Waffle", "Fresh strawberries, blueberries and granola", "$12.75"),
  # Uses the TRANSPARENT clean_* variant (served via IMGV). The repo's clean_shake_*
  # PNGs were never pushed to main, so GH raw 404s on them and every other landing
  # page falls back to the black-boxed original. Free visual upgrade available there.
  card(f"{IMGV}/protein-shake.png", "MEAL", "Protein Shake", "24–30g protein · ~300 cal · fills you up like a meal", "$9.97"),
  card(f"{IMGV}/acaibowl.jpg", "BOWL", "Acai Bowl", "Fresh berries, banana and granola on an acai base", "$14.00"),
  card(f"{IMGV}/protein-balls.jpg", "GRAB-AND-GO", "Protein Balls", "4-pack · oats and chocolate, protein-packed bite", "$4.50"),
 ]),
 why_h2='What makes it <span>healthy food</span> here',
 why=[("💪", "Protein <span>first</span>", "Every meal option is built around 24–30g of protein — the thing that actually keeps you full, instead of a sugar spike that leaves you hungry an hour later."),
      ("🥡", "Real <span>grab-and-go</span>", "Protein balls and candied grapes on the counter from $4.50 — faster than a drive-thru and you can eat it in the car without regret."),
      ("📆", "Open <span>7 days</span>", "Weekday mornings from 6:30 AM through Sunday afternoon at 8201 Broadway, Suite 113 — easy parking, right on FM 518.")],
 faqs=[
  ("Where can I find healthy food near me in Pearland, TX?",
   "Nutrition Hub is at 8201 Broadway, Suite 113, Pearland, TX 77581, right on Broadway (FM 518). We serve protein-first meals and snacks 7 days a week — protein shakes with 24–30g of protein, protein balls, candied protein grapes, acai bowls, and waffles. Order online at order.nutritionhub101.com or walk in."),
  ("What healthy food does Nutrition Hub serve?",
   "Protein balls (4-pack, $4.50), candied protein grapes ($4.50), mini donuts (6-pack, $4), an acai bowl ($14.00), and a loaded waffle ($12.75) on the food side. On the drink side, 16 gourmet protein smoothies with 24–30g protein ($9.97), 20oz smoothies ($7.80), 12+ teas ($9.15), and protein coffee ($9.97). Everything is made fresh to order."),
  ("Can a protein shake really replace a meal?",
   "Our gourmet shakes run 24–30g of protein at around 300 calories, which is what makes them filling enough to stand in for a meal rather than just a snack. A lot of our regulars run one for lunch and eat a normal dinner."),
  ("Do you have healthy grab-and-go snacks?",
   "Yes — protein balls in a 4-pack and candied protein grapes are both $4.50 and sit right on the counter. They're the quickest thing we sell, and the most popular add-on to a shake or tea."),
  ("How much does healthy food cost at Nutrition Hub?",
   "Snacks start at $4.50, a 20oz smoothie is $7.80, gourmet protein smoothies and protein coffee are $9.97, and the waffle is $12.75. Most people spend $10–15 for a full meal. Order online or walk in at 8201 Broadway, Suite 113."),
 ],
 cta_label="🍽️ Order Online",
 close_h2='Eat something that <span>actually works.</span>',
 close_p="Order online and it's ready at the counter — or walk in and ask for Ronnie on your first visit.",
))

# ================= PAGE 7: GRAB-AND-GO / MEAL-PREP INTENT =================
# Build item (2) from the 8/6 PM handoff. The map-pack list shows "Power Fit Eats"
# — a DIFFERENT local business's brand — pulling up NH 495 times (14% of all
# impressions), with `meal prep pearland` trailing it, and NH had zero coverage.
#
# ⚠️ WHITE-HAT RULE, NON-NEGOTIABLE: their brand name appears nowhere on this page —
# not in the title, H1, meta, body, schema, or alt text. We build a genuine page for
# what NH actually sells and let Google keep making the association it already makes.
#
# 🔑 POSITIONING CALL (Ronnie OK'd 8/7): the demand term is "meal prep," but NH does
# NOT sell meal prep — no containers, no weekly plans. It sells grab-and-go protein.
# Selling "meal prep" would rank and then disappoint everyone who walked in. So the
# page is honestly framed as GRAB-AND-GO, and the meal-prep query is answered head-on
# in an FAQ ("we're the no-prep alternative") — which earns the query without lying.
PAGES.append(dict(
 slug="grab-and-go-pearland", acc="#ff8c42", acc2="#2effb4", accglow="rgba(255,140,66,.45)",
 title="Grab-and-Go Protein Snacks in Pearland, TX | Nutrition Hub",
 desc="Grab-and-go protein snacks in Pearland, TX from $4 — mini donuts, protein balls, candied protein grapes, and shakes that work as a quick meal. Order ahead.",
 ogimg=f"{IMGV}/donuts.jpg",
 schema_desc="Grab-and-go protein snacks and quick meals in Pearland, TX — mini donuts, protein balls, candied protein grapes, and 24–30g protein shakes, made fresh 7 days a week.",
 serves=["Protein Snacks", "Healthy Food", "Protein Shakes", "Smoothies"],
 h1='<span class="a">Grab-and-Go</span><br>in <span class="b">Pearland, TX</span>',
 hero_sub="Protein snacks from $4 and a shake that works as a whole meal — in and out in a couple of minutes, 7 days a week.",
 intro_h2='The <span>no-prep</span> way to eat better in Pearland',
 intro=f"""<p>Some weeks you plan every meal. Most weeks you don't. <strong>Nutrition Hub</strong> on Broadway is built for the second kind — <strong>grab-and-go protein</strong> you can pick up on the way to work, between errands, or on the way home, with nothing to plan and nothing to wash.</p>
    <p>On the counter right now: <strong>mini donuts</strong> (6 to a bag, $4), <strong>protein balls</strong> (4-pack, $4.50), and <strong>candied protein grapes</strong> ($4.50). Want something that actually holds you over? A gourmet shake carries <strong>24–30g of protein</strong> in about 300 calories and drinks like dessert, or there's a hot <strong>waffle</strong> ($12.75) if you've got a minute to sit.</p>
    <p>Order ahead and it's bagged and waiting at the counter. See the <a href="/healthy-food-pearland/">full healthy food lineup</a>, the <a href="/smoothies-pearland/">smoothie board</a>, or the <a href="/healthy-breakfast-pearland/">6:30 AM breakfast combo</a> — or <a href="{ORDER}" target="_blank" onclick="fbq('track','Lead')">order online</a> right now.</p>""",
 grid_h2='On the <span>counter today</span>',
 grid_lead="Everything here is grab-and-go — no wait, no prep, from $4.",
 grid="\n".join([
  card(f"{IMGV}/donuts.jpg", "$4 · 6-PACK", "Mini Donuts", "Six to a bag — the fastest thing we sell", "$4.00"),
  card(f"{IMGV}/protein-balls.jpg", "4-PACK", "Protein Balls", "Oats and chocolate, protein-packed bite", "$4.50"),
  card(f"{IMGV}/candied-protein-grapes.jpg", "CHILLED", "Candied Protein Grapes", "Cold, sweet, and gone before you get home", "$4.50"),
 ]),
 why_h2='Why <span>grab-and-go</span> beats meal prep for most people',
 why=[("⏱️", "Zero <span>planning</span>", "No Sunday afternoon cooking, no containers, no forgetting the bag on the counter. You pick it up on the day you actually want it."),
      ("💪", "Still <span>protein-first</span>", "The reason meal prep works is protein and portion control. You get both here without the prep — a gourmet shake runs 24–30g of protein at around 300 calories."),
      ("🛍️", "Order <span>ahead</span>", "Order online on the way over and it's bagged at the counter when you walk in. In and out in about the time it takes to park.")],
 faqs=[
  ("Do you do meal prep in Pearland?",
   "Not in the containers-for-the-week sense — Nutrition Hub doesn't sell prepped meal boxes. What we do is the no-prep alternative: grab-and-go protein snacks from $4 and gourmet shakes with 24–30g of protein that stand in for a meal, made fresh whenever you walk in. If meal prep keeps falling apart by Wednesday, this is the version that doesn't need planning."),
  ("What grab-and-go snacks do you have?",
   "Mini donuts (6 to a bag, $4), protein balls (4-pack, $4.50), and candied protein grapes ($4.50) sit right on the counter. There's also a hot waffle for $12.75 if you have a few minutes, and gourmet protein shakes at $9.97."),
  ("How much do your grab-and-go snacks cost?",
   "Snacks start at $4 for a 6-pack of mini donuts. Protein balls and candied protein grapes are $4.50 each, a 20oz smoothie is $7.80, and gourmet protein shakes are $9.97. Most people spend $10–15 for a snack and a drink."),
  ("Can I get a quick healthy lunch in Pearland?",
   "Yes — a gourmet protein shake with 24–30g of protein at around 300 calories is what most of our regulars use for a fast lunch, often with a snack on the side. Order online at order.nutritionhub101.com and it's ready at the counter when you arrive."),
  ("Where can I grab healthy food near me in Pearland, TX?",
   "Nutrition Hub is at 8201 Broadway, Suite 113, Pearland, TX 77581, right on Broadway (FM 518) with easy parking. Open Mon–Thu 6:30 AM–5 PM, Friday 6:30 AM–3 PM, Saturday 8 AM–2 PM, and Sunday 12–3 PM."),
 ],
 cta_label="🛍️ Order Ahead",
 close_h2='Skip the prep. <span>Just grab it.</span>',
 close_p="Order online on your way over and it's bagged at the counter — or walk in and see what's out today.",
))

# ================= PAGES 8–10: NEIGHBORHOODS =================
def hood_page(slug, hood, acc, acc2, glow, drive_line, local_line):
    return dict(
     slug=slug, acc=acc, acc2=acc2, accglow=glow,
     title=f"Smoothies & Loaded Teas near {hood} | Nutrition Hub Pearland",
     desc=f"Protein smoothies and loaded teas near {hood} — Nutrition Hub in Pearland, {drive_line}. 24–30g protein shakes, 12+ teas. Order online for pickup.",
     ogimg=f"{GH}/shake_banana_pudding.png",
     schema_desc=f"Protein smoothies and loaded energy teas serving {hood} from Nutrition Hub in Pearland, TX.",
     serves=["Smoothies", "Protein Shakes", "Loaded Teas", "Energy Teas"],
     area=hood,
     h1=f'Smoothies &amp; <span class="a">Loaded Teas</span><br>near <span class="b">{hood}</span>',
     hero_sub=f"Nutrition Hub is {drive_line} from {hood} — 16 gourmet protein smoothies and 12+ loaded teas, made fresh to order.",
     intro_h2=f'Serving <span>{hood}</span> from Broadway',
     intro=f"""<p>Live or work around <strong>{hood}</strong> and craving a real protein smoothie or a loaded tea? <strong>Nutrition Hub</strong> is {drive_line} away at 8201 Broadway, Suite 113 in Pearland — {local_line}</p>
    <p>The board: 16 gourmet protein smoothies with <strong>24–30g protein</strong> that taste like dessert, 12+ loaded teas for clean energy, protein coffee for the morning run, and 20oz smoothies from $7.80.</p>
    <p>The move from {hood}: <a href="{ORDER}" target="_blank" onclick="fbq('track','Lead')">order online</a> before you leave and it's ready at the counter. See our <a href="/smoothies-pearland/">smoothies</a>, <a href="/loaded-teas-pearland/">loaded teas</a>, or the <a href="/">full menu</a>.</p>""",
     grid_h2='Worth the <span>short drive</span>',
     grid_lead="Fan favorites our regulars drive in for.",
     grid="\n".join([
      card(f"{GH}/shake_banana_pudding.png", "GOURMET", "Banana Pudding", "24–30g protein · tastes like dessert", "$9.97"),
      card(f"{GH}/tea_dragon_juice.png", "LOADED TEA", "Dragon Juice", "32oz · clean energy, no crash", "$9.15"),
      card(f"{GH}/shake_strawberry_cheesecake.png", "GOURMET", "Strawberry Cheesecake", "24–30g protein · creamy &amp; filling", "$9.97"),
     ]),
     why_h2=f'Why {hood} <span>drives to us</span>',
     why=[("🚗", "Quick <span>trip</span>", f"We're {drive_line} from {hood} — order online and your drinks are ready when you pull up."),
          ("💪", "Protein <span>first</span>", "24–30g of protein per gourmet smoothie — filling fuel, not mall-smoothie sugar."),
          ("🤝", "Small-club <span>feel</span>", "We learn your name and your order. First visit, ask for Ronnie.")],
     faqs=[
      (f"Is there a smoothie shop near {hood}?",
       f"Yes — Nutrition Hub in Pearland is {drive_line} from {hood}, at 8201 Broadway, Suite 113. We make 16 gourmet protein smoothies and 12+ loaded teas fresh to order, 7 days a week."),
      (f"Where can I get a loaded tea near {hood}?",
       f"Nutrition Hub serves 12+ loaded tea flavors ($9.15 for 32oz), {drive_line} from {hood}. Order online at order.nutritionhub101.com for pickup."),
      ("How much are your smoothies?",
       "Gourmet protein smoothies with 24–30g protein are $9.97; 20oz smoothies are $7.80; loaded teas are $9.15."),
      ("Can I order ahead?",
       f"Yes — order online at order.nutritionhub101.com before you leave {hood} and your order will be ready at the counter when you arrive."),
      ("What are your hours?",
       "Mon–Thu 6:30 AM–5 PM, Friday 6:30 AM–3 PM, Saturday 8 AM–2 PM, Sunday 12–3 PM at 8201 Broadway, Suite 113, Pearland, TX 77581."),
     ],
     cta_label="🥤 Order for Pickup",
     close_h2=f'{hood}, your <span>order\'s ready.</span>',
     close_p="Order online before you head over and skip the line — first visit, ask for Ronnie.",
    )

PAGES.append(hood_page("smoothies-shadow-creek-ranch", "Shadow Creek Ranch",
 "#23e0ff", "#2effb4", "rgba(35,224,255,.45)", "a straight shot down Broadway (FM 518)",
 "an easy run east on FM 518 whenever you're headed across Pearland."))
PAGES.append(hood_page("smoothies-silverlake", "Silverlake",
 "#ff2e88", "#ffd166", "rgba(255,46,136,.45)", "a few minutes east on Broadway (FM 518)",
 "just follow Broadway east and we're on your right at Suite 113."))
PAGES.append(hood_page("smoothies-friendswood", "Friendswood",
 "#2effb4", "#a64dff", "rgba(46,255,180,.45)", "a short drive up FM 518",
 "right where Broadway meets east Pearland — closer than you think."))

# ---------------- TEMPLATE ----------------
TPL = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__TITLE__</title>
<meta name="description" content="__DESC__">
<link rel="canonical" href="https://__DOMAIN__/__SLUG__/">

<meta property="og:type" content="website">
<meta property="og:title" content="__TITLE__">
<meta property="og:description" content="__DESC__">
<meta property="og:url" content="https://__DOMAIN__/__SLUG__/">
<meta property="og:image" content="__OGIMG__">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="__TITLE__">
<meta name="twitter:description" content="__DESC__">

<!-- LocalBusiness structured data -->
<script type="application/ld+json">
__BIZ_JSONLD__
</script>

<!-- FAQ structured data (eligible for FAQ rich results) -->
<script type="application/ld+json">
__FAQ_JSONLD__
</script>

<!-- Meta Pixel -->
<script>
!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;
n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,
document,'script','https://connect.facebook.net/en_US/fbevents.js');
fbq('init','__PIXEL__');fbq('track','PageView');
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id=__PIXEL__&ev=PageView&noscript=1"/></noscript>
<style>
  :root{
    --bg:#0a0a12; --card:#12121e; --line:#23233a;
    --acc:__ACC__; --acc2:__ACC2__; --accGlow:__ACCGLOW__; --pink:#ff2e88; --lime:#a6ff4d;
    --txt:#f2f0f7; --mut:#a3a0b8;
    --font:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  }
  *{margin:0;padding:0;box-sizing:border-box}
  html{scroll-behavior:smooth}
  body{background:var(--bg);color:var(--txt);font-family:var(--font);overflow-x:hidden;line-height:1.5}
  a{color:inherit;text-decoration:none}
  .wrap{max-width:1080px;margin:0 auto;padding:0 22px}
  .nav{position:sticky;top:0;z-index:50;background:rgba(10,10,18,.85);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
  .nav .row{display:flex;align-items:center;justify-content:space-between;padding:12px 0}
  .brand{font-weight:900;letter-spacing:.5px;font-size:18px}
  .nav .btn{padding:9px 18px;font-size:13px}
  .hero{position:relative;padding:64px 0 46px;text-align:center;overflow:hidden}
  .hero::before{content:"";position:absolute;inset:0;background:
    radial-gradient(600px 300px at 18% 0%,var(--accGlow),transparent 62%),
    radial-gradient(700px 360px at 85% 18%,rgba(255,46,136,.12),transparent 60%)}
  .pill{position:relative;display:inline-flex;align-items:center;gap:8px;background:var(--card);border:1px solid var(--line);color:var(--mut);font-size:12px;font-weight:800;letter-spacing:1.2px;padding:7px 16px;border-radius:40px;margin-bottom:22px}
  .hero h1{position:relative;font-size:clamp(32px,6vw,58px);line-height:1.05;font-weight:900;letter-spacing:-1px}
  .hero h1 .a{color:var(--acc);text-shadow:0 0 18px var(--accGlow)} .hero h1 .b{color:var(--pink)}
  .hero p{position:relative;max-width:600px;margin:18px auto 0;color:var(--mut);font-size:17px}
  .cta{position:relative;display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin-top:30px}
  .btn{cursor:pointer;display:inline-block;border:none;font-family:var(--font);font-weight:900;letter-spacing:.5px;border-radius:40px;transition:.18s;font-size:14px}
  .btn-acc{background:var(--acc);color:#0a0a12;padding:14px 26px;box-shadow:0 0 24px var(--accGlow)}
  .btn-acc:hover{transform:translateY(-2px)}
  .btn-pink{background:var(--pink);color:#fff;padding:14px 26px;box-shadow:0 0 22px rgba(255,46,136,.4)}
  .btn-pink:hover{transform:translateY(-2px)}
  .btn-ghost{background:transparent;border:1px solid var(--line);color:var(--txt);padding:13px 24px}
  .btn-ghost:hover{border-color:var(--acc);color:var(--acc)}
  .sec{padding:48px 0;border-top:1px solid var(--line)}
  .sec h2{font-size:clamp(26px,4.4vw,38px);font-weight:900;letter-spacing:-.5px;text-align:center}
  .sec h2 span{color:var(--acc)}
  .sec .lead{color:var(--mut);text-align:center;max-width:620px;margin:12px auto 0;font-size:15px}
  .prose{max-width:760px;margin:28px auto 0;color:var(--txt);font-size:16px;line-height:1.75}
  .prose p{margin-bottom:18px;color:#d8d4e4}
  .prose strong{color:var(--acc)}
  .prose a{color:var(--pink);text-decoration:underline;text-underline-offset:3px}
  .grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:34px}
  .drink{background:var(--card);border:1px solid var(--line);border-radius:20px;padding:18px;text-align:center;position:relative;overflow:hidden;transition:.2s;display:flex;flex-direction:column}
  .drink::after{content:"";position:absolute;left:0;top:0;height:3px;width:100%;background:linear-gradient(90deg,var(--acc),var(--acc2))}
  .drink:hover{transform:translateY(-4px);border-color:var(--acc)}
  .drink img{width:100%;height:200px;object-fit:contain;margin-bottom:12px}
  .drink .emoji{font-size:52px;margin:18px 0 22px}
  .drink .tag{font-size:11px;font-weight:900;letter-spacing:1.5px;padding:4px 10px;border-radius:30px;display:inline-block;margin-bottom:8px;background:var(--card);border:1px solid var(--line);color:var(--acc)}
  .drink h3{font-size:17px;font-weight:900;letter-spacing:-.3px}
  .drink p{color:var(--mut);font-size:13px;margin-top:4px;flex:1}
  .drink .price{display:block;margin-top:8px;font-weight:900;color:var(--txt);font-size:15px}
  .feats{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:34px}
  .fcard{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:24px}
  .fcard .ic{font-size:28px;margin-bottom:10px}
  .fcard h3{font-size:18px;font-weight:900;margin-bottom:6px}
  .fcard h3 span{color:var(--acc)}
  .fcard p{color:var(--mut);font-size:14px}
  .faq{max-width:760px;margin:30px auto 0}
  .qa{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:20px 22px;margin-bottom:14px}
  .qa h3{font-size:16px;font-weight:900;margin-bottom:8px;color:var(--txt)}
  .qa p{color:var(--mut);font-size:14px;line-height:1.7}
  .qa a{color:var(--acc);text-decoration:underline}
  .info{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-top:34px}
  .infocard{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:24px}
  .infocard h3{font-size:16px;font-weight:900;letter-spacing:1px;color:var(--pink);margin-bottom:14px}
  .hrow{display:flex;justify-content:space-between;padding:9px 0;border-bottom:1px solid var(--line);font-size:14px}
  .hrow:last-child{border-bottom:none}
  .hrow .d{color:var(--mut)} .hrow .t{font-weight:700}
  .infocard .addr{font-size:15px;line-height:1.7}
  .infocard .addr b{color:var(--acc)}
  .close{text-align:center;padding:60px 0 36px;border-top:1px solid var(--line)}
  .close h2{font-size:clamp(28px,4.6vw,44px);font-weight:900;letter-spacing:-.5px}
  .close h2 span{color:var(--acc)}
  .close p{color:var(--mut);max-width:480px;margin:14px auto 26px;font-size:15px}
  .footer{text-align:center;color:#6a6880;font-size:12px;padding:26px 0;border-top:1px solid var(--line)}
  .footer a{color:var(--mut)}
  .crumb{font-size:13px;color:var(--mut);padding-top:18px}
  .crumb a{color:var(--acc)}
  @media(max-width:780px){.grid{grid-template-columns:1fr 1fr;gap:12px}.feats{grid-template-columns:1fr}.info{grid-template-columns:1fr}.drink img{height:160px}}
  @media(max-width:480px){.grid{grid-template-columns:1fr}}
</style>
<script defer src="/analytics-consent.js"></script>
<script defer src="/assets/portfolio-measurement.js"></script>
</head>
<body>

<nav class="nav"><div class="wrap row">
  <a class="brand" href="/" style="display:flex;align-items:center;gap:10px">
    <img src="__LOGO__" alt="Nutrition Hub 101" style="height:46px;width:46px;border-radius:50%;background:#fff;padding:3px;object-fit:contain;flex:none">
    <span>NUTRITION <span style="color:var(--lime)">HUB</span></span>
  </a>
  <a class="btn btn-pink" href="__ORDER__" target="_blank" onclick="fbq('track','Lead')">Order Online</a>
</div></nav>

<header class="hero"><div class="wrap">
  <span class="pill">📍 8201 BROADWAY, SUITE 113 · PEARLAND, TX</span>
  <h1>__H1__</h1>
  <p>__HERO_SUB__</p>
  <div class="cta">
    __CTAS__
  </div>
</div></header>

<section class="sec"><div class="wrap">
  <h2>__INTRO_H2__</h2>
  <div class="prose">
    __INTRO__
  </div>
</div></section>

<section class="sec" id="more"><div class="wrap">
  <h2>__GRID_H2__</h2>
  <p class="lead">__GRID_LEAD__</p>
  <div class="grid">
__GRID__
  </div>
  <div class="cta" style="margin-top:34px">
    <a class="btn btn-acc" href="__ORDER__" target="_blank" onclick="fbq('track','Lead')">__CTA_LABEL__ →</a>
  </div>
</div></section>

<section class="sec"><div class="wrap">
  <h2>__WHY_H2__</h2>
  <div class="feats">
__WHY__
  </div>
</div></section>

<section class="sec"><div class="wrap">
  <h2>Frequently asked <span>questions</span></h2>
  <div class="faq">
__FAQ_HTML__
  </div>
</div></section>

<section class="sec"><div class="wrap">
  <h2>Come <span>see us</span></h2>
  <div class="info">
    <div class="infocard">
      <h3>HOURS</h3>
      __HOURS_ROWS__
    </div>
    <div class="infocard">
      <h3>LOCATION</h3>
      <p class="addr">
        <b>Nutrition Hub</b><br>
        8201 Broadway, Suite 113<br>
        Pearland, TX 77581
      </p>
      <div class="cta" style="justify-content:flex-start;margin-top:18px">
        <a class="btn btn-ghost" href="__MAPS__" target="_blank">Get Directions</a>
        <a class="btn btn-ghost" href="__IG__" target="_blank">Message Us on IG</a>
      </div>
    </div>
  </div>
</div></section>

<div class="close"><div class="wrap">
  <h2>__CLOSE_H2__</h2>
  <p>__CLOSE_P__</p>
  <a class="btn btn-acc" href="__ORDER__" target="_blank" onclick="fbq('track','Lead')">__CTA_LABEL__</a>
</div></div>

<div class="footer"><div class="wrap">
  <div class="crumb"><a href="/">← Back to Nutrition Hub home</a></div>
  © 2026 Nutrition Hub · 8201 Broadway, Suite 113, Pearland, TX ·
  <a href="__IG__" target="_blank">@nutritionhub101</a>
</div></div>

</body>
</html>
"""

def biz_jsonld(p):
    d = {"@context": "https://schema.org", "@type": "FoodEstablishment", "name": "Nutrition Hub",
         "description": p["schema_desc"], "url": f"https://{DOMAIN}/{p['slug']}/", "image": p["ogimg"],
         "servesCuisine": p["serves"], "priceRange": "$", "telephone": PHONE_TEL,
         "address": {"@type": "PostalAddress", "streetAddress": ADDR_STREET, "addressLocality": ADDR_LOC,
                     "addressRegion": ADDR_REG, "postalCode": ADDR_ZIP, "addressCountry": "US"},
         "geo": {"@type": "GeoCoordinates", "latitude": LAT, "longitude": LNG},
         "hasMenu": f"{ORDER}/", "acceptsReservations": "False", "sameAs": [IG]}
    if p.get("area"):
        d["areaServed"] = [{"@type": "Place", "name": f"{p['area']}, Pearland, TX"},
                           {"@type": "City", "name": "Pearland"}]
    s = json.dumps(d, indent=2)
    s = s[:-2] + ',\n  "openingHoursSpecification": ' + HOURS_SCHEMA + '\n}'
    return s

def why_html(why):
    return "\n".join(
        f'    <div class="fcard">\n      <div class="ic">{ic}</div>\n      <h3>{h}</h3>\n      <p>{p}</p>\n    </div>'
        for (ic, h, p) in why)

outdir = os.path.dirname(os.path.abspath(__file__))
for p in PAGES:
    faq_json, faq_vis = faq_blocks(p["faqs"])
    html = TPL
    rep = {
        "__TITLE__": p["title"], "__DESC__": p["desc"], "__DOMAIN__": DOMAIN, "__SLUG__": p["slug"],
        "__OGIMG__": p["ogimg"], "__PIXEL__": PIXEL, "__ACC__": p["acc"], "__ACC2__": p["acc2"],
        "__ACCGLOW__": p["accglow"], "__BIZ_JSONLD__": biz_jsonld(p), "__FAQ_JSONLD__": faq_json,
        "__H1__": p["h1"], "__HERO_SUB__": p["hero_sub"], "__CTAS__": ctas(p["cta_label"]),
        "__INTRO_H2__": p["intro_h2"], "__INTRO__": p["intro"],
        "__GRID_H2__": p["grid_h2"], "__GRID_LEAD__": p["grid_lead"], "__GRID__": p["grid"],
        "__WHY_H2__": p["why_h2"], "__WHY__": why_html(p["why"]), "__FAQ_HTML__": faq_vis,
        "__HOURS_ROWS__": HOURS_ROWS, "__MAPS__": MAPS, "__IG__": IG, "__ORDER__": ORDER,
        "__LOGO__": LOGO, "__CTA_LABEL__": p["cta_label"],
        "__CLOSE_H2__": p["close_h2"], "__CLOSE_P__": p["close_p"],
    }
    for k, v in rep.items():
        html = html.replace(k, v)
    left = set(re.findall(r"__[A-Z0-9_]+__", html))
    assert not left, f"{p['slug']}: leftover tokens {left}"
    assert html.count("fbq('init'") == 1, f"{p['slug']}: pixel init count != 1"
    path = os.path.join(outdir, f"{p['slug']}.html")
    open(path, "w", encoding="utf-8").write(html)
    print("wrote", path, f"({len(html)} bytes)")

# ---------------- SITEMAP ----------------
urls = [f"https://{DOMAIN}/"]
urls += [f"https://{DOMAIN}/{s}/" for s in EXISTING_SLUGS]
urls += [f"https://{DOMAIN}/{p['slug']}/" for p in PAGES]
if os.path.isfile(os.path.join(outdir, "blog", "index.html")):
    urls.append(f"https://{DOMAIN}/blog/")
for f in sorted(glob.glob(os.path.join(outdir, "blog", "*.html"))):
    name = os.path.basename(f)
    if name == "index.html":
        continue
    urls.append(f"https://{DOMAIN}/blog/{name[:-5]}/")
urls.append(f"https://order.{DOMAIN}/")

sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u in urls:
    sm += f"  <url><loc>{u}</loc><changefreq>weekly</changefreq></url>\n"
sm += "</urlset>\n"
open(os.path.join(outdir, "sitemap.xml"), "w", encoding="utf-8").write(sm)
print(f"wrote sitemap.xml ({len(urls)} URLs)")
print("\nNEW PAGES:", ", ".join(p["slug"] for p in PAGES))
