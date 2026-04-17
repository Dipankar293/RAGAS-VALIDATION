from datasets import Dataset

from ragas import evaluate
from langchain_openai import OpenAIEmbeddings
from ragas.metrics import faithfulness, answer_relevancy, context_precision

from langchain_openai import ChatOpenAI
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper

evaluator_llm = LangchainLLMWrapper(
    ChatOpenAI(
        model="gpt-4o"   # use cheaper/faster model
    )
)

evaluator_embeddings = LangchainEmbeddingsWrapper(
    OpenAIEmbeddings(model="text-embedding-3-small")
)

def build_eval_dataset(query, answer, retrieved_chunks):
    contexts = [chunk["content"] for chunk in retrieved_chunks]

    data = {
        "question": [query],
        "answer": [answer],
        "contexts": [contexts],
        #"ground_truth": ["Research methodology is a systematic approach used in research"]  # simple ground truth
        
    }

    return Dataset.from_dict(data)


def run_evaluation(dataset):
    result = evaluate(
        dataset,
        metrics=[
            faithfulness,
            answer_relevancy
        ],
        llm=evaluator_llm,
        embeddings=evaluator_embeddings
    )

    return result