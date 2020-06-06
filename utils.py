def clamp(s, l=200):
    if len(s) > l:
        return s[:l] + " ..."
    return s

def plain(text):
    return [{
        "type" : "Plain",
        "text" : text
      }]
