import beanie
from typing import Type


async def save_many_to_collection(
    doc: Type[beanie.Document], documents: list[beanie.Document]
) -> dict:
    """
    This Function is intended to be used only to initialise the collection documents
    created from a json file.
    """
    try:
        if await doc.count() > 0:
            return {"message": f"Collection '"
                               f"{doc.__name__.replace('Document','')}s' is not empty, "
                               f"no documents "
                               f"were added"}

        result = await doc.insert_many(documents)
        return {"message": f"{len(result.inserted_ids)} documents added successfully "
                           f"to {doc.__name__.replace('Document','')}s' collection"}

    except Exception as e:
        print(f"Error: {str(e)}")
        return {"error": {str(e)}}
