import pygame


class UpdateScheduler:
    __instance = None
    
    @classmethod
    def GetInstance(cls) -> 'UpdateScheduler':
        if cls.__instance is None:
            cls.__instance = UpdateScheduler()
        return cls.__instance
    

    def __init__(self) -> None:
        self.updatesScheduled = []
        self.clock = pygame.time.Clock()
        self.deltaTime = 0
    

    def ScheduleUpdate(self, callable) -> None:
        if callable not in self.updatesScheduled:
            self.updatesScheduled.append(callable)
    

    def UnscheduleUpdate(self, callable) -> None:
        if callable in self.updatesScheduled:
            self.updatesScheduled.remove(callable)
    

    def ClearSchedule(self) -> None:
        self.updatesScheduled = []
    

    def UpdateAll(self) -> None:
        for callable in self.updatesScheduled:
            callable(self.deltaTime)


    def CalculateDeltaTime(self) -> None:
        self.deltaTime = self.clock.tick() / 1000.0


    def GetDeltaTime(self) -> int:
        return self.deltaTime
    