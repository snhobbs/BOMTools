https://github.com/xesscorp/kicad-3rd-party-tools#bom-tools

Have a master BOM type that then is processed to produce the other necessary types. This can be created from a data base and then altered.

## BOM Types
- Master BOM:
  - Line number, ref des, internal part number, manufacturer, manufacturers part number, supplier, supplier part number, description
- Ordering/Budget BOM: Ordered by part type.
  - Line Number, Internal Part Number, Manufacturer, Manufacturers Number, Ref Des List, Quantity, Supplier, Supplier Part Number, Price
- Supplier BOM:
  - Identical to Ordering BOM filtered by supplier
- Design BOM: Ordered by Ref Des.
  - Line Number, Ref Des List, Manufacturer, Manufacturers Number, Quantity, Supplier, Price
- EDA BOM: Sorted by ref des, generated from the EDA program.
  - Ref Des, internal part number, value, footprint name
- EDA Check BOM
  - Ref Des, internal part number, value, footprint
- Net list: Node connections
- KiCost BOM
