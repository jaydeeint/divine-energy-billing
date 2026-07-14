import billing_core as core


def get_items():
    items = []
    print("Enter items for the bill. Type 'reset' as the product names to clear all items and start over.\n")
    while True:
        names_raw = input("Product names (separated by ,): ").strip()
        if names_raw.lower() == "reset":
            if items:
                confirm_reset = input(f"Clear all {len(items)} item(s) entered so far? (y/n): ").strip().lower()
                if confirm_reset == "y":
                    items = []
                    print("All items cleared. Starting over.\n")
                else:
                    print("Reset cancelled.\n")
            else:
                print("No items to reset.\n")
            continue

        prices_raw = input("Prices (separated by ,): ").strip()
        quantities_raw = input("Quantities (separated by ,): ").strip()

        names = [n.strip() for n in names_raw.split(",") if n.strip()]
        price_tokens = [p.strip() for p in prices_raw.split(",") if p.strip()]
        quantity_tokens = [q.strip() for q in quantities_raw.split(",") if q.strip()]

        if not names or not (len(names) == len(price_tokens) == len(quantity_tokens)):
            print(
                f"Mismatch: {len(names)} name(s), {len(price_tokens)} price(s), "
                f"{len(quantity_tokens)} quantity(ies). Counts must match. Try again.\n"
            )
            continue

        try:
            prices = [float(p) for p in price_tokens]
            quantities = [int(q) for q in quantity_tokens]
        except ValueError:
            print("Prices must be numbers and quantities must be whole numbers. Try again.\n")
            continue

        batch = [{"name": n, "price": p, "quantity": q} for n, p, q in zip(names, prices, quantities)]

        print("\nConfirm these items:")
        for item in batch:
            subtotal = item["price"] * item["quantity"]
            print(f"  {item['name']}: {item['quantity']} x {item['price']:.2f} = {subtotal:.2f}")
        confirm = input("Add these items? (y/n): ").strip().lower()
        if confirm != "y":
            print("Discarded. Let's re-enter.\n")
            continue

        items.extend(batch)
        print(f"\n{len(batch)} item(s) added. Total items so far: {len(items)}\n")

        generate = input("Generate bill now? (y/n): ").strip().lower()
        if generate == "y":
            break
    return items


def get_number(prompt, default="0"):
    while True:
        raw = input(prompt).strip() or default
        try:
            return float(raw)
        except ValueError:
            print("Must be a number. Try again.")


def get_discount():
    while True:
        raw = input("Discount - flat amount or percent, e.g. 5 or 10% (blank for none): ").strip()
        try:
            core.parse_discount(raw, 1.0)
        except ValueError as e:
            print(str(e))
            continue
        return raw


def get_payment_method():
    options = core.PAYMENT_METHODS
    print("Payment method: " + ", ".join(f"{i + 1}. {m}" for i, m in enumerate(options)))
    raw = input(f"Choose (1-{len(options)}, blank for {options[0]}): ").strip()
    if not raw:
        return options[0]
    try:
        index = int(raw) - 1
        if 0 <= index < len(options):
            return options[index]
    except ValueError:
        pass
    return options[0]


def show_sales_summary():
    summary = core.get_sales_summary()
    if summary is None:
        print("No transactions recorded yet.")
        return

    today = summary["today"]
    month = summary["month"]
    all_time = summary["all_time"]
    voided = summary["voided"]

    print("\n--- Sales Summary ---")
    print(f"Today ({today['date']}): {today['count']} bill(s), Total: {today['total']:.2f}")
    print(f"This Month ({month['label']}): {month['count']} bill(s), Total: {month['total']:.2f}")
    print(f"All Time: {all_time['count']} bill(s), Total: {all_time['total']:.2f}")
    print(f"Voided: {voided['count']} bill(s), Total: {voided['total']:.2f}")
    print("---------------------\n")


def void_a_bill():
    recent = core.get_transactions_list(limit=15)
    if not recent:
        print("No transactions recorded yet.")
        return

    print("\nRecent bills:")
    for t in recent:
        status = " (already voided)" if t["voided"] else ""
        print(f"  {t['bill']}  |  {t['date']}  |  Total: {t['grand_total']:.2f}{status}")

    bill_name = input("\nEnter the exact bill filename to void (blank to cancel): ").strip()
    if not bill_name:
        return
    if core.void_bill(bill_name):
        print(f"Voided: {bill_name}")
    else:
        print("Bill not found.")


def delete_a_bill():
    recent = core.get_transactions_list(limit=15)
    if not recent:
        print("No transactions recorded yet.")
        return

    print("\nRecent bills:")
    for t in recent:
        status = " (voided)" if t["voided"] else ""
        print(f"  {t['bill']}  |  {t['date']}  |  Total: {t['grand_total']:.2f}{status}")

    bill_name = input("\nEnter the exact bill filename to permanently delete (blank to cancel): ").strip()
    if not bill_name:
        return
    confirm = input(
        f"Permanently delete '{bill_name}'? This removes it from transactions.xlsx and deletes its PDF. "
        "This cannot be undone. (y/n): "
    ).strip().lower()
    if confirm != "y":
        print("Cancelled.")
        return
    if core.delete_bill(bill_name):
        print(f"Deleted: {bill_name}")
    else:
        print("Bill not found.")


def make_bill():
    items = get_items()
    if not items:
        print("No items entered. Nothing to print.")
        return

    discount_raw = get_discount()
    tax_rate = get_number("Tax percent (blank for none): ")
    delivery_charge = get_number("Delivery charge (0 for none): ")
    payment_method = get_payment_method()

    output_path, totals, invoice_number = core.generate_bill(items, discount_raw, tax_rate, delivery_charge, payment_method)

    print(f"\nBill saved to: {output_path}")
    print(f"Invoice #: {invoice_number:06d}")
    print(f"Transaction logged to: {core.EXCEL_PATH}")
    print(f"Grand Total: {totals['grand_total']:.2f}")


def main():
    print("1. Generate a new bill")
    print("2. View sales summary")
    print("3. Void a bill")
    print("4. Delete a bill")
    choice = input("Choose an option (1/2/3/4): ").strip()

    if choice == "2":
        show_sales_summary()
        return
    if choice == "3":
        void_a_bill()
        return
    if choice == "4":
        delete_a_bill()
        return

    make_bill()


if __name__ == "__main__":
    main()
