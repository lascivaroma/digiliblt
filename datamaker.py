from csv import reader
import os
from subprocess import call
import shutil

textgroups = []
works = []
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
        print(textgroup)
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
            "java -jar /home/thibault/saxon9he.jar -s:{SOURCE} -xsl:general.xsl -o:data/{tg}/{wk}/{tg}.{wk}.digilibLT-lat1 urn='urn:cts:latinLit:{tg}.{wk}.digilibLT-lat1.xml'".format(
                SOURCE=path, tg=textgroup, wk=work
            ).split(" "))
