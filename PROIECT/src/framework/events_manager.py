from matplotlib.pyplot import clabel
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
            self.eventListeners[eventType].add(callable)
        else:
            self.eventListeners[eventType] = set((callable,))

    
    def RemoveListener(self, eventType: int, callable) -> None:
        if eventType in self.eventListeners:
            self.eventListeners[eventType].discard(callable)
    

    def ClearListeners(self) -> None:
        self.eventListeners = {}


    def ProcessEvents(self) -> bool:
        listeners = dict()
        for k,v in self.eventListeners.items():
            listeners[k] = v.copy()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type in listeners:
                for callable in listeners[event.type]:
                    callable(event)
        return True
