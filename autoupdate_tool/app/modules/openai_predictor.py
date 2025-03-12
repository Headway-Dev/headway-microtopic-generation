import json

from openai import OpenAI

from . import abstract



SUPPORTED_MODELS = ['gpt-4o-mini']


class OpenAIMicrotopicsPredictor(abstract.AbstracBookMicrotopicsPredictor):
    def __init__(
            self,
            openai_key: str,
            model: str,
    ) -> None:
        assert model in SUPPORTED_MODELS, (
            f'{model} not supported. Must be one of {SUPPORTED_MODELS}.'
        )
        self._client = OpenAI(api_key=openai_key)
        
    def predict(self, book: abstract.Book, microtopics: list[str]) -> list[str]:
        all_mircotopics_s = ''.join(f'{i+1}. {mt}\n ' for i, mt in enumerate(microtopics))
        response = self._client.chat.completions.create(
            model="gpt-4o",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": f"""Your task is to label the given book with approximately 8 exact tags from {all_mircotopics_s}. Sort the in the order of relevance. Return the list of relevant tags under key `result` as a JSON."""},
                {"role": "user", "content": f"Title: {book.title}"}
            ]
        )
        pred_microtopics = json.loads(response.choices[0].message.content)['result']

        return pred_microtopics

