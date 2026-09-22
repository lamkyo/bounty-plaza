import pytest

from action_rubberbanding import Action, RubberbandController, Snapshot, Vec2


def test_actions_are_applied_immediately_and_sequence_numbers_are_monotonic():
    c = RubberbandController()
    first, second = c.apply_actions((Vec2(2, 0), Vec2(0, 3)))
    assert (first.sequence, second.sequence) == (1, 2)
    assert c.position == Vec2(2, 3)
    assert c.pending_actions == (first, second)


def test_reconciliation_keeps_unacknowledged_prediction():
    c = RubberbandController(position=Vec2(0, 0), correction_speed=0)
    c.apply_action(Vec2(5, 0))
    c.apply_action(Vec2(2, 0))
    c.reconcile(Snapshot(1, Vec2(4, 0)))
    assert c.pending_actions[0].sequence == 2
    assert c.position == Vec2(6, 0)


def test_rubberband_moves_toward_target_with_speed_cap():
    c = RubberbandController(position=Vec2(0, 0), max_correction_speed=2, correction_speed=100)
    c.reconcile(Snapshot(0, Vec2(10, 0)))
    assert c.tick(1) == Vec2(2, 0)
    assert c.tick(4) == Vec2(10, 0)


def test_snap_distance_can_apply_hard_correction():
    c = RubberbandController(position=Vec2(0, 0), snap_distance=5)
    c.reconcile(Snapshot(0, Vec2(10, 0)))
    assert c.position == Vec2(10, 0)


@pytest.mark.parametrize("kwargs", [
    {"correction_speed": -1}, {"max_correction_speed": 0}, {"snap_distance": -1}
])
def test_invalid_configuration_is_rejected(kwargs):
    with pytest.raises(ValueError):
        RubberbandController(**kwargs)


def test_negative_tick_is_rejected():
    with pytest.raises(ValueError):
        RubberbandController().tick(-0.01)


def test_action_is_value_object():
    assert Action(1, Vec2(1, 2)).delta == Vec2(1, 2)
