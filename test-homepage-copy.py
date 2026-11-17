from pathlib import Path
import hashlib
from html.parser import HTMLParser
p = Path(__file__).with_name("index.html").read_text()
old_lead = 'Join the Hub Rewards club — earn points on every drink and unlock a <b style="color:var(--lime)">free drink</b> when you hit 100.'
new_lead = 'Earn 1 point per visit and unlock a <b style="color:var(--lime)">free drink</b> after 10 visits.'
old_step = 'Free drink at 100'
new_step = 'Free drink after 10 visits'
assert p.count(new_lead) == 1
assert p.count(new_step) == 1
assert old_lead not in p and old_step not in p
delivery_banner = '\n  <p style="font-size:1rem"><strong>Local delivery: $3 fee.</strong> Within 3 miles of our Pearland shop, Monday–Friday, 8–11:30 AM Central. <a href="https://order.nutritionhub101.com/">Order for delivery</a> and select Delivery at checkout; address and time restrictions apply. Pickup and walk-ins remain available.</p>'
assert p.count(delivery_banner) == 1
original = p.replace(delivery_banner, "").replace(new_lead, old_lead).replace(new_step, old_step)
assert hashlib.sha256(original.encode()).hexdigest() == "f36c22b4ddd7cdbcd00b5b14f7b35ba5e8910efc2b424986a4ea693f55f8180d", "Unapproved change outside the two copy replacements"
HTMLParser().feed(p)
print("PASS: exact approved wording; all other production bytes preserved")
