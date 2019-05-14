import yara

def yaramatch(filename):
    rules = yara.compile("DBs/rules/index.yar")
    matches = rules.match(filename)
    return matches
