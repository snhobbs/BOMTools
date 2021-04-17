# Bom Tools
## Purpose
Simplify the process of wrangling bills of materials with a platform and software agnostic tool.
This set of python tools allows for the generation of several types of BOMs for various different tasks.
The tool set is spreadsheet focused with spreadsheets used as the input and output formats.

The generic data transformations are handled by the package spreadsheet-wrangler[https://github.com/snhobbs/spreadsheet-wrangler].
The processes that are specific to bill of materials are handled here.

https://github.com/xesscorp/kicad-3rd-party-tools#bom-tools

## Usage Examples
### Expand a list of designators and unique identifiers with additional data
To expand a list of reference designators and unique identifier of a part (bom.xlsx) with
additionally available data (data_store.xlsx) using the merge function:
```
bom_compiler.py merge --on="pn" -b bom.xlsx -p data_store.xlsx
```
The column to use can be any unique identifier will work, examples are: manufacturers part number, internal part number, index to a database, etc.
Equivilent names for columns are passed to the tool in a JSON format. A file titled bom_Merged_data_store_On_pn.xlsx will be generated with this command.

### Compare the data in two BOMS
To compare the available data of two BOMs to compare function of spreadsheet_wrangler should be used. If a BOM was exported
and needs to be checked against another with questionable history run:
```
bom_compiler.py compare --first bom.xlsx --second bom_Merged_data_store_On_pn.xlsx
```
This will compare the original BOM with the merged one from the first example.
Comparisons are done column by column with rows lined up by the ref-des.
Discrepencies are printed to screen.

### Generate a BOM sorted by the type of parts
BOMs used for ordering, shipping, budgeting, or shipping to a CM are typically ordered by the type of part.

The ordering BOM sorts by reference designator and combines the BOM into unique part types.
This can then be used for ordering or quoting.
This can be passed to a tool like kicost or used with supplier BOM Managers or the Octopart BOM Manager (recommended).

To sort a BOM by the type of part and with a list of the reference designators run:
```
bom_compiler.py cluster --on="pn" -b bom.xlsx
```
NOTE: Currently the first matching row with in the column passed with the "--on" argument is used for all the matching parts. This is not necessarily correct.

### Compare a BOM sorted by the type of parts with a design BOM
To compare a BOM sorted by the part type (as shown above) with a BOM sorted by reference designator the BOM needs to be unpacked first and then compared.
To unpack run:
```
bom_compiler.py uncluster -b bom_Clustered_On_ref-des.xlsx
```
This will seperate the lines like the original bom.xlsx. This BOM can now be compared using the compare function described above.

NOTE: Note the data in each grouped row is duplicated for each clustered element. This is not necessarily correct if data was dissimilar and lost during the clustering step.

### Expanding a hierachical schematic
Hierarchical schematics involve many duplicated parts. Expanding takes an EDA BOM and a BOM with the base parts. The generated BOM has one line for each of the duplicated parts. Ex. an EDA BOM with a line like: 
```
C1_1, C1_2, C1_3, C4, C5_1, C5_2;...
```
and a unexpanded BOM with the matching part lines:
```
C1, C00-1U00-00, Susumu, 1234567
C4, C00-1U00-00, Susumu, 1234567
C5, C00-1U00-00, Susumu, 1234567
```
will expand to:
```
C1_1, C00-1U00-00, Susumu, 1234567
C1_2, C00-1U00-00, Susumu, 1234567
C1_3, C00-1U00-00, Susumu, 1234567
C4, C00-1U00-00, Susumu, 1234567
C5_1, C00-1U00-00, Susumu, 1234567
C5_2, C00-1U00-00, Susumu, 1234567
```
To do this run:
```
bom_compiler.py expand-hierarchy -m base_hierarchy.xlsx -e eda_bom.csv
```

### Extracting an assembly
Population options and different component choices are often designed into a single board. The master bom
contains a sub assembly field to note this. An empty field indicates the default choice and a value 
will overload this option for that subtype. This can be used for DNP also. 

Breaks apart a bom into a specified assembly. Blank assembly fields are taken as the default field with assembly names overriding the value. The reference designator and assembly have to be a unique combination. This tool allows for maintaining configuration options for a given design in one place, simplifying the BOM management. Exporting the assembly BOM will strip out all the parts that aren't part of the assembly.


To filter out the appropriate columns for an assembly run: 
```
bom_compiler.py filter --value="A" -b bom.xlsx
```
This will include all rows with the value A in the column "assembly" and any blank assembly entry is the value of ref-des is not already accounted for (the assembly value overloads the default).

## Assemblies
Have a master BOM type that then is processed to produce the other necessary types. This can be created from a data base and then altered.

## Workflow
During the schematic design the ref des, value, and requirements notes (this may be power dissipation requirements, low noise considerations, or accuracy as well as function) are written down. Known or essential parts are added. 

BOM Type: Notes BOM

After the initial design the BOM is filled out with parts being chosen and added to the BOM. Parts are added to a database with the footprint, value, 
manufacturer, manufacturer part number, and an internal part number if that is being used. 
The notes and important considerations generated in the Notes BOM are maintained with the additional columns added.
Parts can be copy and pasted from a data base or the fill function can be used to fill out the lines indexed by either the internal part number or the manufacturer part number.

It may be useful to iterate with the layout to finalize footprints and improve the design. Consistancy between the EDA and the paper BOM
should be automatically checkable. FIXME: A tool for joining the paper and EDA BOM on reference designator should be added.


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

