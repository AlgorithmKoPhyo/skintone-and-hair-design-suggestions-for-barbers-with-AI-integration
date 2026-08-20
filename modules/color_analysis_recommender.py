# [cite: 3]"""Color analysis recommendation module placeholder."""

import json
import random
from pathlib import Path

PALETTES_PATH = Path(__file__).parent / "palettes.json"


def load_palettes():
    with open(PALETTES_PATH, "r", encoding="utf-8") as file:
        return json.load(file)

def normalize_undertone(undertone):

    if not undertone:
        return "warm"

    undertone = undertone.lower().strip()

    if "cool" in undertone:
        return "cool"

    if "neutral" in undertone:
        return "neutral"

    if "warm" in undertone:
        return "warm"

    return undertone

def normalize_gender(gender):
    
    if not gender:
        return "female"

    gender = gender.lower().strip()

    if gender not in ("male", "female"):
        return "female"

    return gender

def select_hair_colors(hair_colors, gender):

    selected_hair_colors = []

    for item in hair_colors:

        images = item.get("images", {})

        image = images.get(gender, "")

        selected_hair_colors.append({
            "name": item.get("name", ""),
            "image": image
        })

    return selected_hair_colors

def select_jewelry_images(jewelry, gender):
    selected_jewelry = []

    for item in jewelry:
        images = item.get("images", {})
        gender_images = images.get(gender, [])

        selected_image = (
            random.choice(gender_images)
            if gender_images
            else ""
        )

        selected_jewelry.append({
            "name": item.get("name", ""),
            "image": selected_image
        })

    return selected_jewelry

def select_occasion_jewelry(occasion_jewelry, gender):
    if not occasion_jewelry:
        return {}

    images = occasion_jewelry.get("images", {})
    gender_image = images.get(gender, "")

    return {
        "name": occasion_jewelry.get("name", ""),
        "image": gender_image
    }

def get_recommendations(undertone,gender="female"):

    undertone = normalize_undertone(undertone)
    gender = normalize_gender(gender)

    palettes = load_palettes()
    if not palettes:
        return {
            "status": "error",
            "message": "Unable to load palettes"
        }
    
    if undertone not in palettes:
        return {
            "status": "error",
            "message": f"Unsupported undertone: {undertone}"
        }

    palette = palettes[undertone]

    hair_colors = palette.get(
        "hair_colors",
        {}
    )
    selected_hair_colors = select_hair_colors(
        hair_colors,
        gender
    )

    jewelry = palette.get(
        "jewelry",
        []
    )

    selected_jewelry = select_jewelry_images(
        jewelry,
        gender
    )

    occasion_recommendations = palette.get(
        "occasion_recommendations",
        {}
    )

    for occasion, data in occasion_recommendations.items():
        data["jewelry"] = select_occasion_jewelry(
            data.get("jewelry", {}),
            gender
        )

    return {
        "status": "success",
        "undertone": undertone,
        "gender": gender,

         "description": palette.get(
            "description",
            ""
        ),

        "recommended_colors": palette.get(
            "recommended_colors",
            []
        ),


         "avoid_colors": palette.get(
            "avoid_colors",
            []
        ),

        "neutral_colors": palette.get(
            "neutral_colors_that_flatter",
            []
        ),

       "hair_colors": selected_hair_colors,

        "jewelry": selected_jewelry,

        "occasion_recommendations": occasion_recommendations
    }

# Testing 

# if __name__ == "__main__":

#     result = get_recommendations("warm","female")

#     import json
#     print(json.dumps(result, indent=4))
# ```[cite: 3]