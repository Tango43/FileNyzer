import yara

def yaramatch(f):
    rules = yara.compile("rules/index.yar")
    matches = rules.match(data=f)
    print(str(matches))
    return matches
