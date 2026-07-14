# Point of Sale

A desktop point-of-sale app that generates itemized PDF receipts sized for an 80mm thermal receipt printer, and logs every transaction to `transactions.xlsx`.

## Option 1: Just run the app (no install needed)

Download the zip from the [Releases](../../releases) page, unzip it, and run `PointOfSale.exe`. Keep the `assets` folder next to it.

## Branding it as your own

Drop a `logo.png` (or `.jpg`/`.jpeg`/`.bmp`/`.gif`) into the `assets` folder and it will automatically show up in the app and print at the top of every receipt. No logo file is required — the app works fine without one.

Set your business name/address/phone in the app's Settings tab to print them under the logo too.

## Option 2: Run from source

Requires Python 3.

```
pip install -r requirements.txt
python billing_gui.py
```

A console-only version is also available (`bill_generator.py`) if you prefer a terminal-based flow instead of the GUI.

## Features

- Add, edit, and delete individual line items before generating a bill (no need to start over on a mistake)
- Live-updating item and grand totals as you type
- Discounts (flat or percent), tax, delivery charge, and payment method (Cash/Card/Other)
- Sequential invoice numbers printed on every receipt
- Void a bill from the Sales Summary tab (excluded from revenue totals, kept in the log for auditing)
- Configurable keyboard shortcuts for Add Item, Generate Bill, and Clear All (Settings tab)
- Arrow-key navigation between Product/Price/Quantity fields
- Every bill logs its line items to `transactions.xlsx`
- Receipts sized and cropped for 80mm thermal printers, with your logo and business info

## Rebuilding the standalone exe

```
pip install pyinstaller
pyinstaller --onefile --windowed --name PointOfSale billing_gui.py
```
