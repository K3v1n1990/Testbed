from __future__ import annotations

from typing import List

from .models import Exercise


_DEF_STEPS = {
    "sit": [
        "Hold a treat close to your dog's nose.",
        "Move your hand up, allowing their head to follow the treat and causing their bottom to lower.",
        "Say 'Sit', give the treat, and share affection once they sit.",
    ],
    "stay": [
        "Ask your dog to 'Sit'.",
        "Open your palm in front of you and say 'Stay'.",
        "Take a few steps back, return, reward, and gradually increase distance and duration.",
    ],
    "down": [
        "Hold a treat in your closed fist and place it up to your dog's nose.",
        "Move your hand to the floor so they follow.",
        "Slide your hand along the ground to encourage them to stretch forward into the down position.",
    ],
    "come": [
        "Put a leash on your dog and go down to their level.",
        "Gently pull the leash while saying 'Come'.",
        "When they reach you, reward with praise and treats.",
    ],
}


_DEF_GOALS = {
    "sit": "Dog sits on command for at least 5 seconds.",
    "stay": "Dog holds position until released, even with distractions.",
    "down": "Dog lays down calmly on cue.",
    "come": "Dog returns promptly when called.",
}


def default_exercises() -> List[Exercise]:
    return [
        Exercise(
            name="Sit",
            goal=_DEF_GOALS["sit"],
            steps=_DEF_STEPS["sit"],
            recommended_duration=3,
        ),
        Exercise(
            name="Stay",
            goal=_DEF_GOALS["stay"],
            steps=_DEF_STEPS["stay"],
            recommended_duration=5,
        ),
        Exercise(
            name="Down",
            goal=_DEF_GOALS["down"],
            steps=_DEF_STEPS["down"],
            recommended_duration=4,
        ),
        Exercise(
            name="Come",
            goal=_DEF_GOALS["come"],
            steps=_DEF_STEPS["come"],
            recommended_duration=5,
        ),
    ]
