import unittest
import pygame

from framework.update_scheduler import UpdateScheduler


class TestUpdateScheduler(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('\nTesting Update Scheduler...\n')

    def setUp(self):
        if UpdateScheduler.__dict__['_UpdateScheduler__instance'] is not None:
            UpdateScheduler.__dict__['_UpdateScheduler__instance'].__init__()
        pygame.init()
    
    def tearDown(self):
        pygame.quit()


    def test_GetInstance(self):
        self.assertTrue(isinstance(UpdateScheduler.GetInstance(), UpdateScheduler))
    

    def test_Singleton(self):
        us1 = UpdateScheduler.GetInstance()
        us2 = UpdateScheduler.GetInstance()
        self.assertEqual(id(us1), id(us2))


    def test_ScheduleUpdate(self):
        def update(deltaTime: float):
            pass

        UpdateScheduler.GetInstance().ScheduleUpdate(update)
        self.assertIn(update, UpdateScheduler.GetInstance().updatesScheduled)
    

    def test_UnscheduleUpdate(self):
        def update(deltaTime: float):
            pass

        UpdateScheduler.GetInstance().ScheduleUpdate(update)
        UpdateScheduler.GetInstance().UnscheduleUpdate(update)
        self.assertNotIn(update, UpdateScheduler.GetInstance().updatesScheduled)


    def test_ClearSchedule(self):
        def update1(deltaTime: float):
            pass
        def update2(deltaTime: float):
            pass
        
        UpdateScheduler.GetInstance().ScheduleUpdate(update1)
        UpdateScheduler.GetInstance().ScheduleUpdate(update2)
        UpdateScheduler.GetInstance().ClearSchedule()
        self.assertEqual(len(UpdateScheduler.GetInstance().updatesScheduled), 0)

    
    def test_UpdateAll(self):
        def update(deltaTime: float):
            update.counter += 1
        update.counter = 0

        UpdateScheduler.GetInstance().ScheduleUpdate(update)
        UpdateScheduler.GetInstance().UpdateAll()
        UpdateScheduler.GetInstance().UpdateAll()
        self.assertEqual(update.counter, 2)

    
    def test_CalculateDeltaTime(self):
        UpdateScheduler.GetInstance().CalculateDeltaTime()
        self.assertEqual(UpdateScheduler.GetInstance().deltaTime, UpdateScheduler.GetInstance().clock.get_time() / 1000.0)
    

    def test_GetDeltaTime(self):
        self.assertEqual(UpdateScheduler.GetInstance().GetDeltaTime(), UpdateScheduler.GetInstance().deltaTime)
