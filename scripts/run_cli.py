"""CLI runner for the agent."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents import ResearchAgent


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m scripts.run_cli \"your query\"")
        sys.exit(1)
    
    query = " ".join(sys.argv[1:])
    
    agent = ResearchAgent()
    result = agent.research(query, verbose=True)
    
    print("\n" + "=" * 60)
    print("REPORT")
    print("=" * 60)
    print(result["report"])
    print(f"\nSources: {len(result['sources'])}")


if __name__ == "__main__":
    main()
