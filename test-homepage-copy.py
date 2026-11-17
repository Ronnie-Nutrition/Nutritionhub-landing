from pathlib import Path
import hashlib
p = Path(__file__).with_name("index.html").read_bytes()
assert hashlib.sha256(p).hexdigest() == 'f36c22b4ddd7cdbcd00b5b14f7b35ba5e8910efc2b424986a4ea693f55f8180d'
print("PASS: exact production baseline")
