# django_assignment

1. Create a Python 3.7 virtualenv
2. Install dependencies:

   
   pip install -r requirements.txt
3. Configure your database in settings.py file
4. To Create tables, use given command:
   
   
   - python manage.py makemigrations
   - python manage.py migrate
5. Create a superuser using given command:


   python manage.py loaddata seed_super_user.json
   useremail:admin@gmail.com
   password:Sarvesh@12
6. Run the server:


   python manage.py runserver
7. api's and request data:
   
   
   login api: HTTP POST
   url: /api/v1/login/
   request data: {
    "email":"",
    "password":""
   }
   
   
   registration api: HTTP POST
   url: /api/v1/registrations/
   request data: {
    "email":"",
    "first_name": "",
    "last_name": "",
    "phone":"",
    "pincode":"",
    "password":"",
    "address":"",
    "city":"",
    "state":"",
    "country":""
  }
  
  
  cms api: HTTP POST,GET,PUT,DELETE
  
  
  url: /api/v1/contentmanagements/
  
  
  To create cms use form type of request data and refer given db:
  
  Delete request data:
  {
    "id":id number
  }
  
  
  
  Put request data:
  {
    "id":1,
    "title":"",
    "body":"",
    "summary":"",
    ...
  }
  
