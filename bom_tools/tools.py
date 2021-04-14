import pandas as pd # type: ignore
'''
Group a dataframe by the column given.
The cluster column will be made as a list. The sort_by column determines the group.
Shared values are grouped and the other values in the list are filled in
with the first entry found.
'''
'''
def group_by(df : pd.DataFrame, sort_by: str, cluster : str) -> pd.DataFrame:
    grouped = df.groupby(sort_by)
    rows = []
    for _, parts in grouped:
        if len(parts) < 1:
            continue
        assert(type(parts) is pd.DataFrame)
        assert(len(parts) > 0)
        print(parts)
        cluster_row = parts.head(1)
        cluster_list = []
        for _, part in parts.iterrows():
            cluster_list.append(part[cluster])
        print(cluster_row, type(cluster_row))
        cluster_row[cluster] = cluster_list
        rows.append(cluster_row)
        print(rows)
    return pd.DataFrame(rows, ignore_index=True)
'''
'''
def group_by(df : pd.DataFrame, sort_by : str, cluster : str) -> pd.DataFrame:
    rows = []
    count = 0
    for entry in df[sort_by].unique():
        filtered_df = df[df[sort_by]==entry]
        try:
            row = next(filtered_df.iterrows())[-1] # use the first matching row for the output row data
        except StopIteration:
            continue
        cluster_list = []
        for i, row in filtered_df.iterrows():
            try:
                val = row[cluster][0]
            except (IndexError,TypeError):
                 val = row[cluster]
            cluster_list.append(val)

        print(cluster_list)
        row.drop(cluster) # remove the column to avoid confusion
        new_row = [
            (key, val) for key, val in row.items()
        ]
        new_row.append((cluster, cluster_list))
        #row[cluster] = list(cluster_list)
        rows.append(row)
    return pd.DataFrame(rows)
'''
