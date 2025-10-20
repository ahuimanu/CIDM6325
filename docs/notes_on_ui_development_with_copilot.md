# CIDM 6325 — UI Development from Wireframes with Django DTL + Bootstrap + HTMX (Overview)

*A pragmatic guide to turn sketches, wireframes, diagrams, or screenshots into working Django templates using the Django Template Language (DTL), Bootstrap, and HTMX. This is an overview; deeper guides will follow.*

---

## 0) Goals and Scope

* Show a **repeatable path** from low‑fidelity artifacts (whiteboard, Figma, Balsamiq, screenshots) to **working HTML**.
* Use **DTL** for templating, **Bootstrap** for CSS/layout, and **HTMX** for small dynamic behaviors without a SPA.
* Keep concerns clean: **layout** (base.html) → **partials** (reusable fragments) → **pages** (compose layout + partials) → **endpoints** (FBV/CBV + forms).

---

## 1) Inputs → Outputs (the pipeline)

### Inputs

* Wireframe(s): annotated with regions, hierarchy, and states.
* Diagram(s): page flow, component relationships, data in/out.
* Screenshot(s): examples to emulate; annotate spacing/typography.

### Outputs

* UI contract: page map, region names, component IDs, and data needed per region.
* Template skeletons: base layout, section blocks, partials.
* Minimal view(s) and URL(s) that render the skeleton with placeholder data.

---

## 2) UI Contract (1 page)

Define the contract **before coding**. This keeps the team aligned and helps Copilot.

### UI Contract Template (copy/paste)

``` text
Page: {{route-name}}
URL: /{{path}}
View: {{App}}.views.{{Name}}View
Layout: base.html
Blocks used: content, scripts (plus any custom blocks)
Partials: _navbar.html, _flash.html, _card_item.html
Data needed: { items: List[CardItem], user: User, messages: List[str] }
Actions: { search: GET /items?query=…, like: POST /items/{{id}}/like }
States: { loading, empty, error, populated }
HTMX: { search hx-get="/items", hx-target="#results", hx-indicator="#spinner" }
```

---

## 3) Project Structure (DTL‑first)

``` text
project/
  app/
    templates/
      base.html
      pages/
        items_list.html
      partials/
        _navbar.html
        _flash.html
        _card_item.html
    static/
      css/ (custom overrides)
      js/  (htmx helpers)
```

Conventions:

* **Partials** start with underscore, live in `templates/partials/`.
* **Pages** live in `templates/pages/` to separate composition from base.
* Keep **one purpose per partial** (card, modal, row, form).

---

## 4) From Wireframe → Base Layout

Translate global chrome (nav, container, footer) into **base.html**. Make regions into `{% block %}`s.

### base.html (Bootstrap + HTMX)

``` html
<!doctype html> <html lang="en"> <head> <meta charset="utf-8"> <meta name="viewport" content="width=device-width, initial-scale=1"> <title>{% block title %}App{% endblock %}</title> <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet"> <script src="https://unpkg.com/htmx.org@1.9.12" defer></script> </head> <body>
{% include "partials/_navbar.html" %} <main class="container py-4">
{% include "partials/_flash.html" %}
{% block content %}{% endblock %} </main>
{% block scripts %}{% endblock %} </body> </html>
```

#### _navbar.html

``` html
<nav class="navbar navbar-expand-lg bg-body-tertiary"> <div class="container-fluid"> <a class="navbar-brand" href="/">Project</a> <div class="collapse navbar-collapse"> <ul class="navbar-nav me-auto"> <li class="nav-item"><a class="nav-link" href="/items/">Items</a></li> </ul> </div> </div> </nav>
```

### _flash.html (DTL Messages)

``` html
{% if messages %} <div class="mt-2">
{% for message in messages %}
<div class="alert alert-{{ message.tags|default:"info" }} mb-2">{{ message }}</div>
{% endfor %} </div>
{% endif %}
```

---

## 5) From Wireframe → Page Template

Map the wireframe’s **grid** and **components** to Bootstrap rows/cols and partials. Use placeholder data first.

### pages/items_list.html

``` html
{% extends "base.html" %}
{% block title %}Items{% endblock %}
{% block content %} <div class="d-flex align-items-center mb-3 gap-2"> <input id="q" name="q" class="form-control" placeholder="Search…"
            hx-get="/items" hx-trigger="keyup changed delay:300ms" hx-target="#results" hx-indicator="#spin" /> <div id="spin" class="spinner-border spinner-border-sm text-secondary htmx-indicator" role="status"></div> </div>

  <div id="results" class="row g-3">
    {% for item in items %}
      <div class="col-12 col-md-6 col-lg-4">
        {% include "partials/_card_item.html" with item=item %}
      </div>
    {% empty %}
      <div class="col"><div class="text-muted">No results</div></div>
    {% endfor %}
  </div>
{% endblock %}
```

### partials/_card_item.html

``` html
<div class="card h-100"> <div class="card-body"> <h5 class="card-title">{{ item.title }}</h5> <p class="card-text">{{ item.summary }}</p> <button class="btn btn-outline-primary"
             hx-post="/items/{{ item.id }}/like" hx-swap="outerHTML" hx-target="closest .card">
Like ({{ item.likes }}) </button> </div> </div>
```

---

## 6) Views, URLs, and HTMX endpoints

Start with static data to validate structure; then wire real QuerySets.

### urls.py

``` python
from django.urls import path
from . import views

urlpatterns = [
    path("items", views.items_list, name="items_list"),
    path("items/<int:pk>/like", views.item_like, name="item_like"),
]
```

### views.py (FBV example)

``` python
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Item

def items_list(request):
    q = request.GET.get("q", "").strip()
    qs = Item.objects.all()
    if q:
        qs = qs.filter(title__icontains=q)
    context = {"items": qs[:24]}
    if request.htmx:
        return render(request, "pages/items_list.html #results", context)
    return render(request, "pages/items_list.html", context)

def item_like(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        item.likes = (item.likes or 0) + 1
        item.save(update_fields=["likes"])
    return render(request, "partials/_card_item.html", {"item": item})
```

Notes:

* `request.htmx` is available if you add **django‑htmx** middleware; otherwise check header `HX-Request`.
* Using the **CSS selector** (`template.html #results`) renders only a fragment for HTMX swaps.

---

## 7) Wireframe Annotation Checklist

Before you code, mark up the wireframe with:

* Regions → `block`s (content, sidebar, footer, scripts).
* Components → partials (`_card_item.html`, `_modal.html`).
* Data → variables and lists (`{{ user }}`, `{% for item in items %}`).
* Actions → URLs & HTTP verbs (GET search, POST like, PATCH update).
* States → empty / loading / error placeholders.
* Responsive rules → Bootstrap grid breakpoints (col‑12/6/4, etc.).

---

## 8) Forms & Modals (DTL + Bootstrap + HTMX)

### Partial modal

``` html
<div class="modal fade" id="itemModal" tabindex="-1" aria-hidden="true"> <div class="modal-dialog"><div class="modal-content"> <div class="modal-header"><h5 class="modal-title">New Item</h5></div> <div class="modal-body" id="itemForm"> <!-- form will load here via HTMX --> </div> </div></div> </div>
```

### Load form via HTMX

``` html
<button class="btn btn-primary"
         hx-get="/items/new" hx-target="#itemForm" hx-trigger="click"
         data-bs-toggle="modal" data-bs-target="#itemModal">Add Item</button>
```

**Server fragments**
def item_new(request):
form = ItemForm(request.POST or None)
if request.method == "POST" and form.is_valid():
form.save()
messages.success(request, "Item created")
return HttpResponse(status=204, headers={"HX-Redirect": "/items"})
return render(request, "partials/_item_form.html", {"form": form})

#### _item_form.html

``` html
<form method="post" hx-post="/items/new" hx-target="#itemForm" hx-swap="outerHTML">
{% csrf_token %}
{{ form.as_p }} <div class="d-flex gap-2"> <button class="btn btn-primary" type="submit">Save</button> <button class="btn btn-outline-secondary" type="button" data-bs-dismiss="modal">Cancel</button> </div> </form>
```

---

## 9) Bootstrap Layout Patterns (from wireframes)

* **Grid**: map columns in wireframe to `row` + `col-*` classes. Start mobile‑first.
* **Spacing**: use utility classes (`pt-3`, `mb-2`, `gap-2`). Avoid inline styles.
* **Typography**: match hierarchy with `h1`–`h6`, `.lead`, `.small`.
* **Cards/Lists**: prefer cards for repeatable items; tables for dense data.
* **Feedback**: use alerts, toasts, and spinners; couple with HTMX indicators.

---

## 10) HTMX Patterns (progressive enhancement)

* **Search-as-you-type**: `hx-get`, `hx-trigger="keyup changed delay:300ms"`, target a result container.
* **Partial swaps**: return only fragments (`template.html #id`) to reduce payload.
* **Stateful buttons**: POST to toggle state; re-render the button/card partial.
* **Indicators**: `hx-indicator` for spinner visibility.
* **Redirect after success**: send `HX-Redirect` header.

---

## 11) Validation, Messages, Empty/Loading States

* Always render `{% csrf_token %}` in forms.
* Use Django **messages** in `_flash.html` for cross‑request feedback.
* Provide **empty** states in loops and **loading** spinners for HTMX targets.

---

## 12) Review Checklist (before PR)

* Base layout renders; blocks used consistently.
* Partials are focused, reusable, and named with `_` prefix.
* Pages match the wireframe’s regions and flow.
* HTMX requests degrade gracefully (page still works without JS).
* Forms validate; errors are visible and accessible.
* Bootstrap utilities replace ad‑hoc CSS; custom CSS isolated.

---

## 13) Copilot Brief (for this workflow)

``` text
COPY BLOCK — Copilot UI Slice Brief
Context: We have a wireframe for the Items list page and a UI contract.
Goal: Produce base.html, items_list.html, and three partials (navbar, flash, card_item)
      using Bootstrap 5 + HTMX + DTL, with placeholder data and search-as-you-type.
Constraints: Keep components small; add indicators; map grid to wireframe; no inline styles.
Deliverables: Template files with blocks/partials wired, minimal views/urls, and a checklist.
```

---

## 14) Next Steps

* Convert another wireframe into a modal‑heavy page (create/edit flows).
* Extract repeating blocks into macros/partials; consider template tags for formatting.
* Add accessibility review and keyboard flows to the checklist.

*End of overview.*
