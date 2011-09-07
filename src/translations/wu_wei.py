
import os
import sys

from PyQt4.QtCore import *


class WuWeiTranslation:

    kuaNumberToKuaTranslation = \
               {1 : "Creating",
                2 : "Open - Receptive - Yielding - Willing To Follow",
                3 : "Difficulty And Danger at the Beginning",
                4 : "Inexperience",
                5 : "Waiting in the Face of Danger",
                6 : "Argument",
                7 : "Collective Forces",
                8 : "Joining - Supporting - Uniting",
                9 : "Gentle Restraint",
                10 : "Walking Your Path",
                11 : "Peaceful Prosperity - Harmony",
                12 : "Separation - Decline",
                13 : "Mingling",
                14 : "Great Wealth",
                15 : "Modesty - Hubleness - Moderation",
                16 : "Enthusiasm - Revelry",
                17 : "Leading and Following",
                18 : "Correcting Deficiencies",
                19 : "Advance",
                20 : "Seeing Yourself Inwardly, Seeing The World Outwardly, Being Seen By Others For Whom You Set An Example",
                21 : "Punishment",
                22 : "Outer Refinement",
                23 : "Undermining - Overthrowing, Ending a Relationship",
                24 : "Return of the Light Force",
                25 : "Innocent Action, Unexpected Misfortune",
                26 : "Great Restraint",
                27 : "Providing Sustenance",
                28 : "Excess of Power",
                29 : "Water - Danger - The Abyss",
                30 : "Clarity - Adherence",
                31 : "Attraction - Influence",
                32 : "Duration",
                33 : "Withdrawal",
                34 : "Great Power",
                35 : "Great Progress",
                36 : "Persecution",
                37 : "The Family, The Organization",
                38 : "Alienation",
                39 : "Dangerous Adversity",
                40 : "Abatement of Danger",
                41 : "Decrease",
                42 : "Gain",
                43 : "Overthrow of Evil",
                44 : "Return of the Dark Force",
                45 : "Gathering Together - Joining",
                46 : "Advance",
                47 : "Oppression",
                48 : "The Well",
                49 : "Time For a Change",
                50 : "The Caldron",
                51 : "Shock - The Arousing",
                52 : "Moutain - Stopping Action, Thoughts Coming to Rest",
                53 : "Gradual Development",
                54 : "Joyous Movement",
                55 : "Abundance Peaked",
                56 : "The Stranger - The Traveler",
                57 : "Gently Penetrating",
                58 : "Joyousness - Pleasure",
                59 : "Dissolve - Disintegrate - Dissipate",
                60 : "Setting Limitations",
                61 : "Emptiness",
                62 : "Attention to Detail, The Performance of Small Tasks, Avoidance of Excesses",
                63 : "Completion, In Place - In Order",
                64 : "In Order - Out of Place"}


    def _getTranslationPath():

        # Return value.
        directory = ""
        
        (pathname, scriptname) = os.path.split(os.path.abspath(sys.argv[0]))

        translationDir = \
            pathname + \
            os.sep + ".." + \
            os.sep + "resources" + \
            os.sep + "texts" + \
            os.sep + "wu_wei"
        
        directory = os.path.abspath(translationDir)

        return directory
    
    def getUrl():
	# Unsupported at this time.

        #f = WuWeiTranslation._getTranslationPath() + \
        #    os.sep + "index.html"

        f = ""
	
        url = QUrl.fromLocalFile(f)

        return url

