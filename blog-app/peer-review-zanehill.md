# Peer Review — External Assessment

**Repo:** `mmparton1/CIDM6325` → `blog` app  
**Focus:** Model clarity, validation (for a web app), business fit  
**Reviewer:** External assessor

## Quick Take

This is a clean, well-structured Django blog. The `Post` model is simple and sensible, the views lean on Django’s class-based patterns, and the URLs are clear. You’ve got the basics right: public list view shows **published** posts only, while create/update/delete actions require the author to be logged in. Nice touch auto-filling `published_at` when a post goes live.

Where it needs polish is mostly in the safety nets and “edge cases”: protecting draft detail pages, handling slug collisions, adding tests, and writing down what “success” looks like once people start using this. None of these are heavy lifts, and they’d make the project feel production-aware instead of just “it runs.”

---

## What I Looked At (and Liked)

**Models (`models.py`)**

- `Post` has the right fields: `title`, `slug` (unique), `author`, `body`, `status` (`draft/published`), timestamps, and `published_at`.
    
- Default ordering by newest published first is exactly what readers expect.
    
- `get_absolute_url()` wires into the detail route cleanly.
    

**Views (`views.py`)**

- List view filters to `status="published"`—great.
    
- Create/Update set `author = request.user` on the server, so users can’t spoof ownership.
    
- Slug auto-generates from the title if you didn’t type one.
    
- When a post flips to **Published**, `published_at` gets set for you.
    

**URLs (`urls.py`)**

- Simple, readable routes with namespacing (`blog:`).
    
- Slug-based detail is user-friendly and SEO-friendly.
    

Overall, it’s solid Django and easy to follow. That alone earns you a lot of points.

---

## Where It Can Be Safer and Smoother

1. **Drafts are viewable by URL right now**  
    Your list hides drafts, but `PostDetail` doesn’t block them. If someone guesses a slug (or has an old link), they can view a draft.  
    **Fix:** In `PostDetail`, limit the queryset so anonymous users only see published posts; authors and superusers can see drafts.
    
2. **Slug collisions**  
    Two posts with the same title will generate the same slug and blow up on save.  
    **Fix:** When a slug exists, append `-2`, `-3`, etc., until you find a free one. Small loop, big win.
    
3. **“Published” should always have a timestamp**  
    Views try to set `published_at`, but nothing enforces it at the model/database level.  
    **Fix:** In `clean()` or `save()`, ensure `published_at` is present when `status == published`, or add a `CheckConstraint` so the DB enforces it too.
    
4. **Performance and UX nits**
    
    - Add `paginate_by = 10` to the list view so a long feed doesn’t turn into an endless page.
        
    - Use `select_related('author')` to avoid N+1 queries in templates.
        
    - Consider a small index on `status` and `published_at` since you filter/sort on them.
        
5. **Testing and guardrails**  
    Right now there’s no visible test coverage. You don’t need a lot—just enough to keep you safe:
    
    - List shows only published posts.
        
    - Draft detail is private to the author/superuser.
        
    - Only the author can edit/delete.
        
    - Publishing sets `published_at`.
        
    - Slug de-dupe works.
        

---

## Business Fit (Yes, Even for a Blog)

Even a small blog has a “why.” A couple of lightweight ideas turn this into a project with a purpose:

- **Define success:**  
    Pick 2–3 simple KPIs—e.g., “time from draft → publish,” “% of posts that get published within 24h,” or “average views per post in first week.”
    
- **Spell out the workflow:**  
    Who can publish? Is there a review step? If that matters, consider adding an extra status like `review` and a basic moderation path.
    
- **Write down the ops basics:**  
    How to set up (venv, install, migrate, createsuperuser), what environment variables you expect, and where secrets live (env vars, not in repo).
    

These don’t take long to document and they make evaluators feel confident about the project.

---

## Suggested README Upgrades (Copy/Paste Friendly)

**Quickstart**

`python -m venv .venv # Windows: .venv\Scripts\activate # macOS/Linux: source .venv/bin/activate pip install -r requirements.txt python manage.py migrate python manage.py createsuperuser python manage.py runserver`

**Model at a Glance**

- `Post(title, slug, author, body, status[draft|published], published_at, created, updated)`
    
- Drafts are private to the author; published posts are public.
    
- `published_at` auto-fills when you publish.
    
- Ordered by newest published first.
    

**Publishing Rules**

- Only authors (or admins) can edit/delete their posts.
    
- Draft detail pages are **not** public.
    
- Slugs are auto-generated and de-duplicated if needed.
    

**Nice-to-Haves**

- Pagination (10 per page)
    
- `select_related('author')` on list/detail
    
- Basic search by title
    

---

## Tiny Code Tweaks Worth Making

- **Protect draft detail**
    
    `# in PostDetail def get_queryset(self):     qs = Post.objects.all().select_related("author")     if not self.request.user.is_authenticated:         return qs.filter(status=Post.PUBLISHED)     return qs.filter(         models.Q(status=Post.PUBLISHED) |         models.Q(author=self.request.user) |         models.Q(author__is_superuser=True)     )`
    
- **Slug de-dupe on create**
    
    `from django.utils.text import slugify  def unique_slug_for(title):     base = slugify(title) or "post"     candidate, i = base, 2     from .models import Post     while Post.objects.filter(slug=candidate).exists():         candidate = f"{base}-{i}"         i += 1     return candidate`
    
- **Enforce published timestamp**
    
    `# in Post.save() or clean() if self.status == Post.PUBLISHED and not self.published_at:     self.published_at = timezone.now()`
    
- **List view polish**
    
    `class PostList(ListView):     queryset = Post.objects.filter(status=Post.PUBLISHED).select_related("author")     paginate_by = 10`
    

---

## Score (with quick rationale)

|Area|Score|Why|
|---|---|---|
|**Model Clarity (5)**|**4**|Clean model and workflow; add a small diagram + model-level checks for perfection|
|**Validation Quality (6)**|**3**|Good ownership checks; add draft protection, tests, pagination, and a couple of indexes|
|**Business Fit (4)**|**2.5**|Define a couple of KPIs and a lightweight ops story|

**Total:** **9.5 / 15**  
You’re very close. Tighten draft access, add a few tests, and document success metrics, and this reads like a small, well-engineered app instead of just a working demo.

---

## Final Word

This is solid, readable Django. The code shows good instincts (server-side author assignment, published timestamping, clean URLs). With a little extra care on access control, slug safety, and a few lines of documentation/tests, you’ll check every box the rubric cares about—and it’ll feel like something you could actually hand to a teammate without a tour.