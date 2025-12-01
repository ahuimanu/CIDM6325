# Discussion — Modular Design & Scalability in Django  
*Tan Vu | CIDM 6325 Weeks 7–8*

Django’s app-based modular design turns large projects into orchestrated collections of small, reusable units. Each app acts as a micro-module with its own models, templates, and URLs. When refactoring my blog from Function-Based Views (FBVs) to Class-Based Views (CBVs), I observed how this modularity enabled horizontal scaling without code bloat.

CBVs encapsulate patterns like Create/Update/Delete into generic classes, dramatically reducing duplication. Inheritance and mixins—`LoginRequiredMixin`, `PermissionRequiredMixin`, and `AuthorRequiredMixin`—became reusable blocks of logic across multiple apps. This inheritance structure mirrors real-world team scaling: as teams grow, each developer can extend a base class rather than rewrite workflows.

Modularity also improves maintainability. By isolating responsibilities—models handle persistence, views orchestrate flow, and templates render presentation—errors remain localized. When the `Post` schema expanded with Tags and Categories, the rest of the app required minimal change.

However, modularity introduces its own governance challenges. Without documentation, CBV hierarchies can feel opaque. Teams must agree on naming conventions and review mixin order to avoid method-resolution confusion. Django’s strict folder conventions and CI automation mitigate this risk.

From a scalability perspective, modularity supports both vertical (feature growth) and horizontal (team growth) expansion. Apps can be deployed independently, versioned, or replaced—key properties of sustainable software.

**AI Disclosure:** I used ChatGPT (GPT-5) to brainstorm discussion points and verify CBV terminology. All narrative, structure, and examples were rewritten and validated manually to ensure originality and accuracy.
