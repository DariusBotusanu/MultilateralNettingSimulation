import os
import sys
from pathlib import Path

PACKAGE_PATH = Path(os.path.abspath(__file__)).parent
SOURCE_PATH = PACKAGE_PATH.parent

sys.path.append(str(SOURCE_PATH))

from typing import Dict

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from EconomicScenario import EconomicScenario

from LiquidityGame import LiquidityGame
from NetworkConstructor.network import create_complex_network

# Set style for better-looking plots
plt.style.use("seaborn-v0_8-darkgrid")
sns.set_palette("husl")


def run_scenario_comparison():
    """Run simulations for all scenarios and create comparison plots"""

    # Create network
    print("Creating complex network...")
    network = create_complex_network()

    # Storage for results
    results_no_bank = {}
    results_with_bank = {}

    # Run simulations for each scenario
    for scenario in EconomicScenario:
        print(f"\nRunning simulations for {scenario.value} scenario...")

        game = LiquidityGame(network, scenario)

        # Run without bank intervention
        results_no_bank[scenario.value] = game.run_simulation(
            iterations=100, use_bank=False
        )

        # Reset and run with bank intervention
        game = LiquidityGame(network, scenario)
        results_with_bank[scenario.value] = game.run_simulation(
            iterations=100, use_bank=True
        )

    # Create plots
    create_comparison_plots(results_no_bank, results_with_bank)
    create_payment_dynamics_plot(network)
    create_network_health_dashboard(results_no_bank, results_with_bank)

    return results_no_bank, results_with_bank


def create_comparison_plots(results_no_bank: Dict, results_with_bank: Dict):
    """Create comprehensive comparison plots across scenarios"""

    scenarios = list(results_no_bank.keys())

    # Create figure with subplots
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle(
        "Economic Scenario Impact on Payment Network Behavior", fontsize=16, y=0.98
    )

    # 1. Payment Rate Comparison
    ax = axes[0, 0]
    payment_rates_no_bank = [
        results_no_bank[s]["payment_rate"] * 100 for s in scenarios
    ]
    payment_rates_bank = [results_with_bank[s]["payment_rate"] * 100 for s in scenarios]

    x = np.arange(len(scenarios))
    width = 0.35

    ax.bar(
        x - width / 2,
        payment_rates_no_bank,
        width,
        label="Without Bank",
        alpha=0.8,
        color="crimson",
    )
    ax.bar(
        x + width / 2,
        payment_rates_bank,
        width,
        label="With Bank",
        alpha=0.8,
        color="forestgreen",
    )

    ax.set_ylabel("Payment Rate (%)", fontsize=12)
    ax.set_title("Payment Success Rate by Scenario", fontsize=14, pad=10)
    ax.set_xticks(x)
    ax.set_xticklabels([s.capitalize() for s in scenarios], rotation=45)
    ax.legend()
    ax.grid(axis="y", alpha=0.3)

    # Add value labels on bars
    for i, (v1, v2) in enumerate(zip(payment_rates_no_bank, payment_rates_bank)):
        ax.text(
            i - width / 2, v1 + 1, f"{v1:.1f}%", ha="center", va="bottom", fontsize=9
        )
        ax.text(
            i + width / 2, v2 + 1, f"{v2:.1f}%", ha="center", va="bottom", fontsize=9
        )

    # 2. Total Payment Volume
    ax = axes[0, 1]
    volumes_no_bank = [
        results_no_bank[s]["total_volume"] / 1e9 for s in scenarios
    ]  # In billions
    volumes_bank = [results_with_bank[s]["total_volume"] / 1e9 for s in scenarios]

    ax.bar(
        x - width / 2,
        volumes_no_bank,
        width,
        label="Without Bank",
        alpha=0.8,
        color="darkblue",
    )
    ax.bar(
        x + width / 2,
        volumes_bank,
        width,
        label="With Bank",
        alpha=0.8,
        color="dodgerblue",
    )

    ax.set_ylabel("Payment Volume ($ Billions)", fontsize=12)
    ax.set_title("Total Transaction Volume by Scenario", fontsize=14, pad=10)
    ax.set_xticks(x)
    ax.set_xticklabels([s.capitalize() for s in scenarios], rotation=45)
    ax.legend()
    ax.grid(axis="y", alpha=0.3)

    # 3. Average Final Reputation
    ax = axes[0, 2]
    reputations_no_bank = [
        results_no_bank[s]["avg_final_reputation"] for s in scenarios
    ]
    reputations_bank = [results_with_bank[s]["avg_final_reputation"] for s in scenarios]

    ax.plot(
        scenarios,
        reputations_no_bank,
        "o-",
        linewidth=2,
        markersize=8,
        label="Without Bank",
        color="orangered",
    )
    ax.plot(
        scenarios,
        reputations_bank,
        "s-",
        linewidth=2,
        markersize=8,
        label="With Bank",
        color="green",
    )

    ax.set_ylabel("Average Reputation", fontsize=12)
    ax.set_title("Final Company Reputation by Scenario", fontsize=14, pad=10)
    ax.set_xticklabels([s.capitalize() for s in scenarios], rotation=45)
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 1.1)

    # 4. Average Final Suspicion
    ax = axes[1, 0]
    suspicions_no_bank = [results_no_bank[s]["avg_final_suspicion"] for s in scenarios]
    suspicions_bank = [results_with_bank[s]["avg_final_suspicion"] for s in scenarios]

    ax.plot(
        scenarios,
        suspicions_no_bank,
        "o-",
        linewidth=2,
        markersize=8,
        label="Without Bank",
        color="darkred",
    )
    ax.plot(
        scenarios,
        suspicions_bank,
        "s-",
        linewidth=2,
        markersize=8,
        label="With Bank",
        color="darkgreen",
    )

    ax.set_ylabel("Average Suspicion Level", fontsize=12)
    ax.set_title("Final Suspicion Levels by Scenario", fontsize=14, pad=10)
    ax.set_xticklabels([s.capitalize() for s in scenarios], rotation=45)
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 1.1)

    # 5. Bank Intervention Impact (Percentage Improvement)
    ax = axes[1, 1]
    payment_improvements = []
    volume_improvements = []

    for s in scenarios:
        payment_imp = (
            (
                results_with_bank[s]["total_payments"]
                - results_no_bank[s]["total_payments"]
            )
            / results_no_bank[s]["total_payments"]
            * 100
        )
        volume_imp = (
            (results_with_bank[s]["total_volume"] - results_no_bank[s]["total_volume"])
            / results_no_bank[s]["total_volume"]
            * 100
        )

        payment_improvements.append(payment_imp)
        volume_improvements.append(volume_imp)

    ax.bar(
        x - width / 2,
        payment_improvements,
        width,
        label="Payment Count",
        alpha=0.8,
        color="purple",
    )
    ax.bar(
        x + width / 2,
        volume_improvements,
        width,
        label="Payment Volume",
        alpha=0.8,
        color="indigo",
    )

    ax.set_ylabel("Improvement (%)", fontsize=12)
    ax.set_title("Bank Intervention Impact by Scenario", fontsize=14, pad=10)
    ax.set_xticks(x)
    ax.set_xticklabels([s.capitalize() for s in scenarios], rotation=45)
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    ax.axhline(y=0, color="black", linestyle="-", linewidth=0.5)

    # 6. Cycles Resolved
    ax = axes[1, 2]
    cycles_resolved = [results_with_bank[s]["cycles_resolved"] for s in scenarios]

    colors = plt.cm.viridis(np.linspace(0, 1, len(scenarios)))
    bars = ax.bar(scenarios, cycles_resolved, color=colors, alpha=0.8)

    ax.set_ylabel("Total Cycles Resolved", fontsize=12)
    ax.set_title("Payment Cycles Resolved with Bank Intervention", fontsize=14, pad=10)
    ax.set_xticklabels([s.capitalize() for s in scenarios], rotation=45)
    ax.grid(axis="y", alpha=0.3)

    # Add value labels
    for bar, value in zip(bars, cycles_resolved):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 5,
            f"{int(value)}",
            ha="center",
            va="bottom",
            fontsize=10,
        )

    plt.tight_layout()

    # Save figure
    output_dir = SOURCE_PATH / "analysis_results" / "plots"
    output_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(
        output_dir / "scenario_comparison_metrics.png", dpi=300, bbox_inches="tight"
    )
    print(
        f"Saved scenario comparison plot to {output_dir / 'scenario_comparison_metrics.png'}"
    )
    plt.close()


def create_payment_dynamics_plot(network):
    """Create a plot showing payment dynamics over time for different scenarios"""

    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle("Payment Dynamics Over Time Across Economic Scenarios", fontsize=16)

    scenarios = list(EconomicScenario)

    for idx, scenario in enumerate(scenarios):
        ax = axes[idx // 3, idx % 3]

        # Run simulation and collect iteration data
        game = LiquidityGame(network, scenario)

        # Run without bank
        game.run_simulation(iterations=50, use_bank=False)
        history_no_bank = game.history

        # Reset and run with bank
        game = LiquidityGame(network, scenario)
        game.run_simulation(iterations=50, use_bank=True)
        history_bank = game.history

        # Extract data
        iterations = range(1, len(history_no_bank) + 1)
        payments_no_bank = [h["payments_made"] for h in history_no_bank]
        payments_bank = [h["payments_made"] for h in history_bank]

        # Calculate moving average for smoother lines
        window = 5
        payments_no_bank_ma = (
            pd.Series(payments_no_bank).rolling(window=window, center=True).mean()
        )
        payments_bank_ma = (
            pd.Series(payments_bank).rolling(window=window, center=True).mean()
        )

        # Plot
        ax.plot(iterations, payments_no_bank, alpha=0.3, color="red", linewidth=1)
        ax.plot(
            iterations,
            payments_no_bank_ma,
            color="red",
            linewidth=2,
            label="Without Bank",
        )

        ax.plot(iterations, payments_bank, alpha=0.3, color="green", linewidth=1)
        ax.plot(
            iterations, payments_bank_ma, color="green", linewidth=2, label="With Bank"
        )

        ax.set_title(f"{scenario.value.capitalize()} Scenario", fontsize=12)
        ax.set_xlabel("Iteration")
        ax.set_ylabel("Payments Made")
        ax.legend(loc="best")
        ax.grid(True, alpha=0.3)

        # Add scenario info
        base_suspicion = game.base_suspicion
        ax.text(
            0.02,
            0.98,
            f"Base Suspicion: {base_suspicion:.1f}",
            transform=ax.transAxes,
            verticalalignment="top",
            bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
        )

    plt.tight_layout()

    # Save figure
    output_dir = SOURCE_PATH / "analysis_results" / "plots"
    output_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(
        output_dir / "payment_dynamics_over_time.png", dpi=300, bbox_inches="tight"
    )
    print(
        f"Saved payment dynamics plot to {output_dir / 'payment_dynamics_over_time.png'}"
    )
    plt.close()


def create_network_health_dashboard(results_no_bank: Dict, results_with_bank: Dict):
    """Create a comprehensive dashboard showing network health metrics"""

    fig = plt.figure(figsize=(20, 12))
    gs = fig.add_gridspec(3, 4, hspace=0.3, wspace=0.3)

    # Title
    fig.suptitle("Liquidity Network Health Dashboard", fontsize=20, y=0.98)

    scenarios = list(results_no_bank.keys())
    scenario_names = [s.capitalize() for s in scenarios]

    # 1. Payment Success Rate Heatmap
    ax1 = fig.add_subplot(gs[0, :2])

    payment_rates = []
    payment_rates.append([results_no_bank[s]["payment_rate"] * 100 for s in scenarios])
    payment_rates.append(
        [results_with_bank[s]["payment_rate"] * 100 for s in scenarios]
    )

    sns.heatmap(
        payment_rates,
        annot=True,
        fmt=".1f",
        cmap="RdYlGn",
        center=50,
        xticklabels=scenario_names,
        yticklabels=["Without Bank", "With Bank"],
        cbar_kws={"label": "Payment Rate (%)"},
        ax=ax1,
    )
    ax1.set_title("Payment Success Rate Heatmap", fontsize=14, pad=10)

    # 2. Suspicion vs Reputation Scatter
    ax2 = fig.add_subplot(gs[0, 2:])

    for i, scenario in enumerate(scenarios):
        # Without bank
        ax2.scatter(
            results_no_bank[scenario]["avg_final_suspicion"],
            results_no_bank[scenario]["avg_final_reputation"],
            s=200,
            alpha=0.6,
            label=f"{scenario} (No Bank)",
            marker="o",
            edgecolors="black",
            linewidth=1,
        )

        # With bank
        ax2.scatter(
            results_with_bank[scenario]["avg_final_suspicion"],
            results_with_bank[scenario]["avg_final_reputation"],
            s=200,
            alpha=0.6,
            label=f"{scenario} (Bank)",
            marker="s",
            edgecolors="black",
            linewidth=1,
        )

        # Draw arrows showing improvement
        ax2.annotate(
            "",
            xy=(
                results_with_bank[scenario]["avg_final_suspicion"],
                results_with_bank[scenario]["avg_final_reputation"],
            ),
            xytext=(
                results_no_bank[scenario]["avg_final_suspicion"],
                results_no_bank[scenario]["avg_final_reputation"],
            ),
            arrowprops=dict(arrowstyle="->", color="gray", alpha=0.5, lw=2),
        )

    ax2.set_xlabel("Average Suspicion Level", fontsize=12)
    ax2.set_ylabel("Average Reputation", fontsize=12)
    ax2.set_title("Suspicion vs Reputation Trade-off", fontsize=14, pad=10)
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(-0.05, 1.05)
    ax2.set_ylim(-0.05, 1.05)

    # 3. Total Delays Comparison
    ax3 = fig.add_subplot(gs[1, :2])

    delays_no_bank = [results_no_bank[s]["total_delays"] for s in scenarios]
    delays_bank = [results_with_bank[s]["total_delays"] for s in scenarios]

    x = np.arange(len(scenarios))
    width = 0.35

    bars1 = ax3.bar(
        x - width / 2,
        delays_no_bank,
        width,
        label="Without Bank",
        color="#ff6b6b",
        alpha=0.8,
    )
    bars2 = ax3.bar(
        x + width / 2, delays_bank, width, label="With Bank", color="#4ecdc4", alpha=0.8
    )

    ax3.set_ylabel("Total Payment Delays", fontsize=12)
    ax3.set_title("Payment Delays by Scenario", fontsize=14, pad=10)
    ax3.set_xticks(x)
    ax3.set_xticklabels(scenario_names, rotation=45)
    ax3.legend()
    ax3.grid(axis="y", alpha=0.3)

    # 4. Bank Intervention Efficiency
    ax4 = fig.add_subplot(gs[1, 2:])

    # Calculate efficiency metric (payment improvement / cycles resolved)
    efficiency = []
    for s in scenarios:
        payment_improvement = (
            results_with_bank[s]["total_payments"]
            - results_no_bank[s]["total_payments"]
        )
        cycles = (
            results_with_bank[s]["cycles_resolved"]
            if results_with_bank[s]["cycles_resolved"] > 0
            else 1
        )
        efficiency.append(payment_improvement / cycles)

    bars = ax4.bar(
        scenario_names,
        efficiency,
        color=plt.cm.plasma(np.linspace(0, 1, len(scenarios))),
        alpha=0.8,
    )

    ax4.set_ylabel("Payments per Cycle Resolved", fontsize=12)
    ax4.set_title("Bank Intervention Efficiency", fontsize=14, pad=10)
    ax4.set_xticklabels(scenario_names, rotation=45)
    ax4.grid(axis="y", alpha=0.3)

    # 5. Network Liquidity Score
    ax5 = fig.add_subplot(gs[2, :])

    # Create a composite liquidity score
    liquidity_scores_no_bank = []
    liquidity_scores_bank = []

    for s in scenarios:
        # Score based on payment rate, low suspicion, high reputation
        score_no_bank = (
            results_no_bank[s]["payment_rate"] * 0.5
            + (1 - results_no_bank[s]["avg_final_suspicion"]) * 0.3
            + results_no_bank[s]["avg_final_reputation"] * 0.2
        ) * 100

        score_bank = (
            results_with_bank[s]["payment_rate"] * 0.5
            + (1 - results_with_bank[s]["avg_final_suspicion"]) * 0.3
            + results_with_bank[s]["avg_final_reputation"] * 0.2
        ) * 100

        liquidity_scores_no_bank.append(score_no_bank)
        liquidity_scores_bank.append(score_bank)

    x = np.arange(len(scenarios))

    ax5.plot(
        x,
        liquidity_scores_no_bank,
        "o-",
        linewidth=3,
        markersize=10,
        label="Without Bank",
        color="#e74c3c",
    )
    ax5.plot(
        x,
        liquidity_scores_bank,
        "s-",
        linewidth=3,
        markersize=10,
        label="With Bank",
        color="#27ae60",
    )

    # Fill area between lines
    ax5.fill_between(
        x,
        liquidity_scores_no_bank,
        liquidity_scores_bank,
        alpha=0.2,
        color="green",
        where=np.array(liquidity_scores_bank) > np.array(liquidity_scores_no_bank),
    )

    ax5.set_ylabel("Network Liquidity Score (0-100)", fontsize=12)
    ax5.set_xlabel("Economic Scenario", fontsize=12)
    ax5.set_title("Overall Network Liquidity Health Score", fontsize=14, pad=10)
    ax5.set_xticks(x)
    ax5.set_xticklabels(scenario_names)
    ax5.legend()
    ax5.grid(True, alpha=0.3)
    ax5.set_ylim(0, 100)

    # Add score values
    for i, (v1, v2) in enumerate(zip(liquidity_scores_no_bank, liquidity_scores_bank)):
        ax5.text(i, v1 - 3, f"{v1:.1f}", ha="center", va="top", fontsize=9)
        ax5.text(i, v2 + 3, f"{v2:.1f}", ha="center", va="bottom", fontsize=9)

    plt.tight_layout()

    # Save figure
    output_dir = SOURCE_PATH / "analysis_results" / "plots"
    output_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(
        output_dir / "network_health_dashboard.png", dpi=300, bbox_inches="tight"
    )
    print(
        f"Saved network health dashboard to {output_dir / 'network_health_dashboard.png'}"
    )
    plt.close()


if __name__ == "__main__":
    # Run comparison analysis
    results_no_bank, results_with_bank = run_scenario_comparison()

    print(
        "\nAll plots have been generated and saved to the analysis_results/plots directory."
    )
