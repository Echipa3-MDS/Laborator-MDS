import unittest
import pygame

from framework.events_manager import EventsManager


class TestEventsManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('\nTesting Events Manager...\n')

    def setUp(self):
        if EventsManager.__dict__['_EventsManager__instance'] is not None:
            EventsManager.__dict__['_EventsManager__instance'].__init__()
        pygame.init()
    
    def tearDown(self):
        pygame.quit()


    def test_GetInstance(self):
        self.assertTrue(isinstance(EventsManager.GetInstance(), EventsManager))
    

    def test_Singleton(self):
        em1 = EventsManager.GetInstance()
        em2 = EventsManager.GetInstance()
        self.assertEqual(id(em1), id(em2))


    def test_AddListener(self):
        def eventListener(event: pygame.event.Event):
            pass

        EventsManager.GetInstance().AddListener(pygame.USEREVENT, eventListener)
        self.assertIn((pygame.USEREVENT, set((eventListener,))), EventsManager.GetInstance().eventListeners.items())
    

    def test_RemoveListener(self):
        def eventListener(event: pygame.event.Event):
            pass

        EventsManager.GetInstance().AddListener(pygame.USEREVENT, eventListener)
        EventsManager.GetInstance().RemoveListener(pygame.USEREVENT, eventListener)
        self.assertNotIn((pygame.USEREVENT, [eventListener]), EventsManager.GetInstance().eventListeners.items())
    

    def test_ClearListeners(self):
        def eventListener1(event: pygame.event.Event):
            pass
        def eventListener2(event: pygame.event.Event):
            pass
        
        EventsManager.GetInstance().AddListener(pygame.USEREVENT, eventListener1)
        EventsManager.GetInstance().AddListener(pygame.USEREVENT, eventListener2)
        EventsManager.GetInstance().ClearListeners()
        self.assertEqual(len(EventsManager.GetInstance().eventListeners.items()), 0)
    

    def test_ProcessEvents(self):
        def eventListener(event: pygame.event.Event):
            eventListener.counter += 1
        eventListener.counter = 0

        EventsManager.GetInstance().AddListener(pygame.USEREVENT, eventListener)
        pygame.event.post(pygame.event.Event(pygame.USEREVENT))
        pygame.event.post(pygame.event.Event(pygame.USEREVENT))
        pygame.event.post(pygame.event.Event(pygame.USEREVENT))
        EventsManager().GetInstance().ProcessEvents()
        self.assertEqual(eventListener.counter, 3)


    def test_EndAppEvent(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        self.assertFalse(EventsManager().GetInstance().ProcessEvents())
    

    def test_ContinueApp(self):
        pygame.event.post(pygame.event.Event(pygame.USEREVENT))
        self.assertTrue(EventsManager().GetInstance().ProcessEvents())
