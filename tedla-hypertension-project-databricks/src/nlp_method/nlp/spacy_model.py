def download():
    """
    Download the spacy model
    """

    import os

    spacy_model: str | None = os.getenv("SPACY_MODEL", None)
    if spacy_model is None:
        raise ValueError("SPACY_MODEL environment variable is not set.")

    import importlib.util

    if importlib.util.find_spec(spacy_model) is None:
        import spacy
        import spacy.cli

        spacy.cli.download(spacy_model)  # type: ignore


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    download()
