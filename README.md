The Django server in this repository has been used to host the asked 10 questions query implementation.
The preprocessing of the data is done using the ipynb file in folder Preprocessing.

To initialise the Django server : 
NOTE : (Change the GraphDB host link in views.py)

```
virtualenv -p python .
pip install -r requirements.txt
cd kde_django/
python manage.py runserver
```
You can now access the page using localhost:8000 .