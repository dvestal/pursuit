import unittest

from pursuit.game import Direction, Velocity, speed_from_velocity_and_direction

class TestVelocityConversion(unittest.TestCase):
    """Test names identify current and new direction"""

    def test_up(self):
        orig_vel = Velocity(0, 1)
        new_vel = speed_from_velocity_and_direction(orig_vel, Direction.UP)
        self.assertEqual(new_vel, 1)

    def test_down(self):
        orig_vel = Velocity(0, -1)
        new_vel = speed_from_velocity_and_direction(orig_vel, Direction.DOWN)
        self.assertEqual(new_vel, -1)

    def test_right(self):
        orig_vel = Velocity(1, 0)
        new_vel = speed_from_velocity_and_direction(orig_vel, Direction.RIGHT)
        self.assertEqual(new_vel, 1)

    def test_left(self):
        orig_vel = Velocity(-1, 0)
        new_vel = speed_from_velocity_and_direction(orig_vel, Direction.LEFT)
        self.assertEqual(new_vel, -1)


if __name__ == '__main__':
    unittest.main()
