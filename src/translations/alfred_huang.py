
import os
import sys

from PyQt5.QtCore import *


class AlfredHuangTranslation:

    kuaNumberToKuaTranslation = \
               {1 : "Initiating",
                2 : "Responding",
                3 : "Beginning",
                4 : "Childhood",
                5 : "Needing",
                6 : "Contention",
                7 : "Multitude",
                8 : "Union", 
                9 : "Little Accumulation",
                10 : "Fulfillment",
                11 : "Advance",
                12 : "Hindrance",
                13 : "Seeking Harmony",
                14 : "Great Harvest",
                15 : "Humbleness",
                16 : "Delight",
                17 : "Following",
                18 : "Remedying",
                19 : "Approaching",
                20 : "Watching",
                21 : "Eradicating",
                22 : "Adorning",
                23 : "Falling Away",
                24 : "Turning Back",
                25 : "Without Falsehood",
                26 : "Great Accumulation",
                27 : "Nourishing",
                28 : "Great Exceeding",
                29 : "Darkness",
                30 : "Brightness",
                31 : "Mutual Influence",
                32 : "Long Lasting",
                33 : "Retreat",
                34 : "Great Strength",
                35 : "Proceeding Forward",
                36 : "Brilliance Injured",
                37 : "Household",
                38 : "Diversity",
                39 : "Hardship",
                40 : "Relief",
                41 : "Decreasing",
                42 : "Increasing",
                43 : "Eliminating",
                44 : "Encountering",
                45 : "Bringing Together",
                46 : "Growing Upward",
                47 : "Exhausting",
                48 : "Replenishing",
                49 : "Abolishing the Old",
                50 : "Establishing the New",
                51 : "Taking Action",
                52 : "Keeping Still",
                53 : "Developing Gradually",
                54 : "Marrying Maiden",
                55 : "Abundance",
                56 : "Traveling",
                57 : "Proceeding Humbly",
                58 : "Joyful",
                59 : "Dispersing",
                60 : "Restricting",
                61 : "Innermost Sincerity",
                62 : "Little Exceeding",
                63 : "Already Fulfilled",
                64 : "Not Yet Fulfilled"}


    def _getTranslationPath():

        # Return value.
        directory = ""
        
        (pathname, scriptname) = os.path.split(os.path.abspath(sys.argv[0]))

        translationDir = \
            pathname + \
            os.sep + ".." + \
            os.sep + "resources" + \
            os.sep + "texts" + \
            os.sep + "alfred_huang"
        
        directory = os.path.abspath(translationDir)
        
        return directory
    
    def getUrl():
        f = AlfredHuangTranslation._getTranslationPath() + \
           os.sep + "TheCompleteIChing.htm"

        url = QUrl.fromLocalFile(f)

        return url


