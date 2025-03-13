# Summary micro-topics generation

## Book micro-topics update tool

This tool uses AI (OpenAI's GPT) to generate micro-topics for summaries.

It scans Firebase for books that don't have associated micro-topics in `common/title_relations`. Books are fetched from `books` collection in Firebase.
For every summary, it combines a set of predefined topics and book information to obtain several relevant topics.
AI has tendency to 'think up' (hallucinate) some micro-topics, so optional filtering ca be applied.

The app is dockerized. The makefile contains helpers for building and pushing docker images to GCP Artifact Registry. 


