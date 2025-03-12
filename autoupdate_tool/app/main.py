import argparse
from pathlib import Path

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
        "A .csv table with integer index column and content column cotaining names of the microtopics"
    ))

    return parser.parse_args()


def main(args: argparse.Namespace) -> None:
    p_firestore_credentials = args.firebase_credentials
    p_microtopics_file = args.microtopics_file

    predictor = openai_predictor.OpenAIMicrotopicsPredictor(
        openai_key=args.openai_key,
        model='gpt-4o-mini',  # todo: de-hardcode
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