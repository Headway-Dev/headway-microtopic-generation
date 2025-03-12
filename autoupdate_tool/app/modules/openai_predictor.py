import json

import loguru
from openai import OpenAI

from . import abstract



SUPPORTED_MODELS = ['gpt-4o-mini']


class OpenAIMicrotopicsPredictor(abstract.AbstracBookMicrotopicsPredictor):
    def __init__(
            self,
            openai_key: str,
            model: str,
            strict_mode: bool = True,
    ) -> None:
        assert model in SUPPORTED_MODELS, (
            f'{model} not supported. Must be one of {SUPPORTED_MODELS}.'
        )
        self._client = OpenAI(api_key=openai_key)
        self._strict_mode = strict_mode
        
    def predict(self, book: abstract.Book, microtopics: list[str]) -> list[str]:
        all_mircotopics_s = ''.join(f'{mt}\n ' for i, mt in enumerate(microtopics))
        response = self._client.chat.completions.create(
            model="gpt-4o",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": f"""Your task is to label the given book with approximately 8 exact tags from:\n {all_mircotopics_s}\n Sort the in the order of relevance. Return the list of relevant tags under key `result` as a JSON."""},
                {"role": "user", "content": f"Title: {book.title}"}
            ]
        )
        pred_microtopics = json.loads(response.choices[0].message.content)['result']

        if self._strict_mode:
            n_all = len(pred_microtopics)
            pred_microtopics = [mt for mt in pred_microtopics if mt in microtopics]
            n_strict = len(pred_microtopics)
            if n_all > n_strict:
                loguru.logger.debug(f'Using {n_strict} exact topics out of {n_all} predicted.')

        return pred_microtopics

