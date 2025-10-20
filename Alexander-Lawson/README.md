# Blog Project (Alexander-Lawson)

A Django-based blog platform supporting Markdown authoring (EasyMDE), Bootstrap 5.3 UI, and extensible for future features.

## Features
- Create, edit, and delete blog posts
- Author posts using Markdown with live preview (EasyMDE – SimpleMDE compatible)
- Responsive, modern UI with Bootstrap 5.3
- Post detail view renders Markdown as HTML
- User authentication and permissions (planned)
- Extensible for comments, tags, and more

## Project Structure
```
Alexander-Lawson/
├── blog_project/           # Django project settings
├── myblog/                # Blog app (models, views, templates)
├── templates/blog/        # Blog templates
├── docs/                  # Documentation, PRDs, ADRs, briefs
├── README.md
└── ...
```

## Setup Instructions
1. **Clone the repository:**
	```sh
	git clone <repo-url>
	cd Alexander-Lawson
	```
2. **Create and activate a virtual environment:**
	```sh
	py -m venv .venv
	.\.venv\Scripts\activate
	```
3. **Install dependencies:**
	```sh
	pip install django markdown django-widget-tweaks django-markdownify
	```
4. **Apply migrations:**
	```sh
	py manage.py migrate
	```
   If prompted for new migrations after model updates (e.g., editable publish date), run:
   ```sh
   py manage.py makemigrations
   py manage.py migrate
   ```
5. **Create a superuser (optional):**
	```sh
	py manage.py createsuperuser
	```
6. **Run the development server:**
	```sh
	py manage.py runserver
	```

## Usage
- Access the blog at `http://127.0.0.1:8000/`
- Create and edit posts using the Markdown editor (EasyMDE)
- View posts with rendered Markdown content
	- Detail page uses `markdownify`; list uses truncated `markdownify`.

## Development
- All templates use Bootstrap 5.3 for styling (Bootstrap JS via CDN). If you see a MIME type error for `/docs/5.3/dist/js/bootstrap.bundle.min.js`, ensure the base template loads the CDN: `https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js`.
- Markdown editor is EasyMDE (SimpleMDE-compatible) and is initialized with `forceSync: true` so the hidden textarea stays updated on submit.
- Project-level templates (in `templates/blog/`) override app-level templates (in `myblog/templates/blog/`). Edit project-level templates for UI changes.
- See `/docs/` for PRDs, ADRs, and Copilot briefs.

### Admin
- Posts are manageable via Django Admin. The "Publish date" (`date_created`) is editable in Admin.

## Testing
- Run tests with:
  ```sh
  py manage.py test myblog
  ```

## Troubleshooting
- Create Post button does nothing / "invalid form control ... not focusable":
	- Caused by the Markdown editor hiding the required textarea. Fixed by removing the `required` attribute and enabling EasyMDE `forceSync`.
	- Hard refresh (Ctrl+F5) after changes to clear cached JS/CSS.
- Toolbar icons are blank:
	- Ensure Font Awesome is loaded or EasyMDE `autoDownloadFontAwesome` is enabled.
- Bootstrap JS MIME error:
	- Ensure base template uses the CDN path listed above.

## Contributing
1. Fork the repo and create a feature branch
2. Make your changes (follow conventional commit style)
3. Add/modify tests as needed
4. Submit a pull request

## License
MIT License

## Admin Credentials (Development Only)
- Username: Admin
- Password: mDitka89+

> **Note:** For security, never use this password in production or public repositories. Change credentials before deployment.

---

For more details, see the [docs](./docs/) folder.
