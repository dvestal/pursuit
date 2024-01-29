import unittest

from pursuit.game import Direction, Velocity, convert_velocity_direction

class TestDirectionVelocityConversion(unittest.TestCase):
    """Test names identify current and new direction"""

    def test_up_up(self):
        orig_vel = Velocity(0, 1)
        new_vel = convert_velocity_direction(orig_vel, Direction.UP, Direction.UP)
        self.assertEqual(new_vel, Velocity(0, 1))

    def test_up_right(self):
        orig_vel = Velocity(0, 1)
        new_vel = convert_velocity_direction(orig_vel, Direction.UP, Direction.RIGHT)
        self.assertEqual(new_vel, Velocity(1, 0))

    def test_up_down(self):
        orig_vel = Velocity(0, 1)
        new_vel = convert_velocity_direction(orig_vel, Direction.UP, Direction.DOWN)
        self.assertEqual(new_vel, Velocity(0, -1))

    def test_up_left(self):
        orig_vel = Velocity(0, 1)
        new_vel = convert_velocity_direction(orig_vel, Direction.UP, Direction.LEFT)
        self.assertEqual(new_vel, Velocity(-1, 0))

    def test_right_up(self):
        orig_vel = Velocity(1, 0)
        new_vel = convert_velocity_direction(orig_vel, Direction.RIGHT, Direction.UP)
        self.assertEqual(new_vel, Velocity(0, 1))

    def test_right_right(self):
        orig_vel = Velocity(1, 0)
        new_vel = convert_velocity_direction(orig_vel, Direction.RIGHT, Direction.RIGHT)
        self.assertEqual(new_vel, Velocity(1, 0))

    def test_right_down(self):
        orig_vel = Velocity(1, 0)
        new_vel = convert_velocity_direction(orig_vel, Direction.RIGHT, Direction.DOWN)
        self.assertEqual(new_vel, Velocity(0, -1))

    def test_right_left(self):
        orig_vel = Velocity(1, 0)
        new_vel = convert_velocity_direction(orig_vel, Direction.RIGHT, Direction.LEFT)
        self.assertEqual(new_vel, Velocity(-1, 0))

    def test_down_up(self):
        orig_vel = Velocity(0, -1)
        new_vel = convert_velocity_direction(orig_vel, Direction.DOWN, Direction.UP)
        self.assertEqual(new_vel, Velocity(0, 1))

    def test_down_right(self):
        orig_vel = Velocity(0, -1)
        new_vel = convert_velocity_direction(orig_vel, Direction.DOWN, Direction.RIGHT)
        self.assertEqual(new_vel, Velocity(1, 0))

    def test_down_down(self):
        orig_vel = Velocity(0, -1)
        new_vel = convert_velocity_direction(orig_vel, Direction.DOWN, Direction.DOWN)
        self.assertEqual(new_vel, Velocity(0, -1))

    def test_down_left(self):
        orig_vel = Velocity(0, -1)
        new_vel = convert_velocity_direction(orig_vel, Direction.DOWN, Direction.LEFT)
        self.assertEqual(new_vel, Velocity(-1, 0))

    def test_left_up(self):
        orig_vel = Velocity(-1, 0)
        new_vel = convert_velocity_direction(orig_vel, Direction.LEFT, Direction.UP)
        self.assertEqual(new_vel, Velocity(0, 1))

    def test_left_right(self):
        orig_vel = Velocity(-1, 0)
        new_vel = convert_velocity_direction(orig_vel, Direction.LEFT, Direction.RIGHT)
        self.assertEqual(new_vel, Velocity(1, 0))

    def test_left_down(self):
        orig_vel = Velocity(-1, 0)
        new_vel = convert_velocity_direction(orig_vel, Direction.LEFT, Direction.DOWN)
        self.assertEqual(new_vel, Velocity(0, -1))

    def test_left_left(self):
        orig_vel = Velocity(-1, 0)
        new_vel = convert_velocity_direction(orig_vel, Direction.LEFT, Direction.LEFT)
        self.assertEqual(new_vel, Velocity(-1, 0))


if __name__ == '__main__':
    unittest.main()
