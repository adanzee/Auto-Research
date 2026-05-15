import duckdb
con = duckdb.connect('jobs.db')
con.execute("CREATE TABLE jobs AS SELECT * FROM read_csv_auto('data/datasets/data_set/data_set.csv')")
print('Loaded CSV into DuckDB')