<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns="http://www.tei-c.org/ns/1.0"
    exclude-result-prefixes="xs"
    xpath-default-namespace="http://www.tei-c.org/ns/1.0"
    version="2.0">
    <xsl:output
        method="xml"
        indent="yes"
        version="1.0"
        encoding="UTF-8"
        standalone="yes"
    />
    <xsl:param name="urn" />
    <xsl:template match="encodingDesc">
        <encodingDesc>
            <refsDecl n="CTS" />
            <xsl:apply-templates />
        </encodingDesc>
    </xsl:template>
    <xsl:template match="body">
        <body>
            <xsl:apply-templates select="@*|comment()"/>
            <div type="edition" xml:lang="lat">
                <xsl:attribute name="n" select="$urn" />
                <xsl:apply-templates select="node()"/>
            </div>
        </body>
    </xsl:template>
    
    <xsl:template match="node()|comment()|@*">
        <xsl:copy>
            <xsl:apply-templates />
        </xsl:copy>
    </xsl:template>
</xsl:stylesheet>