def individual_serial(imageEntity) -> dict :
    return {
        "id": str(imageEntity['_id']),
        "name": imageEntity["name"],
        "link": imageEntity["link"],
        "correctness": float(imageEntity["correctness"]),
        "category": imageEntity["category"],
        "createdAt": imageEntity["createdAt"],
    }



def list_serial(imageEntities) -> list :
    return [individual_serial(img) for img in imageEntities]