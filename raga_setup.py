from datasets import Dataset

from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision

def build_eval_dataset(query, answer, retrieved_chunks):
    contexts = [chunk["content"] for chunk in retrieved_chunks]

    data = {
        "question": [query],
        "answer": [answer],
        "contexts": [contexts],
        "ground_truth": ["Research methodology is a systematic approach used in research"]  # simple ground truth
    }

    return Dataset.from_dict(data)


def run_evaluation(dataset):
    result = evaluate(
        dataset,
        metrics=[
            faithfulness,
            answer_relevancy,
            context_precision
        ]
    )

    return result