# Access_Review
This is a project designed for the Coupa Software. Our project would help them to do the access review easily and automatically.
Coupa software has many services for internal use. For example they have AWS, RightScale, DNS and so on. There are also lots of employees in coupa with different roles. They are supposed to access and operate different applications and data within.
In this Access Review project, we come up with a solution to make access review process easier to manage and realize better visualization. This solution makes permission control more reliable and can greatly relieve the work of administrators.

How to run:

````
pip install django
pip install reportlab
git clone https://github.com/KearneyLiu/Access_Review.git
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
````