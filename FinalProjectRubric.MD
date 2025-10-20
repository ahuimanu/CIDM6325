# Guide to Book Topics for Final Project (Baseline, Good, Better, Best)

***NOTE***: Updated 09/10/2025
Finalized for Fall 2025.  

***NOTE***: You **MUST** document and identify which of the Good, Better, Best features you are using in your project in your project's readme.

## How to use this List

I have classified the learning objectives from [Matt's book](https://www.mattlayman.com/understand-django/browser-to-django/) according to the following scheme. Each category is relative to the following requirements for your final project:

- You must implement *all* **Baseline** components - Gets you to 70% of the value
- You will implement *at least* four **Good** components - Gets you to 80% of the value
- You will implement *at least* two **Better** components - Gets you to 85% of the value
- You will implement *at least* one **Best** component - Gets you to 90% of the value

Where is the remaining 10%? It comes from the synthesis and service to your implementation approach.

- **Baseline** 🟩: Essential Django knowledge that must be demonstrated in your final project  
- **Good** 🟨: Fundamental knowledge that sets up a more useful app  
- **Better** 🟧: Approaching a higher degree of robustness  
- **Best** 🟥: Approaching professional-grade features and tools

NOTE: The chapter references indicate where a technique is introduced. Demonstrate the technique in your project—you need not mirror the exact example from the text.

---

Topic | Baseline 🟩 | Good 🟨 | Better 🟧 | Best 🟥
---|---|---|---|---
***[Chapter 1 — From Browser To Django](https://www.mattlayman.com/understand-django/browser-to-django/)*** | - | - | - | -
[Web request/response lifecycle](https://www.mattlayman.com/understand-django/browser-to-django/) | 🟩 | - | - | -
[DNS → IP → HTTP (context)](https://www.mattlayman.com/understand-django/browser-to-django/) | 🟩 | - | - | -
[HTTP methods & headers](https://www.mattlayman.com/understand-django/browser-to-django/) | 🟩 | - | - | -
[WSGI (where HTTP meets Python)](https://www.mattlayman.com/understand-django/browser-to-django/) | 🟩 | - | - | -
[Django’s job: URLs + views](https://www.mattlayman.com/understand-django/browser-to-django/) | 🟩 | - | - | -
[Getting Django set up (venv, startproject)](https://www.mattlayman.com/understand-django/browser-to-django/) | 🟩 | - | - | -
***[Chapter 2 — URLs Lead The Way](https://www.mattlayman.com/understand-django/urls-lead-way/)*** | - | - | - | -
[URLconf basics: `path()`/`urlpatterns`](https://www.mattlayman.com/understand-django/urls-lead-way/) | 🟩 | - | - | -
[Route converters (`<int:>`, `<slug:>`)](https://www.mattlayman.com/understand-django/urls-lead-way/) | 🟩 | - | - | -
[Ordering/specificity of patterns](https://www.mattlayman.com/understand-django/urls-lead-way/) | 🟩 | - | - | -
[`include()` and namespacing (`app_name`)](https://www.mattlayman.com/understand-django/urls-lead-way/) | - | 🟨 | - | -
[Named URLs & reversing (`reverse`, `{% url %}`)](https://www.mattlayman.com/understand-django/urls-lead-way/) | - | 🟨 | - | -
[`re_path()` and regex routes](https://www.mattlayman.com/understand-django/urls-lead-way/) | - | - | 🟧 | -
***[Chapter 3 — Views On Views](https://www.mattlayman.com/understand-django/views-on-views/)*** | - | - | - | -
[Function-Based Views (FBV)](https://www.mattlayman.com/understand-django/views-on-views/) | 🟩 | - | - | -
[`HttpRequest`/`HttpResponse` essentials](https://www.mattlayman.com/understand-django/views-on-views/) | 🟩 | - | - | -
[Intro to Class-Based Views (CBV)](https://www.mattlayman.com/understand-django/views-on-views/) | - | 🟨 | - | -
[Generic CBVs (`TemplateView`, etc.)](https://www.mattlayman.com/understand-django/views-on-views/) | - | 🟨 | - | -
[View decorators (auth, cache, etc.)](https://www.mattlayman.com/understand-django/views-on-views/) | - | - | 🟧 | -
[Organizing view code for clarity](https://www.mattlayman.com/understand-django/views-on-views/) | - | - | 🟧 | -
***[Chapter 4 — Templates For User Interfaces](https://www.mattlayman.com/understand-django/templates-user-interfaces/)*** | - | - | - | -
[`TEMPLATES` settings & loaders](https://www.mattlayman.com/understand-django/templates-user-interfaces/) | 🟩 | - | - | -
[Rendering from views (`render`, CBV context)](https://www.mattlayman.com/understand-django/templates-user-interfaces/) | 🟩 | - | - | -
[DTL variables, filters, tags](https://www.mattlayman.com/understand-django/templates-user-interfaces/) | - | 🟨 | - | -
[Inheritance: `{% extends %}`, `{% block %}`](https://www.mattlayman.com/understand-django/templates-user-interfaces/) | - | 🟨 | - | -
[`{% include %}` and partials](https://www.mattlayman.com/understand-django/templates-user-interfaces/) | - | 🟨 | - | -
[Custom tags/filters (`templatetags/`)](https://www.mattlayman.com/understand-django/templates-user-interfaces/) | - | - | 🟧 | -
[Built-in helpers (`url`, `spaceless`, etc.)](https://www.mattlayman.com/understand-django/templates-user-interfaces/) | - | - | 🟧 | -
***[Chapter 5 — User Interaction With Forms](https://www.mattlayman.com/understand-django/user-interaction-forms/)*** | - | - | - | -
[`Form classes: fields → HTML`](https://www.mattlayman.com/understand-django/user-interaction-forms/) | 🟩 | - | - | -
[GET vs POST, bound forms, `is_valid()`](https://www.mattlayman.com/understand-django/user-interaction-forms/) | 🟩 | - | - | -
[CSRF & `{% csrf_token %}`](https://www.mattlayman.com/understand-django/user-interaction-forms/) | - | 🟨 | - | -
[`FormView` / success redirect](https://www.mattlayman.com/understand-django/user-interaction-forms/) | - | 🟨 | - | -
[Common widgets & validation patterns](https://www.mattlayman.com/understand-django/user-interaction-forms/) | - |  | - | -
[ModelForms for CRUD](https://www.mattlayman.com/understand-django/user-interaction-forms/) | - | - | 🟧 | -

### Optional 3rd Party Tools to consider

- [Django admin](https://github.com/wsvincent/awesome-django#admin)
- [APIs](https://github.com/wsvincent/awesome-django#apis)
- [Async](https://github.com/wsvincent/awesome-django#async)
- [ECommerce](https://github.com/wsvincent/awesome-django#ecommerce)
- [Files and Images](https://github.com/wsvincent/awesome-django#filesimages)
- [Model enhancements](https://github.com/wsvincent/awesome-django#models)
- [Search](https://github.com/wsvincent/awesome-django#search)
- [Tasks and Job Scheduling](https://github.com/wsvincent/awesome-django#task-queues)
- [Users and SSO](https://github.com/wsvincent/awesome-django#users)
- [Views](https://github.com/wsvincent/awesome-django#views)

***NOTE A***: This does not JUST mean in the inclusion of any [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript).  I would strongly recommend [htmx](https://htmx.org/) if you need any front-end JS magic. However, it should be the case that MOST JavaScript is optional.
