import unittest
from common.messager import MessageAnnouncer

class TestMessageAnnouncer(unittest.TestCase):

    def setUp(self):
        self.announcer = MessageAnnouncer()

    def test_listener_registration(self):
        self.assertEqual(len(self.announcer.listeners), 0, "Listeners list should be initially empty")

        q1 = self.announcer.listen()
        self.assertEqual(len(self.announcer.listeners), 1, "One listener should be registered")

        q2 = self.announcer.listen()
        self.assertEqual(len(self.announcer.listeners), 2, "Two listeners should be registered")

    def test_message_announcement(self):
        q1 = self.announcer.listen()
        q2 = self.announcer.listen()

        test_msg = "Hello, listeners!"
        self.announcer.announce(test_msg)

        self.assertEqual(q1.get_nowait(), test_msg, "First listener did not receive the correct message")
        self.assertEqual(q2.get_nowait(), test_msg, "Second listener did not receive the correct message")

    def test_queue_size_limit_and_cleanup(self):
        q = self.announcer.listen()

        # Fill the queue to its maximum size
        for _ in range(5):
            q.put_nowait("test message")

        self.assertEqual(len(self.announcer.listeners), 1, "Listener should be present before overflow")

        # This should trigger the removal of the listener
        self.announcer.announce("new message")

        self.assertEqual(len(self.announcer.listeners), 0, "Listener should be removed after queue overflow")
