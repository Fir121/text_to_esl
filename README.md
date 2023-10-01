# Repo for esl code tests

|_ Data Processor

    `base.py` - extracts video name, download link from zho website needs selenium to run and saves in pickle file
    `pickle_processor.py` - converts pickled dict to csv
    `download.py` - downloads videos from csv file containing video links

|_ OpenAISearch - *(recheck file paths! moved recently)*

    `database_embeds.py` - Generates embeddings based on the arabic word for all words in csv file
    `openai_search.py` - Searches word within the saved embeddings (also in repo) and returns top 3 with similarity score (effective method)

|_ Base Files

    `search.py` - Loads words stored in csv, uses Arabycia to search for words (not very effective)

Download Arabycia, and dependencies and remove extra code separately
Requirements.txt has a lot of libraries, might prefer to install as you use. Gitignore contains videos folder.
