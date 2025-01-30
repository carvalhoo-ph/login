import json
import psycopg2
import os
import config

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
        host=config.rds_host,
        user=config.db_username,
        password=config.db_password,
        dbname=config.db_name
    )

    try:
        with connection.cursor() as cursor:
            # Verificar se o CPF existe na tabela ex_funcionarios
            sql = "SELECT senha FROM ex_funcionarios WHERE cpf = %s"
            cursor.execute(sql, (cpf,))
            result = cursor.fetchone()

            if result:
                return {
                    'statusCode': 200,
                    'body': json.dumps({'valid': True, 'senha': result[0]})
                }
            else:
                return {
                    'statusCode': 404,
                    'body': json.dumps({'valid': False})
                }
    finally:
        connection.close()
