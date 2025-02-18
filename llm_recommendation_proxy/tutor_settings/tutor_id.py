from enum import Enum


class TutorID(Enum):
    MATH_PARENT_TOOL = "math-parent-tool"

    @classmethod
    def getMembers(cls):
        return [tid.value for tid in list(TutorID)]
