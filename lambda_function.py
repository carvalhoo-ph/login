import json
import pymysql
import os

def lambda_handler(event, context):
    # Obter o CPF do evento
    cpf = event.get('cpf')
    if not cpf:
        return {
            'statusCode': 400,
            'body': json.dumps('CPF não fornecido')
        }

    # Conectar ao banco de dados
    connection = pymysql.connect(
        host=os.environ['RDS_HOST'],
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'],
        database=os.environ['DB_NAME']
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
