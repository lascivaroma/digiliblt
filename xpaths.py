from glob import glob
from lxml.etree import parse
from MyCapytain.common.constants import XPATH_NAMESPACES


def compute_xpath(element):
    path = [element]
    parent = element
    while parent is not None:
        parent = parent.getparent()
        if parent is not None:
            path.append(parent)

    _path = []
    cnt_n = 1
    for p in path[::-1]:
        if p is not None:
            _path.append("tei:"+p.tag.replace("{http://www.tei-c.org/ns/1.0}", ""))
            if p.get("n") is not None and p.get("type") is not None:
                _path[-1] = _path[-1]+"[@n='$"+str(cnt_n)+"']"
                cnt_n += 1
    return "/".join(_path)


files = glob("sources/*/*.xml")

data = ["\t".join(["Filename"] + ["Xpath"]*3)]
for file in files:
    try:
        with open(file) as f:
            xml = parse(f)
    except Exception as E:
        print(file+" is failing")
        raise E

    divs = xml.xpath("//*[@type and @n]", namespaces=XPATH_NAMESPACES)
    divs += xml.xpath("//tei:p[@n]", namespaces=XPATH_NAMESPACES)

    if len(divs) == 0:
        # We use P
        xpaths = ["tei:TEI/tei:text/tei:body//tei:p[@n='$1']"]
    else:
        xpaths = sorted(list(set([compute_xpath(div) for div in divs])))

    data.append("\t".join([file] + xpaths))

with open("xpaths.csv", "w") as f:
    f.write("\n".join(data))
