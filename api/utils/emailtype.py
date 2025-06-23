import re

def emailtype(value):
  if re.match(r"[^@]+@[^@]+\.[^@]+", value):
    return value
  else:
    raise ValueError("Email must be valid!")