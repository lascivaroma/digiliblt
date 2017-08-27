from glob import glob
from lxml.etree import parse
from MyCapytain.common.constants import XPATH_NAMESPACES


files = glob("sources/*/*.xml")

data = ["\t".join(["File", "Author", "Title"])]
for file in files:
    try:
        with open(file) as f:
            xml = parse(f)
    except Exception as E:
        print(file+" is failing")
        raise E

    title = xml.xpath("//tei:titleStmt/tei:title", namespaces=XPATH_NAMESPACES)
    author = xml.xpath("//tei:titleStmt/tei:author", namespaces=XPATH_NAMESPACES)
    description = xml.xpath("//tei:sourceDesc", namespaces=XPATH_NAMESPACES)

    if len(title) == 0:
        raise Exception("There is not title for %s" % file)
    else:
        title = title[0].text
    if len(author) == 0:
        author = "Anonyme"
    else:
        author = author[0].text
        if author is None:
            author = "Anonyme"

    data.append("\t".join([file, author, title]))

with open("sources.csv", "w") as f:
    f.write("\n".join(data))
