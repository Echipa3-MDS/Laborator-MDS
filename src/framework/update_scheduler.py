import pygame


class UpdateScheduler:
    __instance = None
    
    @classmethod
    def GetInstance(cls) -> 'UpdateScheduler':
        if cls.__instance is None:
            cls.__instance = UpdateScheduler()
        return cls.__instance
    

    def __init__(self) -> None:
        self.updatesScheduled = set()
        self.clock = pygame.time.Clock()
        self.deltaTime = 0
    

    def ScheduleUpdate(self, callable) -> None:
        self.updatesScheduled.add(callable)
    

    def UnscheduleUpdate(self, callable) -> None:
        self.updatesScheduled.discard(callable)
    

    def ClearSchedule(self) -> None:
        self.updatesScheduled = set()
    

    def UpdateAll(self) -> None:
        updates = self.updatesScheduled.copy()
        for callable in updates:
            callable(self.deltaTime)


    def CalculateDeltaTime(self) -> None:
        self.deltaTime = self.clock.tick() / 1000.0


    def GetDeltaTime(self) -> int:
        return self.deltaTime
    