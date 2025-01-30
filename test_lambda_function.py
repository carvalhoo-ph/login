import json
import os
import pytest
from lambda_function import lambda_handler

# Configurar variáveis de ambiente para testes
os.environ['RDS_HOST'] = 'portal-ex-colab.cn2i04a6agxy.us-east-1.rds.amazonaws.com'
os.environ['DB_USERNAME'] = 'postgres'
os.environ['DB_PASSWORD'] = 'Koda020116'
os.environ['DB_NAME'] = 'portal_ex_colab'

def test_lambda_handler_valid_cpf(mocker):
    event = {'cpf': '12345678901'}
    context = {}
    
    # Mockar a conexão com o banco de dados e a execução da query
    mock_conn = mocker.Mock()
    mock_cursor = mocker.Mock()
    mock_cursor.__enter__ = mocker.Mock(return_value=mock_cursor)
    mock_cursor.__exit__ = mocker.Mock(return_value=None)
    mock_cursor.fetchone.return_value = ('Senha123',)
    mock_conn.cursor.return_value = mock_cursor
    mocker.patch('psycopg2.connect', return_value=mock_conn)
    
    response = lambda_handler(event, context)
    assert response['statusCode'] == 200
    assert json.loads(response['body']) == {'valid': True, 'senha': 'Senha123'}

def test_lambda_handler_invalid_cpf(mocker):
    event = {'cpf': '00000000000'}
    context = {}
    
    # Mockar a conexão com o banco de dados e a execução da query
    mock_conn = mocker.Mock()
    mock_cursor = mocker.Mock()
    mock_cursor.__enter__ = mocker.Mock(return_value=mock_cursor)
    mock_cursor.__exit__ = mocker.Mock(return_value=None)
    mock_cursor.fetchone.return_value = None
    mock_conn.cursor.return_value = mock_cursor
    mocker.patch('psycopg2.connect', return_value=mock_conn)
    
    response = lambda_handler(event, context)
    assert response['statusCode'] == 404
    assert json.loads(response['body']) == {'valid': False}

def test_lambda_handler_no_cpf():
    event = {}
    context = {}
    response = lambda_handler(event, context)
    assert response['statusCode'] == 400
    assert json.loads(response['body']) == 'CPF não fornecido'
