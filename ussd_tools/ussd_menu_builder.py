import json

class USSDMenu:
    def __init__(self, title):
        self.title = title
        self.options = []

    def add_option(self, key, label, next_menu=None):
        self.options.append({
            "key": key,
            "label": label,
            "next": next_menu
        })

    def to_dict(self):
        return {
            "title": self.title,
            "options": [
                {
                    "key": opt["key"],
                    "label": opt["label"],
                    "next": opt["next"].to_dict() if isinstance(opt["next"], USSDMenu) else opt["next"]
                } for opt in self.options
            ]
        }

    def render(self):
        output = f"CON {self.title}\n"
        for opt in self.options:
            output += f"{opt['key']}. {opt['label']}\n"
        return output

def build_sample_menu():
    main_menu = USSDMenu("Yendoukoa AI USSD Portal")

    services_menu = USSDMenu("Choose AI Service")
    services_menu.add_option("1", "Check Balance")
    services_menu.add_option("2", "Generate Social Post")
    services_menu.add_option("3", "Get Weather")

    monetization_menu = USSDMenu("Subscription Options")
    monetization_menu.add_option("1", "Daily Plan - $0.1")
    monetization_menu.add_option("2", "Weekly Plan - $0.5")
    monetization_menu.add_option("3", "Monthly Plan - $2.0")

    main_menu.add_option("1", "AI Services", services_menu)
    main_menu.add_option("2", "Monetization", monetization_menu)
    main_menu.add_option("3", "My Account")
    main_menu.add_option("4", "Exit")

    return main_menu

if __name__ == "__main__":
    menu = build_sample_menu()
    print("--- USSD Menu Preview ---")
    print(menu.render())
    print("\n--- JSON Structure ---")
    print(json.dumps(menu.to_dict(), indent=2))
