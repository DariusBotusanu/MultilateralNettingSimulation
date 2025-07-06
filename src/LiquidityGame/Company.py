import os
import sys
from pathlib import Path

PACKAGE_PATH = Path(os.path.abspath(__file__)).parent
SOURCE_PATH = PACKAGE_PATH.parent

sys.path.append(str(SOURCE_PATH))
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict

import numpy as np


class PaymentDecision(Enum):
    """The strategies a company may take at any given iteration"""

    PAY = "pay"
    DELAY = "delay"


@dataclass
class Company:
    """Representation of a company in the transaction network"""

    name: str
    reputation: float = 1.0  # [0,1] - how likely it is perceived to pay debts
    suspicion_level: float = 0.5  # [0,1] - level of suspicion it will not get paid
    capital: float = 0.0  # - amount of monet a company has
    debts: float = 0.0  # total amount owed to other companies
    debtors: Dict[str, float] = field(default_factory=dict)  # who owes them money
    creditors: Dict[str, float] = field(default_factory=dict)  # who they owe money

    # Track payment history
    payments_made: int = 0
    payments_received: int = 0
    payments_delayed_to_me: int = 0

    def make_payment_decision(
        self, creditor_name: str, debt_amount: float, companies: Dict[str, "Company"]
    ) -> PaymentDecision:
        """
        Random variable following a Bernoulli distribution (State Space {pay, delay}) with the probability to pay given by the follwing formula
        probability_to_pay = (1 - suspicion_level) * product(debtors' reputations)
        """
        # Calculate expected receipts based on debtors' reputations
        expected_receipts = 0.0
        for debtor_name, amount in self.debtors.items():
            if debtor_name in companies:
                expected_receipts += amount * companies[debtor_name].reputation

        # Decision based on suspicion and expected receipts
        debtors_reputation_product = 1.0
        if self.debtors:
            for debtor_name in self.debtors:
                if debtor_name in companies:
                    debtors_reputation_product *= companies[debtor_name].reputation

        # Probability to pay
        probability_to_pay = (1 - self.suspicion_level) * debtors_reputation_product

        # Make stochastic decision
        if np.random.random() < probability_to_pay:
            return PaymentDecision.PAY
        else:
            return PaymentDecision.DELAY

    def update_reputation(self):
        """Update reputation based on payment history"""
        if self.payments_made + self.payments_received > 0:
            payment_rate = (
                self.payments_made / len(self.creditors) if len(self.creditors) else 1
            )

            if payment_rate > 0.8:
                self.reputation = min(1.0, self.reputation * 1.05)
            elif payment_rate < 0.3:
                self.reputation = max(0.1, self.reputation * 0.9)

    def update_suspicion(self):
        """Update suspicion based on received payments"""
        if self.payments_received + self.payments_delayed_to_me > 0:
            receive_rate = self.payments_received / (
                self.payments_received + self.payments_delayed_to_me
            )
            # If receiving many payments, reduce suspicion
            if receive_rate > 0.7:
                self.suspicion_level = max(0.0, self.suspicion_level - 0.05)
            # If many delays, increase suspicion
            elif receive_rate < 0.3:
                self.suspicion_level = min(1.0, self.suspicion_level + 0.05)
