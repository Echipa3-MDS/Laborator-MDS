from framework.constants import *
from os.path import exists

class HighScores:
    
    __instance = None
    
    @classmethod
    def GetInstance(cls) -> 'HighScores':
        if cls.__instance is None:
            cls.__instance = HighScores()
        return cls.__instance

    @classmethod
    def GetScoreDict(cls) -> dict:
        if exists(RES_DIR + 'high_scores.txt'):
            highScoreFile = open(RES_DIR + 'high_scores.txt', 'r')
            continut = highScoreFile.read().strip().split('\n')
            highScoreFile.close()

            if continut[0] != "":
                lista = {linie.split()[0] : int(linie.split()[1]) for linie in continut}
                lista = dict(sorted(lista.items(), key=lambda item: -item[1]))
            else:
                lista = {}
        else:
            lista = {}
        return lista
    
    @classmethod
    def SaveScoreDict(cls, dictList : dict) -> None:
        highScoreFile = open(RES_DIR + 'high_scores.txt', 'w')
        for player in dictList:
            scor = dictList[player]
            highScoreFile.write(player + ' ' + str(scor) + '\n')
        
        highScoreFile.close()
    
    @classmethod
    def ScoreToStringNLines(cls, dictList : dict, nrOfLines : int = -1, maxLenPlayer : int = 0, maxLenScore : int = 0) -> str:

        for it, player in enumerate(dictList):
            if it < nrOfLines or nrOfLines == -1:
                maxLenPlayer = max(maxLenPlayer, len(player))
                maxLenScore = max(maxLenScore, len(str(dictList[player])))
            else:
                break

        maxLenPlayer = max(maxLenPlayer, len('Jucator'))
        maxLenScore = max(maxLenScore, len('Scor'))
        row = ("{juc:<" + str(maxLenPlayer) + "s}: {scor:<" + str(maxLenScore) + "s}\n").format
        sir = row(juc='Jucator', scor='Scor')
        sir += ('-' * (maxLenPlayer + maxLenScore + 2)) + '\n'

        for it, player in enumerate(dictList):
            if it < nrOfLines or nrOfLines == -1:
                sir += row(juc=player, scor=str(dictList[player]))
            else:
                break


        return sir

    def __init__(self) -> None:
        self.highScore = self.GetScoreDict()
    
    def GetHighScore(self) -> dict:
        return self.highScore

    def GetHighScoreString(self, nrOfLines : int = -1) -> str:
        return self.ScoreToStringNLines(self.highScore, nrOfLines)

    def Update(self, highScore : dict) -> None:
        self.highScore = highScore
        self.highScore = dict(sorted(self.highScore.items(), key=lambda item: -item[1]))
    
    def Save(self) -> None:
        self.SaveScoreDict(self.highScore)
    
    def UpdateAndSave(self, highScore : dict) -> None:
        self.highScore = highScore
        self.highScore = dict(sorted(self.highScore.items(), key=lambda item: -item[1]))
        self.Save()