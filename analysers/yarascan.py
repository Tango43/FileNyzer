import yara

def yaramatch(f):
    rules = yara.compile("rules/index.yar")
    matches = rules.match(rf)
    print(str(matches))
    return matches
