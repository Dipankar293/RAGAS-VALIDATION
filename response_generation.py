from rag_search import search
from LLM_generation import generate_answer
from raga_setup import build_eval_dataset, run_evaluation


# 🔥 TEST QUERY
query = "What is research methodology?"

results = search(query)
answer = generate_answer(query, results)

dataset = build_eval_dataset(query, answer, results)

result = run_evaluation(dataset)

print(answer)

print("\n Evaluation Results:\n")
print(result)