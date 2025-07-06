import os
import sys
from pathlib import Path

PACKAGE_PATH = Path(os.path.abspath(__file__)).parent
SOURCE_PATH = PACKAGE_PATH.parent

sys.path.append(str(SOURCE_PATH))

from enum import Enum


class EconomicScenario(Enum):
    """Economic scenarios affecting suspicion level across the network"""

    CRISIS = "crisis"
    RECESSION = "recession"
    NORMAL = "normal"
    GROWTH = "growth"
    BOOM = "boom"


def get_suspicion_level(scenario: EconomicScenario) -> float:
    """Get base suspicion level for scenario"""
    levels = {
        EconomicScenario.CRISIS: 0.9,  # Very high suspicion
        EconomicScenario.RECESSION: 0.7,  # High suspicion
        EconomicScenario.NORMAL: 0.5,  # Moderate suspicion
        EconomicScenario.GROWTH: 0.3,  # Low suspicion
        EconomicScenario.BOOM: 0.1,  # Very low suspicion
    }
    return levels[scenario]
