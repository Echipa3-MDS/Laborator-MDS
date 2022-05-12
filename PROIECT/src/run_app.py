from framework.app import App
from game.high_scores import HighScores

if __name__ == "__main__":
    App.Init()
    appObj = App.GetInstance()
    appObj.Run()
    App.Quit()
