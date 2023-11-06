# Natural Language Design Statements:

1.	“The app should record student information, including their names, IDs, contact details, and enrollment status."
2.	"It needs to store details about academic programs, specifying program names, majors, and associated degree requirements."
3.	"The app should track course information, including course codes, titles, descriptions, and credit hours."
4.	"It should associate students with their enrolled courses, keeping a record of enrollment dates and academic advisors."
5.	"The app needs to record course prerequisites and co-requisites to ensure students meet the necessary requirements."
6.	"It should store grading information, including student grades, GPA calculations, and grading scales."
7.	"The app should track degree audit progress for each student, indicating completed and remaining degree requirements."
8.	"It needs to capture faculty data, including their names, academic departments, and teaching assignments."
9.	"The app should record academic calendar events, including semester start and en d dates, registration periods, and holidays."
10.	"It needs to store historical data, such as past course offerings, student transcripts, and graduation records."
11.	“The app should track student requests, such as course add/drop requests, transfer credit evaluations, and degree plan changes."
12.	"It needs to record communication logs between students, advisors, and faculty members for academic support."
13.	"The app should store resource allocation data, including classroom assignments, textbooks, and course materials."
14.	"It needs to capture financial information, such as tuition fees, scholarships, and student accounts."
15.	"The app should track extracurricular activities and clubs that students participate in for a holistic student profile."
16.	"It needs to store internship and job placement records for career services and compliance tracking."
17.	"The app should record alumni data, including graduation years, career outcomes, and contact information."
18.	“It needs to track faculty research projects, publications, and grants for academic assessment and reporting."
19.	"The app should store accreditation-related data, including program reviews, assessment results, and compliance documentation."
20.	"It needs to capture institutional data, including campus locations, buildings, and administrative offices."


# H1
## H2
### H3
#### H4
##### H5
###### H6

1. asdf
1. asdfasd

* asdfa
* asdfad

you can use [Google](google.com) to searh for things

*This is italicized*
**This is bold**


# Guide to Book Topics for Final Project (Baseline, Good, Better, Best)

I have classified the learning objectives from Antonio's book according to the following scheme.  Each category is relative to the following requirements for your final project:

* You must implement *all* **Baseline** components - Gets you to 70% of the value
* You will implement *at least* six **Good** components - Gets you to 80% of the vaue
* You will implement *at least* two **Better** components - Gets you to 85% of the value
* You will implement *at least* two **Best** components - Gets you to 90% of the value

Where is the remaining 10%? It comes from the synthesis and service to your idea (implementation).

* **Baseline**: Essential Django knowledge that must be demonstrated in your final project
* **Good**: Fundamental knowledge that sets up a more useful app
* **Better**: Approaching a higher degree of robustness
* **Best**: Approaching professional-grade features and tools

Topic                                       | Baseline  | Good  | Better  | Best
---                                         | ---       | ---   | ---     | ---
***Chapter 1***                             |           |       |         |
Basic Views                                 | x         |       |         |
URL Mapping                                 | x         |       |         |
Templates                                   | x         |       |         |
Routing                                     | x         |       |         |
***Chapter 2***                             |           |       |         |
Working with Databases                      | x         |       |         |
SQL                                         | x         |       |         |
Django Models                               | x         |       |         |
Django Migrations                           | x         |       |         |
Fixtures for import/export                  |           | x     |         |
***Chapter 3 and 11***                      |           |       |         | 
Class-Based Views                           | x         |       |         |
Function-Based Views                        | x         |       |         |
Django Template Language                    | x         |       |         |
Template filters                            | x         |       |         |
Custom template filters                     |           |       | x       |
string filters                              |           | x     |         |
Template tags                               | x         |       |         |
***Chapter 4 and 10***                      |           |       |         |
Django Admin                                | x         |       |         |
Django Admin manage users                   |           |       |         | x
Customize Admin interface                   |           |       | x       | 
Customize ModelAdmin classes                |           |       | x       |
Add custom view to admin interface          |           |       | x       |
***Chapter 5***                             |           |       |         |
Static files                                | x         |       |         |
Use front-end framework (bootstrap)         |           | x     |         |
static urls                                 | x         |       |         |
Cache invalidation                          |           | x     |         |
`django-storages` or `whitenoise`           |           |       | x       |
***Chapter 6 and 7***                       |           |       |         |
Django Forms Classes                        | x         |       |         |
Django ModelForm Class                      | x         |       |         |
Form data validation and retreival          | x         |       |         |
Custom field validation                     |           | x     |         |
***Chapter 8***                             |           |       |         |
Serving Media Files                         |           | x     |         |
File Upload                                 | x         |       |         |
ModelForm and File Uploads                  |           |       | x       |
Serving Uploaded Files                      |           |       | x       |
***Chapter 9***                             |           |       |         |
Passwords and Auth                          |           | x     |         |
Authentication decorators                   |           | x     |         |
Conditional template access                 |           | x     |         |
Sessions                                    | x         |       |         |
***Chapter12***                             |           |       |         |
Django REST Framework                       |           |       |         | x
Object Serializers                          |           |       |         | x
ModelViewSet                                |           |       |         | x
***Chapter 13***                            |           |       |         |
PDF Generation                              | x         |       |         |
CSV Generation (export)                     | x         |       |         |
Graphs and Visualizations                   | x         |       |         |
***Chapter 14***                            |           |       |         | 
`unittest` in Django                        | x         |       |         |
Testing Models                              | x         |       |         |
Testing Views                               |           | x     |         |
Django RequestFactory                       |           | x     |         |
***Chapter15***                             |           |       |         |
`python-dotenv` or `django-configurations`  | x         |       |         |
`dj-database-url`                           |           | x     |         |
`django-crispy-forms`                       | x         |       |         |
`django-allauth`                            |           |       | x       |
Django Debug Toolbar                        |           | x     |         |
***Chapter16***                             |           |       |         |
use any JS front-end framework              |           |       | x       |


### Optional 3rd Party Tools to consider***
* [Django admin](https://github.com/wsvincent/awesome-django#admin)
* [APIs](https://github.com/wsvincent/awesome-django#apis)
* [Async](https://github.com/wsvincent/awesome-django#async)
* [ECommerce](https://github.com/wsvincent/awesome-django#ecommerce)
* [Files and Images](https://github.com/wsvincent/awesome-django#filesimages)
* [Model enhancements](https://github.com/wsvincent/awesome-django#models)
* [Search](https://github.com/wsvincent/awesome-django#search)
* [Tasks and Job Scheduling](https://github.com/wsvincent/awesome-django#task-queues)
* [Users and SSO](https://github.com/wsvincent/awesome-django#users)
* [Views](https://github.com/wsvincent/awesome-django#views)