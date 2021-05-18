<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns="http://www.tei-c.org/ns/1.0"
    xpath-default-namespace="http://www.tei-c.org/ns/1.0"
    exclude-result-prefixes="xs"
    version="2.0">
    <xsl:template match="refsDecl">
        <refsDecl n="CTS">
            <cRefPattern n="paragraph"
                matchPattern="(\w+)"
                replacementPattern="#xpath(/tei:TEI/tei:text/tei:body//tei:p[@n='$1'])">
                <p>This pointer pattern extracts unknown</p>
            </cRefPattern>
        </refsDecl>
        
    </xsl:template>
    <xsl:template match="body//p">
        <p n="{count(./preceding-sibling::p)+1}"><xsl:apply-templates  select="@*|node()|text()"/></p>
    </xsl:template>
    <xsl:template match="node()|text()|@*">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()|text()"/>
        </xsl:copy>
    </xsl:template>
</xsl:stylesheet>