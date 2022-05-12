from framework.constants import *

class HighScores:
    
    __instance = None
    
    @classmethod
    def GetInstance(cls) -> 'HighScores':
        if cls.__instance is None:
            cls.__instance = HighScores()
        return cls.__instance

    @classmethod
    def GetScoreDict(cls) -> dict:
        highScoreFile = open(RES_DIR + 'high_scores.txt', 'r')
        continut = highScoreFile.read().strip().split('\n')
        highScoreFile.close()

        lista = {linie.split()[0] : int(linie.split()[1]) for linie in continut}
        lista = dict(sorted(lista.items(), key=lambda item: -item[1]))
        
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

        maxLenPlayer = max(maxLenPlayer, len('Username'))
        maxLenScore = max(maxLenScore, len('Scor'))
        row = ("{juc:<" + str(maxLenPlayer) + "s}: {scor:<" + str(maxLenScore) + "s}\n").format
        sir = row(juc='Username', scor='Scor')
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
    
    def Save(self) -> None:
        self.SaveScoreDict(self.highScore)
    
    def UpdateAndSave(self, highScore : dict) -> None:
        self.highScore = highScore
        self.Save()