import os
import sys
from pathlib import Path

PROJECT_PATH = Path(os.path.abspath(__file__)).parent

sys.path.append(str(PROJECT_PATH))

from datetime import datetime
from pathlib import Path

from LiquidityGame.EconomicScenario import EconomicScenario
from LiquidityGame.LiquidityGame import LiquidityGame
from NetworkConstructor.network import create_complex_network


def run_all_scenarios(
    dir_path: Path = Path(os.path.join(PROJECT_PATH, "analysis_results")),
):
    """Run analysis for all economic scenarios"""

    # Create network
    print("Creating complex network...")
    network = create_complex_network()

    # Analyze network structure
    print(
        f"Network has {network.number_of_nodes()} nodes and {network.number_of_edges()} edges"
    )

    # Run for each scenario
    all_results = []

    for scenario in EconomicScenario:
        print(f"\nAnalyzing {scenario.value} scenario...")

        game = LiquidityGame(network, scenario)
        analysis = game.analyze_game()

        # Save to file
        filename = f"analysis_{scenario.value}.txt"
        filepath = os.path.join(dir_path, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(analysis)

        print(f"Analysis saved to {filename}")
        all_results.append((scenario, analysis))

    # Create comprehensive report
    comprehensive = []
    comprehensive.append("=" * 80)
    comprehensive.append("COMPREHENSIVE LIQUIDITY GAME ANALYSIS - ALL SCENARIOS")
    comprehensive.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    comprehensive.append("=" * 80)

    for scenario, analysis in all_results:
        comprehensive.append(
            f"\n\n{'=' * 20} {scenario.value.upper()} SCENARIO {'=' * 20}"
        )
        comprehensive.append(analysis)

    with open(
        os.path.join(
            PROJECT_PATH,
            "analysis_results",
            "comprehensive_analysis.txt",
        ),
        "w",
        encoding="utf-8",
    ) as f:
        f.write("\n".join(comprehensive))

    print(
        f"\nComprehensive analysis saved to {
            os.path.join(
                PROJECT_PATH,
                'analysis_results',
                'comprehensive_analysis.txt',
            )
        }"
    )


if __name__ == "__main__":
    run_all_scenarios()
