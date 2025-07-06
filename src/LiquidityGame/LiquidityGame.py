import os
import sys
from pathlib import Path

PACKAGE_PATH = Path(os.path.abspath(__file__)).parent
SOURCE_PATH = PACKAGE_PATH.parent

sys.path.append(str(SOURCE_PATH))

from collections import defaultdict
from typing import Dict, List

import networkx as nx
import numpy as np
from Company import Company, PaymentDecision
from EconomicScenario import EconomicScenario, get_suspicion_level


class LiquidityGame:
    """Simplified Strategic Liquidity Game"""

    def __init__(self, network: nx.DiGraph, scenario: EconomicScenario):
        """Initialize game with network and scenario"""
        self.network = network
        self.scenario = scenario
        self.base_suspicion = get_suspicion_level(scenario)
        self.companies: Dict[str, Company] = {}
        self.iteration = 0
        self.history = []

        # Initialize companies
        self._initialize_companies()

    def _initialize_companies(self):
        """Initialize companies with enough capital to pay all debts"""
        # Create companies
        for node in self.network.nodes():
            self.companies[node] = Company(name=node)

        # Set up debtor/creditor relationships
        for debtor, creditor, data in self.network.edges(data=True):
            amount = data.get("amount", 10000)

            # Update relationships
            self.companies[creditor].debtors[debtor] = amount
            self.companies[debtor].creditors[creditor] = amount
            self.companies[debtor].debts += amount

        # Initialize capital - everyone has enough to pay all debts plus buffer
        for company in self.companies.values():
            company.capital = company.debts * 1.5  # 50% buffer
            company.suspicion_level = self.base_suspicion + np.random.normal(0, 0.05)
            company.suspicion_level = np.clip(company.suspicion_level, 0, 1)

    def detect_all_cycles(self) -> List[List[str]]:
        """Detect all cycles in the network"""
        cycles = []
        try:
            for cycle in nx.simple_cycles(self.network):
                if 3 <= len(cycle) <= 10:  # Reasonable cycle sizes
                    cycles.append(cycle)
        except Exception:
            pass
        return cycles

    def execute_iteration(self, use_bank_intervention: bool = False) -> Dict:
        """Execute one iteration of the game"""
        self.iteration += 1

        # Reset iteration counters
        for company in self.companies.values():
            company.payments_made = 0
            company.payments_received = 0
            company.payments_delayed_to_me = 0

        results = {
            "iteration": self.iteration,
            "payments_made": 0,
            "payments_delayed": 0,
            "total_payment_amount": 0.0,
            "cycles_resolved": 0,
        }

        # Bank intervention: if enabled, all cycles get liquidity
        bank_guaranteed_payments = set()
        if use_bank_intervention:
            cycles = self.detect_all_cycles()
            results["cycles_resolved"] = len(cycles)

            # All payments in cycles are guaranteed
            for cycle in cycles:
                for i in range(len(cycle)):
                    debtor = cycle[i]
                    creditor = cycle[(i + 1) % len(cycle)]
                    bank_guaranteed_payments.add((debtor, creditor))

        # All companies make payment decisions
        all_decisions = {}
        for company_name, company in self.companies.items():
            company_decisions = {}

            for creditor_name, debt_amount in company.creditors.items():
                # If bank guaranteed, always pay
                if (company_name, creditor_name) in bank_guaranteed_payments:
                    decision = PaymentDecision.PAY
                else:
                    # Make decision based on suspicion and expectations
                    decision = company.make_payment_decision(
                        creditor_name, debt_amount, self.companies
                    )

                company_decisions[creditor_name] = (decision, debt_amount)

            all_decisions[company_name] = company_decisions

        # Execute all payments
        for debtor_name, decisions in all_decisions.items():
            debtor = self.companies[debtor_name]

            for creditor_name, (decision, amount) in decisions.items():
                creditor = self.companies[creditor_name]

                if decision == PaymentDecision.PAY:
                    # Transfer money
                    debtor.capital -= amount
                    creditor.capital += amount

                    # Update counters
                    debtor.payments_made += 1
                    creditor.payments_received += 1
                    results["payments_made"] += 1
                    results["total_payment_amount"] += amount
                else:
                    # Payment delayed
                    creditor.payments_delayed_to_me += 1
                    results["payments_delayed"] += 1

        # Update reputations and suspicions
        for company in self.companies.values():
            company.update_reputation()
            company.update_suspicion()

        self.history.append(results)
        return results

    def analyze_network_cycles(self) -> Dict:
        """Analyze cycles in the network"""
        cycles = self.detect_all_cycles()

        # Count cycle participation
        cycle_participation = defaultdict(int)
        for cycle in cycles:
            for company in cycle:
                cycle_participation[company] += 1

        # Find hub nodes (in many cycles)
        hub_nodes = [node for node, count in cycle_participation.items() if count >= 5]
        mega_hubs = [node for node, count in cycle_participation.items() if count >= 10]

        return {
            "total_cycles": len(cycles),
            "companies_in_cycles": len(cycle_participation),
            "hub_nodes": hub_nodes,
            "mega_hubs": mega_hubs,
            "avg_cycle_participation": np.mean(list(cycle_participation.values()))
            if cycle_participation
            else 0,
            "max_cycle_participation": max(cycle_participation.values())
            if cycle_participation
            else 0,
        }

    def run_simulation(self, iterations: int = 100, use_bank: bool = False) -> Dict:
        """Run simulation and return summary statistics"""
        # Reset state
        self._initialize_companies()
        self.history = []

        # Run iterations
        for _ in range(iterations):
            self.execute_iteration(use_bank_intervention=use_bank)

        # Calculate summary statistics
        total_payments = sum(r["payments_made"] for r in self.history)
        total_delays = sum(r["payments_delayed"] for r in self.history)
        total_volume = sum(r["total_payment_amount"] for r in self.history)
        total_cycles_resolved = sum(r["cycles_resolved"] for r in self.history)

        # Final state
        avg_reputation = np.mean([c.reputation for c in self.companies.values()])
        avg_suspicion = np.mean([c.suspicion_level for c in self.companies.values()])
        avg_capital = np.mean([c.capital for c in self.companies.values()])

        return {
            "total_payments": total_payments,
            "total_delays": total_delays,
            "payment_rate": total_payments / (total_payments + total_delays)
            if (total_payments + total_delays) > 0
            else 0,
            "total_volume": total_volume,
            "cycles_resolved": total_cycles_resolved,
            "avg_final_reputation": avg_reputation,
            "avg_final_suspicion": avg_suspicion,
            "avg_final_capital": avg_capital,
        }

    def analyze_game(self) -> str:
        """Run complete analysis comparing with and without bank intervention"""
        report = []
        report.append("=" * 80)
        report.append("SIMPLE STRATEGIC LIQUIDITY GAME ANALYSIS")
        report.append(f"Economic Scenario: {self.scenario.value}")
        report.append(f"Base Suspicion Level: {self.base_suspicion}")
        report.append(
            f"Network: {len(self.companies)} companies, {len(self.network.edges())} debt relationships"
        )
        report.append("=" * 80)

        # Analyze network structure
        report.append("\n1. NETWORK STRUCTURE")
        report.append("-" * 40)

        cycle_analysis = self.analyze_network_cycles()
        report.append(f"Total cycles: {cycle_analysis['total_cycles']}")
        report.append(f"Companies in cycles: {cycle_analysis['companies_in_cycles']}")
        report.append(f"Hub nodes (5+ cycles): {len(cycle_analysis['hub_nodes'])}")
        report.append(
            f"Mega hub nodes (10+ cycles): {len(cycle_analysis['mega_hubs'])}"
        )
        report.append(
            f"Max cycle participation: {cycle_analysis['max_cycle_participation']}"
        )

        # Run without bank intervention
        report.append("\n2. SIMULATION WITHOUT BANK INTERVENTION")
        report.append("-" * 40)

        results_no_bank = self.run_simulation(iterations=100, use_bank=False)

        report.append(f"Total payments made: {results_no_bank['total_payments']}")
        report.append(f"Total payments delayed: {results_no_bank['total_delays']}")
        report.append(f"Payment rate: {results_no_bank['payment_rate'] * 100:.1f}%")
        report.append(f"Total payment volume: ${results_no_bank['total_volume']:,.2f}")
        report.append(
            f"Average final reputation: {results_no_bank['avg_final_reputation']:.3f}"
        )
        report.append(
            f"Average final suspicion: {results_no_bank['avg_final_suspicion']:.3f}"
        )

        # Run with bank intervention
        report.append("\n3. SIMULATION WITH BANK INTERVENTION")
        report.append("-" * 40)

        results_bank = self.run_simulation(iterations=100, use_bank=True)

        report.append(f"Total payments made: {results_bank['total_payments']}")
        report.append(f"Total payments delayed: {results_bank['total_delays']}")
        report.append(f"Payment rate: {results_bank['payment_rate'] * 100:.1f}%")
        report.append(f"Total payment volume: ${results_bank['total_volume']:,.2f}")
        report.append(f"Cycles resolved: {results_bank['cycles_resolved']}")
        report.append(
            f"Average final reputation: {results_bank['avg_final_reputation']:.3f}"
        )
        report.append(
            f"Average final suspicion: {results_bank['avg_final_suspicion']:.3f}"
        )

        # Comparison
        report.append("\n4. BANK INTERVENTION IMPACT")
        report.append("-" * 40)

        payment_improvement = (
            (results_bank["total_payments"] - results_no_bank["total_payments"])
            / results_no_bank["total_payments"]
            * 100
        )
        volume_improvement = (
            (results_bank["total_volume"] - results_no_bank["total_volume"])
            / results_no_bank["total_volume"]
            * 100
        )
        suspicion_reduction = (
            results_no_bank["avg_final_suspicion"] - results_bank["avg_final_suspicion"]
        )

        report.append(f"Payment increase: {payment_improvement:+.1f}%")
        report.append(f"Volume increase: {volume_improvement:+.1f}%")
        report.append(f"Suspicion reduction: {suspicion_reduction:+.3f}")
        report.append(
            f"Payment rate improvement: {(results_bank['payment_rate'] - results_no_bank['payment_rate']) * 100:+.1f} percentage points"
        )

        # Key insights
        report.append("\n5. KEY INSIGHTS")
        report.append("-" * 40)

        if payment_improvement > 0:
            report.append("✓ Bank intervention successfully broke payment gridlock")
            report.append("✓ Guaranteed cycle payments reduced overall suspicion")
            report.append("✓ Lower suspicion led to more payments throughout network")

        report.append(f"\nScenario Impact ({self.scenario.value}):")
        if self.base_suspicion > 0.6:
            report.append("- High initial suspicion created severe payment gridlock")
            report.append("- Bank intervention critical for maintaining payment flows")
        else:
            report.append("- Moderate suspicion still impacted payment efficiency")
            report.append("- Bank intervention improved overall liquidity")

        report.append("\nMechanism:")
        report.append(
            "1. High suspicion → companies delay payments (even with sufficient capital)"
        )
        report.append("2. Delays → increased suspicion → more delays (negative spiral)")
        report.append("3. Bank guarantees cycle payments → breaks the spiral")
        report.append(
            "4. Successful payments → reduced suspicion → more voluntary payments"
        )

        report.append("\n" + "=" * 80)

        return "\n".join(report)
