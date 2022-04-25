
# Lost and Found Items Web Application

Created web-application for students and faculties to upload lost/found items on
website.When Item is uploaded to website notification through email are sent to all
registered users One User can contact another user through chat support. User can add extra facility of
reward money also.This web-application are developed using Django Framework as backend and HTML ,CSS
,Javascript ,Bootstrap as Frontend and MySQL as Database

## Installation
 
1. Install [Python 3](https://www.python.org/downloads/)

2. Install [xampp](https://www.apachefriends.org/download.html) and start MySQL

3. Install required dependenicies using below command

```bash
  pip install -r requirements.txt
```
4. Create Tables Using below command

```bash
  python manage.py migrate
```
5. Navigate to LostAndFound\Radis and double click on redis-server.exe

6. Start Server Using below command
```bash
  python manage.py runserver
```
6. Web Application can be accessible at http://127.0.0.1:8000/

## References

- [Django Quick Introduction](https://docs.djangoproject.com/en/4.0/intro/tutorial01/)
- [Django Models Introduction](https://docs.djangoproject.com/en/4.0/topics/db/models/)
- [Django Admin Introduction](https://docs.djangoproject.com/en/4.0/ref/contrib/admin/)


## Screenshots
1. Login
![Login](https://github.com/Khilan9/LostAndFound/blob/master/Images/Login.png)

2. Home Page
![Home](https://github.com/Khilan9/LostAndFound/blob/master/Images/Homepage.png)

3. Lost Item Registration
![LostRegister](https://github.com/Khilan9/LostAndFound/blob/master/Images/LostItemRegister.png)

4. Found Item Registration
![FoundRegister](https://github.com/Khilan9/LostAndFound/blob/master/Images/FoundItemRegister.png)

5. Lost Items List
![LostList](https://github.com/Khilan9/LostAndFound/blob/master/Images/LostItemsList.png)

6. Found Items List
![FoundList](https://github.com/Khilan9/LostAndFound/blob/master/Images/FoundItems.png)

7. Claim Request
![Claim](https://github.com/Khilan9/LostAndFound/blob/master/Images/ClaimRequest.png)

8. Return Request
![Return](https://github.com/Khilan9/LostAndFound/blob/master/Images/ReturnRequest.png)

14. Chat
![Chat](https://github.com/Khilan9/LostAndFound/blob/master/Images/Chat.png)
