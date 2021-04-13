import pandas as pd # type: ignore
'''
Group a dataframe by the column given.
The cluster column will be made as a list. The sort_by column determines the group.
Shared values are grouped and the other values in the list are filled in
with the first entry found.
'''
def group_by(df : pd.DataFrame, sort_by : str, cluster : str) -> pd.DataFrame:
    rows = []
    for entry in df[sort_by].unique():
        filtered_df = df[df[sort_by]==entry]
        row = next(filtered_df.iterrows())[-1] # use the first matching row for the output row data
        cluster_list = []
        for i, row in filtered_df.iterrows():
            print(row)
            try:
                val = row[cluster][0]
            except (IndexError,TypeError):
                 val = row[cluster]
            cluster_list.append(val)

        row.drop(cluster) # remove the column to avoid confusion
        new_row = [
            (key, val) for key, val in row.items()
        ]
        new_row.append((cluster, cluster_list))
        #row[cluster] = list(cluster_list)
        rows.append(row)
    return pd.DataFrame(rows)

