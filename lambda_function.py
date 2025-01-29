import json
import psycopg2
import os
from config import rds_host, db_username, db_password, db_name

def lambda_handler(event, context):
    # Obter o CPF do evento
    cpf = event.get('cpf')
    if not cpf:
        return {
            'statusCode': 400,
            'body': json.dumps('CPF não fornecido')
        }

    # Conexão com o banco de dados
    connection = psycopg2.connect(
        host=rds_host,
        user=db_username,
        password=db_password,
        dbname=db_name
    )

    try:
        with connection.cursor() as cursor:
            # Verificar se o CPF existe na tabela ex_funcionarios
            sql = "SELECT * FROM ex_funcionarios WHERE cpf = %s"
            cursor.execute(sql, (cpf,))
            result = cursor.fetchone()

            if result:
                return {
                    'statusCode': 200,
                    'body': json.dumps('CPF válido')
                }
            else:
                return {
                    'statusCode': 404,
                    'body': json.dumps('CPF não encontrado')
                }
    finally:
        connection.close()
