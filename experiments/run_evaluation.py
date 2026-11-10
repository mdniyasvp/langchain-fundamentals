
from ai_agent.agent.runner import run_agent
from tests.evaluation_cases import EVALUATION_CASES


def evaluate():

    results = []

    for case in EVALUATION_CASES:

        print(f"\nTest {case['id']}: {case['question']}")

        try:
            response = run_agent(case["question"])
            passed = True

            expected = case["expected_result"]

            if isinstance(expected, list):
                for item in expected:
                    if item.lower() not in response.lower():
                        passed = False
            else:
                if expected.lower() not in response.lower():
                    passed = False

            results.append({
                "id": case["id"],
                "category": case["category"],
                "passed": passed,
                "response": response,
            })

            print("PASS" if passed else "FAIL")
            print("Response:", response[:300])

        except Exception as error:

            results.append({
                "id": case["id"],
                "category": case["category"],
                "passed": False,
                "response": str(error),
            })

            print("ERROR:", error)

    total = len(results)
    passed = sum(item["passed"] for item in results)

    print("\n========== EVALUATION SUMMARY ==========")
    print(f"Total tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Pass rate: {(passed / total) * 100:.2f}%")

    print("\nCategory results:")

    categories = set(item["category"] for item in results)

    for category in sorted(categories):

        category_results = [
            item for item in results
            if item["category"] == category
        ]

        category_passed = sum(
            item["passed"] for item in category_results
        )

        print(
            f"{category}: "
            f"{category_passed}/{len(category_results)}"
        )


if __name__ == "__main__":
    evaluate()
