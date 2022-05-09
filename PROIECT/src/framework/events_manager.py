import pygame


class EventsManager:
    __instance = None
    
    @classmethod
    def GetInstance(cls) -> 'EventsManager':
        if cls.__instance is None:
            cls.__instance = EventsManager()
        return cls.__instance
    

    def __init__(self) -> None:
        self.eventListeners = {}
    

    def AddListener(self, eventType: int, callable) -> None:
        if eventType in self.eventListeners:
            self.eventListeners[eventType].append(callable)
        else:
            self.eventListeners[eventType] = [callable]
    

    def RemoveListener(self, eventType: int, callable) -> None:
        if eventType in self.eventListeners and callable in self.eventListeners[eventType]:
            self.eventListeners[eventType].remove(callable)
    

    def ClearListeners(self) -> None:
        self.eventListeners = {}


    def ProcessEvents(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type in self.eventListeners:
                for callable in self.eventListeners[event.type]:
                    callable(event)
        return True
