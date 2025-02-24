import duckdb

conn = duckdb.connect()

conn.query("""
               INSTALL httpfs;
               LOAD httpfs;
                CREATE SECRET secretaws (
                TYPE S3, 
                URL_STYLE 'path',
                ENDPOINT 'localhost:9000',
                KEY_ID 'minioRootUser',
                SECRET 'iLoveCoding1234',
                REGION 'us-east-1',
                USE_SSL FALSE
            );
               """)

df = conn.query("""
                SELECT wiki, count(wiki)
                FROM read_parquet('s3://wikichanges/topics/wikimedia.recentchange/partition=0/wikimedia.recentchange*.parquet')
                GROUP BY wiki
                ORDER BY count(wiki) DESC
                ;
                """)
df.show()