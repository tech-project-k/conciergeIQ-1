import re

def analyze_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count occurrences of class="...-card"
    card_type = re.findall(r'class="([^"]+-card)"', content)
    print(f"File: {filepath}")
    print(f"Found cards: {len(card_type)}")
    # Print distinct card class names found
    print(f"Card classes: {set(card_type)}")

analyze_html(r"c:\Users\Jahnavi\OneDrive\Desktop\concierge\conciergeiq\src\app\components\hotel-card\hotel-card.component.html")
analyze_html(r"c:\Users\Jahnavi\OneDrive\Desktop\concierge\conciergeiq\src\app\components\destination-card\destination-card.component.html")
analyze_html(r"c:\Users\Jahnavi\OneDrive\Desktop\concierge\conciergeiq\src\app\components\event-card\event-card.component.html")
analyze_html(r"c:\Users\Jahnavi\OneDrive\Desktop\concierge\conciergeiq\src\app\components\restaurant-card\restaurant-card.component.html")
analyze_html(r"c:\Users\Jahnavi\OneDrive\Desktop\concierge\conciergeiq\src\app\components\review-card\review-card.component.html")
