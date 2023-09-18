def individual_serial(categoryEntity) -> dict :
    return {
        "id": str(categoryEntity["_id"]),
        "name": categoryEntity["name"],
        "createdAt": categoryEntity["createdAt"],
    }



def list_serial(categoryEntities) -> list :
    return [individual_serial(img) for img in categoryEntities]