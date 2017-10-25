# Server
Server with Django 1.11.6

sudo apt-get install python3-pip

sudo pip3 install Django

sudo pip3 install djangorestframework

sudo pip3 install Pillow

sudo pip3 install -U djoser

sudo pip3 install -U djangorestframework-jwt

Enable Django CORS
sudo pip3 install django-cors-headers




# Rotas

OBS: Apartir do Login, toda requisição deverá conter o header 'Authorization' com o devido TOKEN.



*Cadastro:

http://localhost:8000/user/

Method: Post
{
    "username": "",
    "email": "",
    "cpf": "",
    "password": ""
}

Response: 200 OK



*Login:

http://localhost:8000/login/

Method: Post
{
    "password": "",
    "username": ""
}

Response: 200 OK Exemplo: {
  "auth_token": "8c21ff07f0011820a2617d8de49e19d9b053f825"
}


*Logout:

http://localhost:8000/logout/

Method: Post

Necessita do header 'Authorization'

Exemplo: 'Authorization: Token 8c21ff07f0011820a2617d8de49e19d9b053f825'

Response: 200 OK 


*Usuario:

http://localhost:8000/me/

Method: Get

Necessita do header 'Authorization'

Response: 

200 OK e Informaçoes do Usuario

401 - "Token invalido" ou "As credenciais de autenticação não foram fornecidas."




