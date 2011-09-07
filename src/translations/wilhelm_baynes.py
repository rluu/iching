
import os
import sys

from PyQt4.QtCore import *


class WilhelmBaynesTranslation:

    kuaNumberToKuaTranslation = \
               {1 : "The Creative",
                2 : "The Receptive",
                3 : "Difficulty at the Beginning",
                4 : "Youthful Folly",
                5 : "Waiting (Nourishment)",
                6 : "Conflict",
                7 : "The Army",
                8 : "Holding Together [Union]",
                9 : "The Taming Power of the Small",
                10 : "Treading [Conduct]",
                11 : "Peace",
                12 : "Standstill [Stagnation]",
                13 : "Fellowship with Men",
                14 : "Possession in Great Measure",
                15 : "Modesty",
                16 : "Enthusiasm",
                17 : "Following",
                18 : "Work on What Has Been Spoiled [Decay]",
                19 : "Approach",
                20 : "Contemplation (View)",
                21 : "Biting Through",
                22 : "Grace",
                23 : "Splitting Apart",
                24 : "Return (The Turning Point)",
                25 : "Innocence (The Unexpected)",
                26 : "The Taming Power of the Great",
                27 : "The Corners of the Mouth (Providing Nourishment)",
                28 : "Preponderance of the Great",
                29 : "The Abysmal (Water)",
                30 : "The Clinging, Fire",
                31 : "Influence (Wooing)",
                32 : "Duration",
                33 : "Retreat",
                34 : "The Power of the Great",
                35 : "Progress",
                36 : "Darkening of the Light",
                37 : "The Family [The Clan]",
                38 : "Opposition",
                39 : "Obstruction",
                40 : "Deliverance",
                41 : "Decrease",
                42 : "Increase",
                43 : "Break-through (Resoluteness)",
                44 : "Coming to Meet",
                45 : "Gathering Together [Massing]",
                46 : "Pushing Upward",
                47 : "Oppression (Exhaustion)",
                48 : "The Well",
                49 : "Revolution (Molting)",
                50 : "The Caldron",
                51 : "The Arousing (Shock, Thunder)",
                52 : "Keeping Still, Mountain",
                53 : "Development (Gradual Progress)",
                54 : "The Marrying Maiden",
                55 : "Abundance [Fullness]",
                56 : "The Wanderer",
                57 : "The Gentle (The Penetrating, Wind)",
                58 : "The Joyous, Lake",
                59 : "Dispersion [Dissolution]",
                60 : "Limitation",
                61 : "Inner Truth",
                62 : "Preponderance of the Small",
                63 : "After Completion",
                64 : "Before Completion"}


    def _getTranslationPath():

        # Return value.
        directory = ""
        
        (pathname, scriptname) = os.path.split(os.path.abspath(sys.argv[0]))

        translationDir = \
            pathname + \
            os.sep + ".." + \
            os.sep + "resources" + \
            os.sep + "texts" + \
            os.sep + "wilhelm_baynes" + \
            os.sep + "www2.unipr.it" + \
            os.sep + "~deyoung"
        
        directory = os.path.abspath(translationDir)

        return directory

    def getUrl():
        f = WilhelmBaynesTranslation._getTranslationPath() + \
            os.sep + "I_Ching_Wilhelm_Translation.html"

        url = QUrl.fromLocalFile(f)

        return url



