import pygame

from framework.animation import Animation
from framework.rendered_object import RenderedObject
from framework.constants import *


class CoinMatrix(RenderedObject):
    
    coinFrames = None
    coinWidth = 30
    coinHeight = 30

    def __init__(self, posX: int, posY: int, width: int, height: int) -> None:
        super().__init__(posX, posY, width, height)
        
        self.__LoadCoinFrames()
        
        self.rows = height // CoinMatrix.coinHeight
        self.columns = width // CoinMatrix.coinWidth
        timeBetweenFrames = 0.1
        self.coinMatrix = [[
            Animation(j * CoinMatrix.coinWidth, i * CoinMatrix.coinHeight, CoinMatrix.coinWidth, CoinMatrix.coinHeight, CoinMatrix.coinFrames, timeBetweenFrames) 
            for j in range(self.columns)] 
            for i in range(self.rows)
        ]
        for row in self.coinMatrix:
            for coin in row:
                self.AttachObject(coin)
    

    def SetActive(self) -> None:
        for row in self.coinMatrix:
            for coin in row:
                if coin is not None:
                    coin.PlayAnimation()
    

    def CleanUp(self):
        for row in self.coinMatrix:
            for coin in row:
                if coin is not None:
                    coin.StopAnimation()


    def CheckCollision(self, playerRect: pygame.Rect) -> int | None:
        if not playerRect.colliderect(self._frame):
            return None
        nrCollided = 0
        for i in range(self.rows):
            for j in range(self.columns):
                if self.coinMatrix[i][j] is not None:
                    coinRect = self.coinMatrix[i][j].GetRect()
                    if playerRect.colliderect(coinRect):
                        self.coinMatrix[i][j].StopAnimation()
                        self.DetachObject(self.coinMatrix[i][j])
                        self.coinMatrix[i][j] = None
                        nrCollided += 1
        return (nrCollided if nrCollided != 0 else None)
                    
    
    def __LoadCoinFrames(self) -> None:
        if CoinMatrix.coinFrames is None:
            CoinMatrix.coinFrames = [
                pygame.image.load(RES_DIR + 'coin/coin_01.png').convert_alpha(),
                pygame.image.load(RES_DIR + 'coin/coin_02.png').convert_alpha(),
                pygame.image.load(RES_DIR + 'coin/coin_03.png').convert_alpha(),
                pygame.image.load(RES_DIR + 'coin/coin_04.png').convert_alpha(),
                pygame.image.load(RES_DIR + 'coin/coin_05.png').convert_alpha(),
                pygame.image.load(RES_DIR + 'coin/coin_06.png').convert_alpha(),
                pygame.image.load(RES_DIR + 'coin/coin_07.png').convert_alpha(),
                pygame.image.load(RES_DIR + 'coin/coin_08.png').convert_alpha()
            ]
