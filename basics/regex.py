import re

string = """abcde
888.559.332
234.234.12
234.234.123
"""
pattern = re.compile(r"(\d{3}\.)(\d{3}\.)(\d{3})")
matches = re.finditer(pattern, string)

# print(list(matches))

for match in matches:
    print(match.group(0))

sub_str = pattern.sub(r"860.\2\3", string)

print(sub_str)
