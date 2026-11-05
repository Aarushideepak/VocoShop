
import re

from inventory import (
    show_inventory,
    reduce_stock,
    increase_stock,
    get_product_details,
    check_low_stock
)

from speech import speak
from orders import create_order, show_orders, cancel_order
from sales import record_sale, get_daily_sales


# ----------------------------------
# 1. Product names in Kannada
# ----------------------------------

KANNADA_NAMES = {
    "rice": "ಅಕ್ಕಿ",
    "sugar": "ಸಕ್ಕರೆ",
    "milk": "ಹಾಲು",
    "oil": "ಎಣ್ಣೆ"
}

KANNADA_UNITS = {
    "kg": "ಕೆ.ಜಿ.",
    "kgs": "ಕೆ.ಜಿ.",
    "litre": "ಲೀಟರ್",
    "litres": "ಲೀಟರ್",
    "packet": "ಪ್ಯಾಕೆಟ್",
    "packets": "ಪ್ಯಾಕೆಟ್"
}


# ----------------------------------
# 2. Convert spoken numbers to digits
# ----------------------------------

NUMBER_WORDS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "fifteen": 15,
    "twenty": 20,
    "hundred": 100
}


def parse_quantity(value):
    value = value.lower().strip()

    if value in NUMBER_WORDS:
        return NUMBER_WORDS[value]

    try:
        return float(value)
    except ValueError:
        return None


# ----------------------------------
# 3. Kannada stock response
# ----------------------------------

def make_stock_response(product, quantity, unit):
    name = KANNADA_NAMES.get(product, product)

    kannada_unit = KANNADA_UNITS.get(
        unit.lower(),
        unit
    )

    return (
        f"ನಿಮ್ಮ ಅಂಗಡಿಯಲ್ಲಿ {quantity} "
        f"{kannada_unit} {name} ಉಳಿದಿದೆ."
    )


# ----------------------------------
# 4. Understand Kannada purchases
# ----------------------------------


def understand_kannada(command):

    products = {
        "ಅಕ್ಕಿ": "rice",
        "ಸಕ್ಕರೆ": "sugar",
        "ಹಾಲು": "milk",
        "ಎಣ್ಣೆ": "oil",
        "akki": "rice",
        "sakkare": "sugar",
        "haalu": "milk",
        "hallu": "milk",
        "enne": "oil"
    }

    product = None

    command = command.lower()

    for name, english_name in products.items():
        if name in command:
            product = english_name
            break

    if product is None:
        return None

    quantities = {
        "ಒಂದು": 1,
        "ಎರಡು": 2,
        "ಮೂರು": 3,
        "one": 1,
        "eradu": 2,
        "mooru": 3
    }

    quantity = None

    for word, number in quantities.items():
        if word in command:
            quantity = number
            break

    if quantity is None:
        return None

    return product, quantity

# ----------------------------------
# 5. Process Kannada purchases
# ----------------------------------

def process_purchase(command):

    result = understand_kannada(command)

    if result is None:
        print("Sorry, I couldn't understand the purchase.")
        speak("ಕ್ಷಮಿಸಿ, ನಿಮ್ಮ ಖರೀದಿಯ ವಿವರ ಅರ್ಥವಾಗಲಿಲ್ಲ.")
        return

    product, quantity = result

    details = get_product_details(product)

    if details is None:
        print(f"{product} is not available.")
        speak("ಕ್ಷಮಿಸಿ, ಈ ಸರಕು ಲಭ್ಯವಿಲ್ಲ.")
        return

    available, unit, price = details

    if unit.lower() not in ["kg", "kgs"]:
        print("Unit handling for this product needs configuration.")
        speak("ಈ ಸರಕಿನ ಅಳತೆಯ ವ್ಯವಸ್ಥೆ ಇನ್ನೂ ಸಿದ್ಧವಾಗಿಲ್ಲ.")
        return

    if quantity > available:
        print(f"Only {available} {unit} available.")
        speak(
            f"ಕ್ಷಮಿಸಿ, ನಿಮ್ಮ ಅಂಗಡಿಯಲ್ಲಿ {available} "
            f"ಕೆ.ಜಿ. {KANNADA_NAMES[product]} ಮಾತ್ರ ಲಭ್ಯವಿದೆ."
        )
        return

    total = quantity * price

    print(f"{quantity} {unit} of {product} costs ₹{total}.")

    speak(
        f"{quantity} ಕೆ.ಜಿ. {KANNADA_NAMES[product]} "
        f"ಬೆಲೆ {total} ರೂಪಾಯಿ."
    )

    confirmation = input(
        "KiranaVoice: Confirm purchase? (yes/no): "
    )

    if confirmation.lower().strip() in ["yes", "y"]:

        reduce_stock(product, quantity)
        order_id, total = create_order(product, quantity, price)
        record_sale(product, quantity, price, order_id)  

        print("Purchase confirmed. Thank you!")
        speak("ಖರೀದಿ ಯಶಸ್ವಿಯಾಗಿದೆ. ಧನ್ಯವಾದಗಳು!")
    else:
        print("Purchase cancelled.")
        speak("ಖರೀದಿ ರದ್ದಾಗಿದೆ.")


# ----------------------------------
# 6. Show complete inventory
# ----------------------------------

def handle_show_inventory():

    print("\nCurrent shop inventory:")

    show_inventory()

    spoken_parts = []

    for product in KANNADA_NAMES:

        details = get_product_details(product)

        if details:
            quantity, unit, price = details

            spoken_parts.append(
                make_stock_response(product, quantity, unit)
            )

    if spoken_parts:
        speak(" ".join(spoken_parts))

    else:
        speak("ನಿಮ್ಮ ಅಂಗಡಿಯಲ್ಲಿ ಯಾವುದೇ ಸರಕುಗಳಿಲ್ಲ.")


# ----------------------------------
# 7. Check stock of a product
# ----------------------------------

def handle_stock_check(product):

    details = get_product_details(product)

    if details is None:
        print(f"{product} is not available in inventory.")
        speak("ಕ್ಷಮಿಸಿ, ಈ ಸರಕು ನಿಮ್ಮ ಅಂಗಡಿಯಲ್ಲಿ ಲಭ್ಯವಿಲ್ಲ.")
        return

    quantity, unit, price = details

    print(f"{product}: {quantity} {unit} available.")
    print(f"Price: ₹{price} per {unit}")

    response = make_stock_response(
        product,
        quantity,
        unit
    )

    speak(response)


# ----------------------------------
# 8. Check whether command unit matches
# ----------------------------------

def units_match(command_unit, actual_unit):

    command_unit = command_unit.lower()
    actual_unit = actual_unit.lower()

    unit_groups = [
        {"kg", "kgs"},
        {"litre", "litres"},
        {"packet", "packets"}
    ]

    return any(
        command_unit in group and actual_unit in group
        for group in unit_groups
    )


# ----------------------------------
# 9. Process English commands
# ----------------------------------

def process_english_command(command):

    command = command.lower().strip()
    # LOW STOCK ALERT
    if "low stock" in command or "check low stock" in command:
        check_low_stock()
        return
    # SHOW ORDER HISTORY
    if "show orders" in command or "order history" in command:
        show_orders()
        return

    # CANCEL ORDER
    if "cancel order" in command:
        match = re.search(r"cancel order (one|two|three|four|five|\d+)", command)

        if match:
            order_text = match.group(1)

            number_words = {
                "one": 1,
                "two": 2,
                "three": 3,
                "four": 4,
                "five": 5
            }

            order_id = number_words.get(order_text, int(order_text) if order_text.isdigit() else None)   
            cancel_order(order_id)
        else:
            print("Please specify the order ID.")

        return

    # KEEP YOUR OTHER EXISTING COMMANDS BELOW THIS
    if (
        "daily sales" in command
        or "today's sales" in command
        or "today sales" in command
    ):

        total, count = get_daily_sales()

        speak(
            f"ಇವತ್ತಿನ ಒಟ್ಟು ಮಾರಾಟ {int(total)} ರೂಪಾಯಿ. "
            f"ಒಟ್ಟು {count} ವ್ಯವಹಾರಗಳು ನಡೆದಿವೆ."
        )


    # SHOW INVENTORY

    elif "show inventory" in command or "list inventory" in command:

        handle_show_inventory()

    # CHECK STOCK

    elif "check" in command or "stock" in command or "price" in command:

        match = re.search(
            r"(?:check|stock|price)(?:\s+of)?\s+(\w+)",
            command
        )

        if match:
            handle_stock_check(match.group(1))

        else:
            print("Please specify a product.")
            speak("ದಯವಿಟ್ಟು ಯಾವ ಸರಕು ಎಂದು ತಿಳಿಸಿ.")

    # SELL PRODUCTS

    elif "sell" in command or "reduce" in command:

        match = re.search(
            r"(?:sell|reduce)\s+(\d+(?:\.\d+)?|[a-z]+)\s+"
            r"(kg|kgs|litres?|packets?)\s+(?:of\s+)?(\w+)",
            command
        )

        if match:

            quantity = parse_quantity(match.group(1))
            unit = match.group(2)
            product = match.group(3)

            details = get_product_details(product)

            if quantity is None or quantity <= 0 or details is None:
                print("Invalid quantity or product.")
                return

            available, actual_unit, price = details

            if not units_match(unit, actual_unit):
                print("The unit does not match the inventory.")
                speak("ಅಳತೆಯ ಘಟಕ ಸರಿಯಾಗಿಲ್ಲ.")
                return

            if quantity > available:
                print(f"Only {available} {actual_unit} available.")
                speak("ಕ್ಷಮಿಸಿ, ಸಾಕಷ್ಟು ಸರಕು ಲಭ್ಯವಿಲ್ಲ.")
                return

            reduce_stock(product, quantity)

            total = quantity * price
            record_sale(product, quantity, price)

            details = get_product_details(product)

            remaining, actual_unit, price = details

            print(f"Remaining stock: {remaining} {actual_unit}.")

            speak(
                f"ಮಾರಾಟದ ನಂತರ {remaining} "
                f"{KANNADA_UNITS.get(actual_unit.lower(), actual_unit)} "
                f"{KANNADA_NAMES.get(product, product)} ಉಳಿದಿದೆ."
            )

        else:
            print("Example: Sell 2 kg rice.")
            speak("ದಯವಿಟ್ಟು ಸರಿಯಾದ ರೀತಿಯಲ್ಲಿ ಹೇಳಿ.")

    # ADD PRODUCTS

    elif command.startswith("add"):

        match = re.search(
            r"add\s+(\d+(?:\.\d+)?|[a-z]+)\s+"
            r"(kg|kgs|litres?|packets?)\s+(?:of\s+)?(\w+)",
            command
        )

        if match:

            quantity = parse_quantity(match.group(1))
            unit = match.group(2)
            product = match.group(3)

            details = get_product_details(product)

            if quantity is None or quantity <= 0 or details is None:
                print("Invalid quantity or product.")
                return

            available, actual_unit, price = details

            if not units_match(unit, actual_unit):
                print("The unit does not match the inventory.")
                speak("ಅಳತೆಯ ಘಟಕ ಸರಿಯಾಗಿಲ್ಲ.")
                return

            increase_stock(product, quantity)

            details = get_product_details(product)

            remaining, actual_unit, price = details

            print(f"Updated stock: {remaining} {actual_unit}.")

            speak(
                f"ಸರಕು ಸೇರಿಸಲಾಗಿದೆ. ಈಗ {remaining} "
                f"{KANNADA_UNITS.get(actual_unit.lower(), actual_unit)} "
                f"{KANNADA_NAMES.get(product, product)} ಇದೆ."
            )

        else:
            print("Example: Add 10 kg rice.")
            speak("ದಯವಿಟ್ಟು ಸರಿಯಾದ ರೀತಿಯಲ್ಲಿ ಹೇಳಿ.")

    # UNKNOWN COMMAND

    else:
        print("Sorry, I didn't understand that command.")
        speak("ಕ್ಷಮಿಸಿ, ನಿಮ್ಮ ಮಾತು ಅರ್ಥವಾಗಲಿಲ್ಲ.")


# ----------------------------------
# 10. Main command processor
# ----------------------------------

def process_command(command):

    command = command.strip()

    kannada_products = [
        "ಅಕ್ಕಿ",
        "ಸಕ್ಕರೆ",
        "ಹಾಲು",
        "ಎಣ್ಣೆ"
    ]

    if any(word in command.lower() for word in kannada_products) or any(
        word in command.lower()
        for word in ["akki", "sakkare", "haalu", "hallu", "enne"]
    ):

        process_purchase(command)
        return

    process_english_command(command.lower())


# ----------------------------------
# 11. Run assistant directly
# ----------------------------------

if __name__ == "__main__":

    print("===== KIRANAVOICE =====")
    print("Type 'exit' to stop.")

    while True:

        user_command = input("\nYou: ")

        if user_command.lower().strip() == "exit":

            print("KiranaVoice: Goodbye!")
            speak("ಧನ್ಯವಾದಗಳು. ಮತ್ತೆ ಭೇಟಿಯಾಗೋಣ!")

            break

        process_command(user_command)
