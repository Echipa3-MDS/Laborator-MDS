import unittest


if __name__ == "__main__":

    testLoader = unittest.TestLoader()
    frameworkTestsPath = 'tests/framework_tests'
    frameworkSuite = testLoader.discover(frameworkTestsPath)

    testLoader = unittest.TestLoader()
    gameTestsPath = 'tests/game_tests'
    gameSuite = testLoader.discover(gameTestsPath)

    runner = unittest.TextTestRunner(None, True, 2)

    print("\n========================")
    print("=== Framework Tests ====")
    print("========================")
    runner.run(frameworkSuite)
    
    print("\n========================")
    print("====== Game Tests ======")
    print("========================")
    runner.run(gameSuite)
