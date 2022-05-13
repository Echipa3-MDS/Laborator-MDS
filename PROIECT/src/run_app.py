from framework.app import App

if __name__ == "__main__":
    App.Init()
    appObj = App.GetInstance()
    appObj.Run()
    App.Quit()
