---
title: BOM Checking & Ordering
author: Simon Hobbs, ElectroOptical Innovations
date: 2022-11-07
---

In the board design process you start with schematic and a rough bill of materials (BOM).
As the design progresses you figure out what packages, versions, values, and features you want each part to have.
In general the layout needs to be final before the BOM in considered final as some changes may be required to improve the layout.

One workflow is putting the BOM at the design stage into a document separate from the schematic and referring to it as the 'ground truth'.
That approach sidesteps the built in checking your EDA software gives you; nothing except care and attention keeps the paper and EDA design consistent.
Another workflow is treating the EDA schematic as the master once the initial design is entered. The design BOM is allowed to get out
of date as it is of historic value only. The EDA software helps ensure the schematic and layout are consistent.

With schematic first design you need to generate something that resembles the design stage BOM to make final check and sourcing easier.
To do this I do the following:
  
  1. Include all requirements for the parts in the part fields. Special notes should go in the notes field.
  1. Generate the BOM from the EDA design including all the fields added to parts. Typically this will be a mess of manufacturers part numbers and values.
  1. Use a BOM tool from [Octopart](https://octopart.com/bom-tool), [Digikey](https://www.digikey.com/en/mylists/), [Mouser](https://www.mouser.com/BOMTool/), [LCSC/JLCPCB](https://www.lcsc.com/bom/) etc.
  1. Select all the specific parts you want
  1. Export the BOM including the extra fields from the database.
  
This allows you to only deal with the characteristics that are important to the design, preventing over constraint at early stages.
