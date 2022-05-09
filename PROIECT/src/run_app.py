from framework.app import App
from game.first_scene_example import FirstSceneExample


if __name__ == "__main__":
    App.Init()
    firstScene = FirstSceneExample()
    appObj = App.GetInstance()
    appObj.Run(firstScene)
    App.Quit()
