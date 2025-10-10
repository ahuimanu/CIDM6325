# ADR-002: Django Blog Architecture and Project Structure Organization

Date: 2025-10-10
Status: Accepted

## Context

- PRD link: [Blog Feature Set 1](../PRD_ExpenseTrackLite.markdown#blog-feature-set-1)
- Problem/forces: The Django blog implementation required several critical architectural decisions regarding project structure, technology stack, accessibility compliance, and development workflow. The initial implementation scattered blog-related files across multiple directories, creating organizational challenges for future multi-project development.
- Technical constraints: Must integrate with existing Django project structure, support multiple future projects in the same repository, maintain clean separation of concerns, and demonstrate enterprise-level development practices.

## Options

### Project Structure Organization:
- A) Keep all blog files in the root `Dewayne-Defoor/` directory alongside other project files
- B) Consolidate all blog-related files within a dedicated `blog_project/` subdirectory
- C) Create separate repositories for each project

### Technology Stack:
- A) Pure Django with basic HTML forms and minimal styling
- B) Django + Bootstrap + HTMX for enhanced UX with minimal JavaScript
- C) Django + React/Vue.js for full SPA experience

### Template and Static File Organization:
- A) App-level templates within each Django app directory
- B) Project-level centralized templates directory
- C) Hybrid approach with both app and project level templates

### Database and Content Management:
- A) Simple models with minimal relationships
- B) Comprehensive models with proper relationships, status workflow, and admin integration
- C) Headless CMS integration (Wagtail, Django CMS)

## Decision

### Project Structure: Option B
We choose to consolidate all blog-related files within `blog_project/` because:
- **Clean Separation**: Each project is self-contained and isolated
- **Scalability**: Easy to add future projects (expense tracker, etc.) without conflicts
- **Maintainability**: Clear ownership and boundaries for each project's dependencies
- **Development Workflow**: Simplified deployment and testing per project

### Technology Stack: Option B
We choose Django + Bootstrap + HTMX because:
- **Progressive Enhancement**: Works without JavaScript but enhanced with it
- **Minimal Learning Curve**: Leverages existing HTML/CSS knowledge
- **Accessibility**: Bootstrap provides accessible components out of the box
- **Performance**: HTMX enables dynamic interactions without heavy JavaScript frameworks
- **Django Integration**: Seamless integration with Django's template system

### Template Organization: Option B
We choose project-level centralized templates because:
- **Consistency**: Easier to maintain consistent styling across the application
- **Reusability**: Base templates can be shared across different apps
- **Theme Management**: Centralized location for global styling and branding

### Database Design: Option B
We choose comprehensive models with relationships because:
- **Extensibility**: Proper relationships support future feature additions
- **Data Integrity**: Foreign keys and constraints ensure data consistency
- **Workflow Support**: Status fields enable draft/published workflows
- **Admin Integration**: Rich admin interface for content management

## Architecture Components

### Models Layer
```python
# Core entities with proper relationships
Post: title, slug, content, author, status, timestamps
Comment: post (FK), author, content, timestamp
```

### Views Layer
```python
# Class-based views for consistency and extensibility
PostListView: Paginated list with published posts only
PostDetailView: Single post with related comments
```

### Template Layer
```html
# Bootstrap-based responsive templates with accessibility
base.html: Common layout with navigation and footer
post_list.html: Homepage with post cards and pagination
post_detail.html: Individual post with comment section
```

### Static Assets
- **Bootstrap 5**: CDN-delivered CSS/JS for responsive design
- **Bootstrap Icons**: Icon font for consistent iconography
- **HTMX**: CDN-delivered for dynamic interactions

## Implementation Decisions

### File Structure Organization
```
blog_project/
├── manage.py              # Django management script
├── settings.py            # Django configuration
├── db.sqlite3            # SQLite database
├── myblog/               # Blog Django app
├── templates/            # Centralized templates
├── create_sample_data.py # Data fixtures
└── README_BLOG.md        # Project documentation
```

### Accessibility Compliance (WCAG 2.2)
- Semantic HTML5 elements (`<article>`, `<nav>`, `<main>`)
- ARIA labels and descriptions for screen readers
- Keyboard navigation support
- Color contrast compliance
- Focus management

### Development Workflow
- **Testing**: Comprehensive unit tests for models and views
- **CI/CD**: GitHub Actions workflow for automated testing
- **Documentation**: Inline code documentation and README guides
- **Data Management**: Sample data fixtures for development

## Consequences

### Positive
- **Maintainability**: Clear project boundaries and consistent architecture
- **Developer Experience**: Simplified setup and clear documentation
- **User Experience**: Fast, responsive interface with smooth interactions
- **Accessibility**: Compliant with modern web standards
- **Scalability**: Architecture supports future feature additions
- **Code Quality**: Comprehensive testing and CI/CD pipeline

### Negative/Risks
- **Complexity**: More sophisticated than basic Django implementation
- **Dependencies**: Reliance on external CDNs for Bootstrap and HTMX
- **Learning Curve**: Developers need familiarity with HTMX patterns
- **File Duplication**: Some Django project files duplicated from root structure

### Migration Impact
- **Path Updates**: Required updates to settings.py BASE_DIR configuration
- **Documentation**: Updated setup instructions and file structure diagrams
- **Command Execution**: Modified Python path requirements for management commands

## Validation

### Success Metrics
- ✅ **Functionality**: All CRUD operations work correctly
- ✅ **Performance**: Pages load under 2 seconds on development server
- ✅ **Accessibility**: No critical issues reported by accessibility testing tools
- ✅ **Testing**: 100% test suite pass rate
- ✅ **Documentation**: Complete setup and usage documentation
- ✅ **Project Isolation**: Blog can be developed independently of other projects

### Rollback Plan
- If project structure complexity becomes unmanageable:
  1. Revert to flat file structure in root directory
  2. Update BASE_DIR and PYTHONPATH configurations
  3. Consolidate documentation back to root README
- If HTMX complexity becomes problematic:
  1. Remove HTMX dependencies
  2. Convert to standard Django form submissions
  3. Maintain Bootstrap styling for consistency

### Monitoring and Maintenance
- **Performance**: Monitor page load times and database query efficiency
- **Accessibility**: Regular accessibility audits using automated tools
- **Dependencies**: Keep Bootstrap and HTMX versions updated
- **Testing**: Maintain test coverage above 90%

## Related ADRs
- [ADR-001: Implement Simple Blog Page using Django Framework](./ADR-basic_blog.md)

## References
- [Django Best Practices Documentation](https://docs.djangoproject.com/)
- [HTMX Documentation](https://htmx.org/docs/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.3/)
- [WCAG 2.2 Guidelines](https://www.w3.org/WAI/WCAG22/quickref/)