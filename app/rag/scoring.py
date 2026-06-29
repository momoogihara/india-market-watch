"""
scoring.py

Hybrid scoring utilities.

Responsibilities:
- Combine vector score and keyword score
- (Future) freshness score
- (Future) source reliability
"""

from typing import List, Dict


def apply_hybrid_score(results: List[Dict]) -> List[Dict]:
    """
    Calculate hybrid score for search results.

    Current score:
        final_score =
            0.6 * vector_score +
            0.4 * keyword_score
    """

    for result in results:

        metadata = result.get("metadata", {})

        vector_score = metadata.get("vector_score", 0.0)
        keyword_score = metadata.get("keyword_rank", 0.0)

        final_score = (
            0.6 * vector_score +
            0.4 * keyword_score
        )

        metadata["final_score"] = final_score

    return sorted(
        results,
        key=lambda r: r["metadata"].get("final_score", 0),
        reverse=True,
    )[:10]