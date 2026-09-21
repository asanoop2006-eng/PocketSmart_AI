def generate_home_recommendations(budget, room_type, lights, fans, tables):

    recommendations = []

    light_budget = budget * 0.20
    fan_budget = budget * 0.25
    table_budget = budget * 0.35
    decoration_budget = budget * 0.20

    recommendations.append({
        "category": "Lighting",
        "item": f"{lights} decorative LED light(s)",
        "budget": round(light_budget, 2),
        "platform": "Amazon / IKEA"
    })

    recommendations.append({
        "category": "Ceiling Fans",
        "item": f"{fans} ceiling fan(s)",
        "budget": round(fan_budget, 2),
        "platform": "Amazon / Flipkart"
    })

    recommendations.append({
        "category": "Furniture",
        "item": f"{tables} table(s)",
        "budget": round(table_budget, 2),
        "platform": "IKEA / Amazon"
    })

    recommendations.append({
        "category": "Decoration",
        "item": f"Decor items for your {room_type}",
        "budget": round(decoration_budget, 2),
        "platform": "IKEA / Amazon"
    })

    return recommendations
def generate_party_recommendations(budget, guests, event_type, venue):

    catering_budget = budget * 0.50
    decoration_budget = budget * 0.30
    entertainment_budget = budget * 0.20

    recommendations = [

        {
            "category": "Catering",
            "item": f"Food arrangements for {guests} guests",
            "budget": round(catering_budget, 2),
            "platform": "Swiggy / Zomato"
        },

        {
            "category": "Decoration",
            "item": f"Decoration for {event_type}",
            "budget": round(decoration_budget, 2),
            "platform": "Local Vendors / Online Stores"
        },

        {
            "category": "Entertainment",
            "item": f"Entertainment setup for your {event_type}",
            "budget": round(entertainment_budget, 2),
            "platform": "Local Service Providers"
        }

    ]

    return recommendations
def generate_jewelry_recommendations(budget, occasion, style, image_name):

    necklace_budget = budget * 0.45
    earrings_budget = budget * 0.25
    bracelet_budget = budget * 0.30

    recommendations = [
        {
            "category": "Necklace",
            "item": f"{style} necklace suitable for {occasion}",
            "budget": round(necklace_budget, 2),
            "platform": "Amazon / Flipkart"
        },
        {
            "category": "Earrings",
            "item": f"{style} earrings for your {occasion}",
            "budget": round(earrings_budget, 2),
            "platform": "Amazon / Flipkart"
        },
        {
            "category": "Bracelet",
            "item": f"{style} bracelet matching your occasion",
            "budget": round(bracelet_budget, 2),
            "platform": "Amazon / Flipkart"
        }
    ]

    return recommendations