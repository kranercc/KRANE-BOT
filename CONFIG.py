import pynput

CONFIG = {
    "window_name": "Team Fortress 2",
    "window_size": 500,
    'width': 500,
    'height': 450,
    "window_position": (0, 0),
    "confidence": 0.5,
    'object_class_id': 0,
    'aim_key': pynput.mouse.Button.right,
    'is_aiming': False,
    "threshold": 0.5,

    "shoot_inside_min_range": 30,
    'tend_to_aim_at_head': True,
    'snap_back_to_reality': False,
}
