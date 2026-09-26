from rag.pipeline import rag_pipeline
from evaluation.dataset import EVALUATION_DATASET
import time


def evaluate():

    results = []

    for item in EVALUATION_DATASET:

        question = item["question"]
        expected = item["expected_answer"]

        start_time = time.perf_counter()

        result = rag_pipeline(question)

        end_time = time.perf_counter()

        latency = end_time - start_time

        answer = result["answer"]

        results.append(
    {
        "question": question,
        "expected_answer": expected,
        "actual_answer": answer,
        "citation_verified": result.get(
            "citation_verified",
            False
        ),
        "has_sources": len(
            result.get("sources", [])
        ) > 0,
        "latency": latency
    }
)

    return results


def calculate_metrics(results):

    total = len(results)

    citation_verified = sum(
        result["citation_verified"]
        for result in results
    )

    retrieval_success = sum(
        result["has_sources"]
        for result in results
    )

    citation_rate = (
        citation_verified / total * 100
        if total
        else 0
    )

    retrieval_rate = (
        retrieval_success / total * 100
        if total
        else 0
    )

    latencies = [
        result["latency"]
        for result in results
    ]

    average_latency = (
        sum(latencies) / len(latencies)
        if latencies
        else 0
    )

    minimum_latency = (
        min(latencies)
        if latencies
        else 0
    )

    maximum_latency = (
        max(latencies)
        if latencies
        else 0
    )

    return {
        "total_questions": total,
        "citation_verification_rate": citation_rate,
        "retrieval_success_rate": retrieval_rate,
        "average_latency": average_latency,
        "minimum_latency": minimum_latency,
        "maximum_latency": maximum_latency
    }


if __name__ == "__main__":

    results = evaluate()

    for i, result in enumerate(results, start=1):

        print(f"\n--- Evaluation {i} ---")

        print("Question:", result["question"])
        print("Expected:", result["expected_answer"])
        print("Actual:", result["actual_answer"])
        print(
            "Citation verified:",
            result["citation_verified"]
        )
        print(
            "Sources found:",
            result["has_sources"]
        )

    metrics = calculate_metrics(results)

    print("\n==============================")
    print("        EVALUATION METRICS")
    print("==============================")

    print(
        "Questions:",
        metrics["total_questions"]
    )

    print(
        "Citation verification rate:",
        f"{metrics['citation_verification_rate']:.1f}%"
    )

    print(
        "Retrieval success rate:",
        f"{metrics['retrieval_success_rate']:.1f}%"
    )

    print(
    "Average latency:",
    f"{metrics['average_latency']:.2f} seconds"
)

print(
    "Minimum latency:",
    f"{metrics['minimum_latency']:.2f} seconds"
)

print(
    "Maximum latency:",
    f"{metrics['maximum_latency']:.2f} seconds"
)