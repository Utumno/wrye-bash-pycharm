# -*- coding: utf-8 -*-
#
# GPL License and Copyright Notice ============================================
#  This file is part of Wrye Bash.
#
#  Wrye Bash is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  Wrye Bash is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Wrye Bash; if not, write to the Free Software Foundation,
#  Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
#  Wrye Bash copyright (C) 2005-2009 Wrye, 2010-2014 Wrye Bash Team
#  https://github.com/wrye-bash
#
# =============================================================================
"""Merge two Pycharm dict files"""

import re
import codecs

reWordSearch = re.compile(r'      <w>(.+)</w>').search
words = set()
wordList = []
word1 = word2 = u''
file1 = file2 = True

with codecs.open(r'.__\__settings\.idea\dictionaries\MrD.xml', 'r',
                 'utf-8') as m1, codecs.open(
    # r'..\sync\.idea\dictionaries\MrD.xml', 'r', 'utf-8'
    r'.__\__settings\.idea\dictionaries\Bauglir.xml', 'r', 'utf-8'
) as m2:
    while file1:
        if not word1:
            line1 = next(m1, None)
            if line1 is None:
                file1 = False
                break
            search = reWordSearch(line1)
            if not search: continue
            word1 = search.group(1)
            if word1 in words:
                word1 = u''
                continue
            words.add(word1)
        if not file2:
            wordList.append(word1)
            word1 = u''
            continue
        while file2:
            if not word2:
                line2 = next(m2, None)
                if line2 is None:
                    file2 = False
                    break
                search = reWordSearch(line2)
                if not search: continue
                word2 = search.group(1)
                if word2 in words:
                    word2 = u''
                    continue
                words.add(word2)
            if word1 < word2:
                wordList.append(word1)
                word1 = u''
                break
            else:
                wordList.append(word2)
                word2 = u''
    m2 = m2 if file2 else m1
    if not word2: word2=word1
    while file2 or file1:
        if not word2:
            line2 = next(m2, None)
            if line2 is None: break
            else:
                search = reWordSearch(line2)
                if not search: continue
                word2 = search.group(1)
                if word2 in words:
                    word2 = u''
                    continue
        words.add(word2)
        wordList.append(word2)
        word2 = u''

with codecs.open(r'.__\__settings\.idea\dictionaries\MrDMixed.xml', 'w',
                 'utf-8') as out:
    out.write(
        '''<component name="ProjectDictionaryState">
  <dictionary name="MrD">
    <words>\n''')
    for w in wordList:
        out.write(u'      <w>' + unicode(w)+ u'</w>\n')
    out.write(
        '''     </words>
  </dictionary>
</component>''')
