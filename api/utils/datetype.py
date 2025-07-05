import re

def datetype(value):
  if re.match(r"\b\d{4}-\d{2}-\d{2}\b", value):
    return value
  else:
    raise ValueError("Date must be valid!")