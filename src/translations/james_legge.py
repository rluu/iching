
import os
import sys

from PyQt4.QtCore import *


class JamesLeggeTranslation:

    kuaNumberToKuaTranslation = \
               {1 : "The Khien Hexagram",
                2 : "The Khwăn Hexagram",
                3 : "The Kun Hexagram",
                4 : "The Măng Hexagram",
                5 : "The Hsü Hexagram",
                6 : "The Sung Hexagram",
                7 : "The Sze Hexagram",
                8 : "The Pî Hexagram",
                9 : "The Hsiâo Khû Hexagram",
                10 : "The Lî Hexagram",
                11 : "The Thâi Hexagram",
                12 : "The Phî Hexagram",
                13 : "The Thung Zăn",
                14 : "The Tâ Yû Hexagram",
                15 : "The Khien Hexagram",
                16 : "The Yü Hexagram",
                17 : "The Sui Hexagram",
                18 : "The Kû Hexagram",
                19 : "The Lin Hexagram",
                20 : "The Kwân Hexagram",
                21 : "The Shih Ho Hexagram",
                22 : "The Pî Hexagram",
                23 : "The Po Hexagram",
                24 : "The Fû Hexagram",
                25 : "The Wû Wang Hexagram",
                26 : "The Tâ Khû Hexagram",
                27 : "The Î Hexagram",
                28 : "The Tâ Kwo Hexagram",
                29 : "The Khan Hexagram",
                30 : "The Lî Hexagram",
                31 : "The Hsien Hexagram",
                32 : "The Hăng Hexagram",
                33 : "The Thun Hexagram",
                34 : "The Tâ Kwang Hexagram",
                35 : "The Žin Hexagram",
                36 : "The Ming Î Hexagram",
                37 : "The Kiâ Zăn Hexagram",
                38 : "The Khwei Hexagram",
                39 : "The Kien Hexagram",
                40 : "The Kieh Hexagram",
                41 : "The Sun Hexagram",
                42 : "The Yî Hexagram",
                43 : "The Kwâi Hexagram",
                44 : "The Kâu Hexagram",
                45 : "The Žhui Hexagram",
                46 : "The Shăng Hexagram",
                47 : "The Khwăn Hexagram",
                48 : "The Žing Hexagram",
                49 : "The Ko Hexagram",
                50 : "The Ting Hexagram",
                51 : "The Kăn Hexagram",
                52 : "The Kăn Hexagram",
                53 : "The Kien Hexagram",
                54 : "The Kwei Mei Hexagram",
                55 : "The Făng Hexagram",
                56 : "The Lü Hexagram",
                57 : "The Sun Hexagram",
                58 : "The Tui Hexagram",
                59 : "The Hwân Hexagram",
                60 : "The Kieh Hexagram",
                61 : "The Kung Fû Hexagram",
                62 : "The Hsiâo Kwo Hexagram",
                63 : "The Kî Žî Hexagram",
                64 : "The Wei Žî Hexagram"}


    def _getTranslationPath():
        (pathname, scriptname) = os.path.split(sys.argv[0])

        directory = \
            os.path.abspath(pathname + \
                "/../resources/texts/james_legge/sacred-texts.com/ich/")

        return directory
    
    def getUrl():
        f = JamesLeggeTranslation._getTranslationPath() + \
           "/index.htm"

        url = QUrl.fromLocalFile(f)

        return url

