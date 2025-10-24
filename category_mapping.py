class CategoryMapping:
    CATEGORIES = [
        "All Categories",
        "Plastic Bottle",
        "Carton",
        "Can",
        "Glass Bottle",
    ]

    MAPPING = {
        # Plastic Bottle
        "plastic_bottle": "Plastic Bottle",
        "bottle": "Plastic Bottle",
        "pet_bottle": "Plastic Bottle",
        "water_bottle": "Plastic Bottle",
        "plastic": "Plastic Bottle",

        # Carton
        "carton": "Carton",
        "tetra": "Carton",
        "tetra_pak": "Carton",
        "milk_carton": "Carton",
        "juice_carton": "Carton",

        # Can
        "can": "Can",
        "aluminum_can": "Can",
        "soda_can": "Can",
        "beer_can": "Can",
        "tin_can": "Can",
        "metal_can": "Can",

        # Glass Bottle
        "glass_bottle": "Glass Bottle",
        "glass": "Glass Bottle",
        "wine_bottle": "Glass Bottle",
        "beer_bottle": "Glass Bottle",

    }

    @classmethod
    def map_to_category(cls, detected_class: str) -> str:
        if not detected_class:
            return "Others"

        normalized = detected_class.lower().strip().replace(' ', '_')
        category = cls.MAPPING.get(normalized)
        return category if category else "Others"

    @classmethod
    def get_categories_without_all(cls) -> list:
        return [cat for cat in cls.CATEGORIES if cat != "All Categories"]