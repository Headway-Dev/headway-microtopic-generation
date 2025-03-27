import json

from openai import OpenAI


SUPPORTED_MODELS = ['gpt-4o-mini']


class OpenAITopicsPredictor:
    def __init__(
            self,
            openai_key: str,
            model: str,
            en_topic_to_class: dict[str, int],
    ) -> None:
        assert model in SUPPORTED_MODELS, (
            f'{model} not supported. Must be one of {SUPPORTED_MODELS}.'
        )
        self._client = OpenAI(api_key=openai_key)
        self._model = model
        self._tpk_to_class = en_topic_to_class

    def predict(self, book_title: str, book_overview: str | None = None) -> list[int]:
        all_mircotopics_s = ''.join(f'{mt}\n ' for i, mt in enumerate(self._tpk_to_class.keys()))
        book_info = f'Title: {book_title}'
        if book_overview is not None:
            book_info += f'\nOverview:\n{book_overview}'
        response = self._client.chat.completions.create(
            model=self._model,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system",
                 "content": f"""Your task is to label the given book with approximately 8 exact tags from:\n {all_mircotopics_s}\n Prefer tags that are unique to this book. Sort them in the order of relevance. Return the list of relevant tags under key `result` as a JSON."""},
                {"role": "user", "content": book_info}
            ]
        )
        pred_topics = json.loads(response.choices[0].message.content)['result']
        valid_topics = [mt for mt in pred_topics if mt in self._tpk_to_class.keys()]
        topic_classes = [self._tpk_to_class[t] for t in valid_topics]
        return topic_classes
