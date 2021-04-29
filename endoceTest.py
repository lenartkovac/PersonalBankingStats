import pkgutil
import encodings
import os

def all_encodings():
    modnames = set([modname for importer, modname, iskpg in pkgutil.walk_packages(
        path = [os.path.dirname(encodings.__file__)], prefix='')])
    aliases = set(encodings.aliases.aliases.values())
    return modnames.union(aliases)

text = b'\x8a'
#text = b'\x8e'
for enc in all_encodings():
    try:
        msg = text.decode(enc)
    except Exception:
        continue
    if msg == 'Š':
    #if msg == 'Ž':
        print("decoding {t} with {enc} is {m}".format(t=text, enc=enc, m=msg))
    