from oletools.olevba import VBA_Parser, TYPE_OLE, TYPE_OpenXML, TYPE_Word2003_XML, TYPE_MHTML

def vbaparsing(filename):
    vbafile = VBA_Parser(filename)
    results = ""
    for (filename, stream_path, vba_filename, vba_code) in vbafile.extract_macros():
        results = results +  vba_code
    result = vbafile.analyze_macros()
    for kw_type, keyword, description in result:
        results = results + 'type=%s - keyword=%s - description=%s' % (kw_type, keyword, description)
    return results
