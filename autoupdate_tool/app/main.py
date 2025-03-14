import argparse
from pathlib import Path

import loguru

from modules import (
    openai_predictor,
    firebase_storages,
    local_microtopics_storage,
    update_manager
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--openai-key', required=True)
    
    parser.add_argument('--firebase-credentials', required=True, type=Path, help=(
        "Path to firebase certificate"
    ))

    parser.add_argument('--microtopics-file', required=True, type=Path, help=(
        "A .csv table with integer index column and content column containing names of the micro-topics"
    ))

    parser.add_argument('--strict-microtopics-filtering', action='store_true', help=(
        "Filter out predicted topics that are not strictly in the predefined list"
    ))

    return parser.parse_args()


def main(args: argparse.Namespace) -> None:
    p_firestore_credentials = args.firebase_credentials
    p_microtopics_file = args.microtopics_file
    strict_filtering = args.strict_microtopics_filtering

    if strict_filtering:
        loguru.logger.info('Using strict topic filtering')
    else:
        loguru.logger.info('Not using strict topic filtering')

    predictor = openai_predictor.OpenAIMicrotopicsPredictor(
        openai_key=args.openai_key,
        model='gpt-4o-mini',  # todo: de-hardcode
        strict_mode=strict_filtering,
    )
    books_storage = firebase_storages.FirebaseBookStorage(
        p_creds=p_firestore_credentials
    )
    microtopics_storage = local_microtopics_storage.LocalMicrotopicsStorage(
        p_microtopics_csv=p_microtopics_file
    )

    manager = update_manager.UpdateManager(
        predictor=predictor,
        books_storage=books_storage,
        microtopics_storage=microtopics_storage
    )
    manager.run()
    

if __name__ == '__main__':
    main(parse_args())
