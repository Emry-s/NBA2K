<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:template match="/">
    <html>
      <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <link rel="stylesheet" type="text/css" href="style.css"/>
      </head>
      <body>
        <h1>Best player by position</h1>
        <table>
          <tr>
            <th>Position</th>
            <th>Full Name</th>
            <th>Rating</th>
            <th>Team</th>
          </tr>
          <xsl:for-each select="NBA_Data/Best_player_by_position/Player">
            <tr>
              <td><xsl:value-of select="position"/></td>
              <td><xsl:value-of select="full_name"/></td>
              <td><xsl:value-of select="rating"/></td>
              <td><xsl:value-of select="team"/></td>
            </tr>
          </xsl:for-each>
        </table>
        <h1>In depth player review</h1>
        <table>
          <tr>
            <th>Full Name</th>
            <th>Jersey</th>
            <th>Team</th>
            <th>Height</th>
            <th>Weight</th>
            <th>Birthday</th>
            <th>Salary</th>
            <th>Country</th>
            <th>College</th>
          </tr>
          <xsl:for-each select="NBA_Data/In_depth_player_review/Player">
            <tr>
              <td><xsl:value-of select="full_name"/></td>
              <td><xsl:value-of select="jersey"/></td>
              <td><xsl:value-of select="team"/></td>
              <td><xsl:value-of select="height"/></td>
              <td><xsl:value-of select="weight"/></td>
              <td><xsl:value-of select="b_day"/></td>
              <td><xsl:value-of select="salary"/></td>
              <td><xsl:value-of select="country"/></td>
              <td><xsl:value-of select="college"/></td>
            </tr>
          </xsl:for-each>
        </table>
        <h1>Draft information</h1>
        <table>
          <tr>
            <th>Full Name</th>
            <th>Draft Year</th>
            <th>Draft Round</th>
            <th>Draft Peak</th>
            <th>College</th>
          </tr>
          <xsl:for-each select="NBA_Data/Draft_info/Player">
            <tr>
              <td><xsl:value-of select="full_name"/></td>
              <td><xsl:value-of select="draft_year"/></td>
              <td><xsl:value-of select="draft_round"/></td>
              <td><xsl:value-of select="draft_peak"/></td>
              <td><xsl:value-of select="college"/></td>
            </tr>
          </xsl:for-each>
        </table>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>

