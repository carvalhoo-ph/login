import psycopg2

rds_host = "portal-ex-colab.cn2i04a6agxy.us-east-1.rds.amazonaws.com"
db_username = "postgres"
db_password = "Koda020116"
db_name = "postgres"  # Atualize com o nome correto do banco de dados

try:
    connection = psycopg2.connect(
        host=rds_host,
        user=db_username,
        password=db_password,
        dbname=db_name
    )
    print("Conexão bem-sucedida!")
    connection.close()
except Exception as e:
    print(f"Erro ao conectar: {e}")