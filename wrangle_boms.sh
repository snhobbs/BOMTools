JLCBOM="${1}"
DESIGNBOM="${2}"
JLCBOM_NAME="${JLCBOM%.*}"
DESIGNBOM_NAME="${DESIGNBOM%.*}"
PSEUDONYMS='{"Value": ["Comment"], "References": ["Designator", "Ref", "Ref Des"], "LCSC Part": ["LCSC", "JLC", "JLCPCB", "JLCPCB Part #", "JLCPCB Part"]}'
DATABASE="/home/simon/tools/kicad-jlcpcb-tools/jlcpcb/parts.db"

echo ${DESIGNBOM} ${DESIGNBOM_NAME}
echo ${JLCBOM} ${JLCBOM_NAME}
# Uncluster from ref des
COMMAND="spreadsheet_wrangler.py uncluster --column=\"References\" -p '${PSEUDONYMS}' -s ${JLCBOM} -o ${JLCBOM_NAME}_Unclustered.xlsx"
echo ${COMMAND}
eval ${COMMAND}

COMMAND="spreadsheet_wrangler.py uncluster --column=\"References\" -p '${PSEUDONYMS}' -s ${DESIGNBOM} -o ${DESIGNBOM_NAME}_Unclustered.xlsx"
echo ${COMMAND}
eval ${COMMAND}

# Same Ref Des Delmiters
#spreadsheet_wrangler.py delimiter --column="References" -p "${PSEUDONYMS}" -n ' ' -d ',' -i ${JLCBOM}.csv -o ${JLCBOM}.xlsx

# Sort Ref Des
#spreadsheet_wrangler.py sort-column --column="References" -p "${PSEUDONYMS}" -d ' ' -i ${JLCBOM}.xlsx -o ${JLCBOM}A.xlsx
#mv ${JLCBOM}A.xlsx ${JLCBOM}.xlsx

# Expand BOM
jlc_part_lookup.py --database ${DATABASE} --bom ${JLCBOM_NAME}_Unclustered.xlsx -o ${JLCBOM_NAME}_Unclustered_Expanded.xlsx

# Merge
spreadsheet_wrangler.py merge --on="References" -p "${PSEUDONYMS}" -l ${DESIGNBOM_NAME}_Unclustered.xlsx -r ${JLCBOM_NAME}_Unclustered_Expanded.xlsx --method outer -o Merged.xlsx

