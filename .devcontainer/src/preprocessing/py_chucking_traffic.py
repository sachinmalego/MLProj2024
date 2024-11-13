#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 13:28:44 2024

@author: qb
"""

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

csv_file = '/home/qb/ML_Group_Assignment/p_traffic_.csv'
parquet_file = '/home/qb/ML_Group_Assignment/traffic_chunks/'
chunksize = 1000

csv_stream = pd.read_csv(csv_file, sep='\t', chunksize=chunksize, low_memory=False, on_bad_lines='skip')

for i, chunk in enumerate(csv_stream):
    print("Chunk", i)
    # Guess the schema of the CSV file from the first chunk
    parquet_schema = pa.Table.from_pandas(df=chunk).schema
    # Open a Parquet file for writing
    file_name ='p_traffic_'+str(i)+'.parquet'
    parquet_writer = pq.ParquetWriter(parquet_file+file_name, parquet_schema, compression='snappy')
    # Write CSV chunk to the parquet file
    table = pa.Table.from_pandas(chunk, schema=parquet_schema)
    parquet_writer.write_table(table)

parquet_writer.close()