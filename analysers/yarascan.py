import yara

def yaramatch(f):
    rules = yara.compile("rules/index.yar")
    matches = rules.match(data=f)
    return matches
