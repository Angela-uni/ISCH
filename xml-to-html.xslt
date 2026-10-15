<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tei="http://www.tei-c.org/ns/1.0"> 
    <xsl:output method="html" encoding="UTF-8" indent="yes"/>

    <xsl:template match="/">
        <html lang="en">
            <head>
                <meta charset="UTF-8"/>
                <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
                <title><xsl:value-of select="//tei:titleStmt/tei:title"/></title>
                <style>
                    * {
                        box-sizing: border-box;
                    }
                    body {
                        font-family: sans-serif;
                        line-height: 1.6;
                        max-width: 800px;
                        margin: 40px auto;
                        padding: 0 20px;
                        color: #222;
                    }
                    h1, h2, h3 {
                        margin-top: 1.5em;
                    }
                    p {
                        margin-bottom: 1em;
                        text-align: justify;
                    }
                    blockquote {
                        margin: 1em 0;
                        padding-left: 20px;
                        border-left: 3px solid #ccc;
                    }
                    /* Stile per indicare le omissioni */
                    .gap {
                        text-align: center;
                        font-style: italic;
                        color: #555;
                        margin: 1.5em 0;
                        padding: 5px;
                        border-top: 1px dashed #ccc;
                        border-bottom: 1px dashed #ccc;
                    }
                    /* Stile per far risaltare le entità senza colori vistosi */
                    .entity {
                        background-color: #f4f4f4;
                        border-bottom: 1px solid #888;
                        padding: 1px 3px;
                        border-radius: 2px;
                    }
                </style>
            </head>
            <body>
                <h1><xsl:value-of select="//tei:titleStmt/tei:title"/></h1>
                <xsl:apply-templates select="//tei:text/tei:body"/>
            </body>
        </html>
    </xsl:template>

    <!-- Manage of <div> -->
    <xsl:template match="tei:div">
        <div class="section">
            <xsl:apply-templates/>
        </div>
    </xsl:template>

    <xsl:template match="tei:div[@type='section']/tei:head">
        <h2><xsl:apply-templates/></h2>
    </xsl:template>

    <xsl:template match="tei:div[@type='subsection']/tei:head">
        <h3><xsl:apply-templates/></h3>
    </xsl:template>

    <!-- Manage of <p> -->
    <xsl:template match="tei:p">
        <p><xsl:apply-templates/></p>
    </xsl:template>

    <!-- Highlighted entities -->
    <xsl:template match="tei:title | tei:persName | tei:placeName | tei:objectName">
        <span class="entity"><xsl:apply-templates/></span>
    </xsl:template>

    <xsl:template match="tei:cit">
        <blockquote><xsl:apply-templates/></blockquote>
    </xsl:template>

    <xsl:template match="tei:quote">
        <p><xsl:apply-templates/></p>
    </xsl:template>

    <xsl:template match="tei:gap">
        <div class="gap">
            [Omission for <xsl:value-of select="@reason"/> reason]
        </div>
    </xsl:template>

    <xsl:template match="tei:listPerson | tei:listObject | tei:listPlace | tei:listBibl | tei:listRelation"/>

</xsl:stylesheet>