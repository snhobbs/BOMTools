
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


## Parts Database
- Notes on parts and the barest additional data should be stored in a database. This could be a flat file loaded into memory or an actual database.
- A flat file has the advantage of being mergable with git. It is unlikely that the file will grow to the point that it will be impractical.

https://github.com/xesscorp/kicad-3rd-party-tools#bom-tools

Have a master BOM type that then is processed to produce the other necessary types. This can be created from a data base and then altered.

FIXME add subassemblies

## Design BOM Workflow
During the schematic design note down the ref des, value, and requirements note. This could become the design BOM
as the parts are chosen.

## Workflow
Some parts will be known and can be put in immediately, others will be filled in at the end.
Values are put in at the beginning on the schematic. The schematic is the master at this step.
It is useful to have an updated list of the parts that we've used previously with notes and
selected data.

BOM Type: Big Bad BOM

After the initial design then the BOM creation starts. This will usefully contain a list of values, footprints,
and specific parts for the none jelly beans. A list of notes as to important considerations should be maintained.
This should contain notes about the parts on the board with any restrictions they have.
For instance this may be power dissipation requirements, low noise considerations, or accuracy.

It may be useful to iterate with the layout to finalize footprints and improve the design. This will go along with the
BOM notes. The paper BOM should become the master during this stage. The EDA program will allow for a BOM export of some
variety.

BOM Type: Design Notes BOM

This BOM should be automatically checked against the paper BOM to ensure consistancy. This should check the value,
a preliminary check of the ref des, footprint, the internal part number or manufacturers part number. This will require an
EDA bom with this data and a paper BOM with the same data or a way to get it such as a supplier API (kicost?).

BOM Type: EDA Check BOM

After the parts placement has been decided the bom should be fleshed out. Internal part numbers should be 
generated. These internal part numbers should be added to the notes BOM. Ordering the parts should be considered.
Information for the generated BOMs are pulled from a database using the internal part number as the key.

BOM Type: Ordering BOM, Supplier BOMs, CM BOM, Budget BOM 

After the design is finalized a design BOM should be generated with all the data necessary to recreate the design and to debug the boards.
This will have information about the part as well as the normal data.

BOM Type: Design BOM

- EDA BOM checkable with design notes
  - Design should have footprint, value, ref des, and manu name & number


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

