https://github.com/xesscorp/kicad-3rd-party-tools#bom-tools

Have a master BOM type that then is processed to produce the other necessary types. This can be created from a data base and then altered.

## BOM Types
- Big Bad BOM:
  - Contains all parts that we have.
  - This is currently generated from a database
- Master BOM:
  - Line number, ref des, internal part number, manufacturer, manufacturers part number, sub assembly
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

## Sub Assemblies
Population options and different component choices are often designed into a single board. The master bom
contains a sub assembly field to note this. An empty field indicates the default choice and a value 
will overload this option for that subtype. This can be used for DNP also.

## Goals
- make file to produce and check all the needed targets for a PCB
  - PCB manufacturing
  - BOM Ordering
  - Assembly documents
  - Check design rules
  - Generate different assembly type for the same board
  - Check all files are in zip
  - Cost estimates
