from csv import reader
import os
from subprocess import call
import shutil
from MyCapytain.common.reference import Citation
from MyCapytain.common.constants import Mimetypes
from tempfile import mkstemp
from shutil import move
from os import fdopen, remove

def replace(file_path, pattern, subst):
    #Create temp file
    fh, abs_path = mkstemp()
    with fdopen(fh,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(pattern, subst))
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)

textgroups = []
works = []

xpaths_dict = {}
with open("xpaths.csv") as f:
    xp = reader(f, delimiter="\t")
    next(xp)
    for line in xp:
        path, xpaths = line[0], line[1:]
        xpaths = [x.replace("body", "body/div") for x in xpaths]
        citation = Citation(name="unknown", refsDecl="#xpath({})".format(xpaths[0]))
        last = citation
        if len(xpaths) > 1:
            for ci in xpaths[1:]:
                last.child = Citation(name="unknown", refsDecl="#xpath({})".format(ci))
                last = last.child

        xpaths_dict[path] = citation

with open("urns.csv") as f:
    csv = reader(f, delimiter="\t")
    for line in csv:
        if len(line) == 0:
            continue
        try:
            textgroup, work, _, _, _, path, tgname, workname, *_ = tuple(line)
        except ValueError:
            print(line)
        if textgroup == "URN Author":
            continue
        # If the author is anonymous, the textgroup == the work

        if tgname.lower().startswith("anony"):
            tgname = workname
        # Create textgroup
        if textgroup not in textgroups:
            if not os.path.exists("data/{}".format(textgroup)):
                os.makedirs("data/{}".format(textgroup))
                with open("data/{}/__cts__.xml".format(textgroup), "w") as tg:
                    tg.write("""<textgroup xmlns="http://chs.harvard.edu/xmlns/cts" urn="urn:cts:latinLit:{}">
    <groupname xml:lang="lat">{}</groupname>
</textgroup>""".format(textgroup, tgname))
        if not work in works:
            if not os.path.exists("data/{}/{}".format(textgroup, work)):
                os.makedirs("data/{}/{}".format(textgroup, work))
                with open("data/{}/{}/__cts__.xml".format(textgroup, work), "w") as wk:
                    wk.write("""<work xmlns="http://chs.harvard.edu/xmlns/cts"
  groupUrn="urn:cts:latinLit:{tg}"
  urn="urn:cts:latinLit:{tg}.{wk}"
  xml:lang="lat"
>
    <title xml:lang="eng">{workname}</title>
    <edition 
      workUrn="urn:cts:latinLit:{tg}.{wk}" 
      urn="urn:cts:latinLit:{tg}.{wk}.digilibLT-lat1">
        <label xml:lang="lat">{workname}</label>
        <description xml:lang="lat">Edition from DigilibLT {digilibLT}</description>
    </edition>
</work>""".format(tg=textgroup, wk=work, workname=workname, digilibLT=path.split("/")[1]))
        else:
            print("Work {} is already annotated".format(work))

        # Copy the file
        call(
            "java -jar /home/thibault/saxon9he.jar -s:{SOURCE} -xsl:general.xsl -o:data/{tg}/{wk}/{tg}.{wk}.digilibLT-lat1.xml urn=urn:cts:latinLit:{tg}.{wk}.digilibLT-lat1".format(
                SOURCE=path, tg=textgroup, wk=work
            ).split(" "))

        newfile = "data/{tg}/{wk}/{tg}.{wk}.digilibLT-lat1.xml".format(tg=textgroup, wk=work)
        replace(newfile, '<refsDecl n="CTS"/>', '<refsDecl n="CTS">{}</refsDecl>'.format(xpaths_dict[path].export(Mimetypes.XML.TEI).replace("tei:", "")))