import beanie
from typing import Type


async def save_many_to_collection(
        model: Type[beanie.Document], documents: list[beanie.Document]
        ) -> dict:
    """
        Saves multiple documents to a Beanie model collection.

        Args:
            model: The Beanie model representing the collection to save the documents to.
            documents: A list of Beanie documents to be saved to the collection.

        Returns:
            A dictionary containing a message indicating the success or failure of the
            operation.
        """
    try:
        if await model.count() > 0:
            return {"message": f"Collection '"
                               f"{model.__name__.replace('Document', '')}s' is not "
                               f"empty, "
                               f"no documents "
                               f"were added"}

        result = await model.insert_many(documents)
        return {"message": f"{len(result.inserted_ids)} documents added successfully "
                           f"to chosen collection"}

    except Exception as e:
        print(f"Error: {str(e)}")
        return {"error": {str(e)}}
