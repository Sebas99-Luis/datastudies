from databricks.connect import DatabricksSession
import pandas as pd
import sklearn

# 1. Conexión con Databricks
spark = DatabricksSession.builder.serverless().getOrCreate()
spark.range(5).show()
print(spark.sql("SELECT current_user()").collect())

# 2. Librerías locales (las que te daban problemas antes)
print("pandas:", pd.__version__)
print("scikit-learn:", sklearn.__version__)

# 3. Spark y pandas juntos
df = spark.range(3).toPandas()
print(df)
