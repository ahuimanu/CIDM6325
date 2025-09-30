# Product Requirements Document (PRD)

## 1. Document Information
- Product/Feature Name: Home Maintenance Compass
- Author(s): Alexander J Lawson
- Date Created: 2025-09-21
- Last Updated: 2025-09-21
- Version: 0.1
---
## 2. Overview
- **Summary:**
  This tool is called the Home Maintenance Compass. It's purpose is to assist new homeowners in creating a personalized preventative maintenance, in addition to provided verified knowledge from nearby experts. The philosophy behind this tool is to prevent homeowners from having to make stressful and costly repairs by providing them an organized plan and access to local resources. The primary target audience are first-time buyers, specifically Millenials and Gen Z, who may never have received guidance or been mentored on what it takes to take care of a property.
  
- **Problem Statement:**
The problem we are trying to solve can be split into two parts: 1) new homeowners are often overwhelmed when it comes to taking care of their new property, which results in a reactive and stressful approach akin to whack-a-mole and 2) the advice they may get is very generic from strangers on the internet and said advice is not tailored to their specific situations or local climate.
- **Goals & Objectives:** 
  - Empower first-time homeowners to adopt a proactive approach to home maintenance.
  - Provide a methodical maintenance schedule based on a home's specific circumstances.
  - Create a community-driven knowledge base for localized tips and advice.
  - Reduce the likelihood of costly and stressful home repairs caused by neglect.

- **Non-Goals:**
The initial version of this product will not include features related to the automated ordering ordering of products or parts, e-commerce integration, professional contractor bidding, smart home device integration, or AI-driven diagnostics.

## 3. Context & Background
- **Business Context:** The product is tethered to the goal of fostering preventative home maintenance with the additional benefit of reducing insurance claims dealing with neglect. This initative would lower the volume of potential claims for both the customers and insurance providers.
- **Market/Customer Insights:** 
The persona of our target audience is first-time homeowners, particularly those in the Millennial and Gen Z generations. These individuals are digitally savvy and used to having any answer to any question at their fingertips. However, many report feelings of being blindsided by the practical realities posed by maintaining a home. They don't typically have a community of knowledgeable people they can ask questions and suffer from a consistent anxiety that their one hard asset, their home, could fall apart. According to a 2022 survey from Thumbtack, 80% of millennial homeowners and 81% of first-time buyers felt overwhelmed or stressed about upkeeping their homes amongst these generations.  Additionally, these individuals are concerned about their ability to stay financially solvent if something breaks. A May 2025 report from Kin Insurance articulated that 72% of Gen-Z and millennial first-time homebuyers encountered unexpected issues after moving in, at an average cost of over $5,000. When you factor in that most of the homes these people buy are fixer-uppers, you can understand their concern. Lastly, they feel anxious about being seen as incompetent when pursuing home repairs and some might report feeling uneasy about asking questions, if they even have someone to ask questions to. To summarize, they often feel daunted by home maintenance tasks. These individuals may not have had a mentor in "Homeownership 101" and find that reliable, specific information is scattered and unverified. There is also a market for budget-conscious users who want to extend the life of their systems and are interested in DIY solutions.

---
## 4. Scope
- **In Scope:**
  - A personalized maintenance schedule based on user inputs like home age, construction type, and climate zone.
  - Maintenance task profiles with step-by-step guides, required tools, and estimated time.
  - A localized tips module with user submission and upvoting functionality.
  - A digital log for key home information, trusted service providers, and links to articles/videos.
- **Out of Scope:** Bullet list of excluded items to prevent ambiguity.
  - Automated parts ordering or e-commerce integration.
  - Recommendations for replacement appliances or service providers based on environmental factors.
  - Professional contractor bidding or scheduling services.
  - Integration with smart home devices.
  - AI-driven diagnostics for maintenance issues.
---
## 5. User Stories & Use Cases
- **Primary User Persona(s):** First-time homeowners, budget-conscious homeowners, local community contributors and property managers.
- **User Stories:**
- As a new homeowner, I want a personalized maintenance schedule, so that I know what tasks I need to do and when to do them.
- As a DIY enthusiast, I want step-by-step guides for common tasks, and access to approachable and knowledgeable individuals, so that I can confidently and competently complete them myself.
- As a local community member, I want to provide and have access to useful tips, so that I can share my knowledge to help others and be helped if I require it.
- **Use Case Scenarios:** 
  - **Happy Path:** The ideal scenario is that a new, young homeowner creates a profile, inputs their home's details, and receives a schedule. For example, a user named John Doe would enter the home's age (1985), construction type (wood frame), her climate zone (Midwestern U.S.) and the ages of appliances.  The app would then create a customized schedule with weekly, seasonal or annual tasks such as “Clean the Gutters” or “Change the Air Filter”.  John would get a notification when it’s time to perform a task and it would have retired tools and a step-by-step guide.  They follow this schedule, marking tasks as complete, and use the task profiles for guidance on how to perform them. They would also browse the knowledge base and upvote tips for their community.
  - **Edge Cases:**
    - **A:** Jane Doe comes to own a unique, older home with a geothermal system and the app’s knowledgebase is not all that helpful because it’s an obscure home feature. When her profile’s created and the input is submitted, the scheduling tool struggles to create a schedule for her or provide any helpful information. The worst case scenario is that instead of improving the algorithm or admitting that the tool is not fully capable yet of assisting in this scenario, the app spits out a low quality result which runs the risk of a user receiving bad advice, which would run counter to the app’s overarching mission which is to reduce  stress and improve people’s situation.
    - **B:** John Doe II is an inexperienced new homeowner who attempts to use the app to solve his leaky faucet problem.  Using the Localized Tips Module, he sees a DIY suggestion with a lot of upvotes, which makes him feel secure in trying it for himself.  During the repair, something breaks (a burst pipe perhaps) which leads to substantial and expensive water damage.  The app would have an upfront and “bulletproof” disclaimer but that doesn’t prevent the user from browsing the unverified results and implementing them. This highlights the potential liability with crowd-sourced tips and the necessity of content moderation to confirm the quality of the content, as well as the need to promote a “consult a professional” advisory.

---
## 6. Functional Requirements
  - **FR-001:** The system must generate a personalized maintenance schedule based on user-provided inputs like Home Age, Climate Zone, Appliance Age/Manufacturer, etc.  This FR relates to the Happy Path scenario.
- **FR-002:** The system must provide a step-by-step guide, a list of required tools, and an estimated time for each respective maintenance task or be forthcoming in admitting the algorithm isn’t able to confidently provide helpful advice. This FR relates to the Happy Path scenario. This FR relates to the Happy Path and Edge Case A scenario.
- **FR-003:** The system must allow users to submit and upvote tips tied to a specific local area or community. This FR relates to the Happy Path.
- **FR-005:** The system must have a process/function in place for content moderators to control and verify the tips to promote good advice and eliminate bad advice. This FR relates to the Edge Case B scenario.
- **FR-006:** The system must provide a simple digital interface for a database to log key home information and vendor contact details. This FR relates to the Happy Path.
---
## 7. Non-Functional Requirements
- **Performance:** There is a crucial need for a strong, responsive system.  One metric that can be utilized to measure this is “Task Completion Rate”, which begs the requirement of a responsive and easy to use tool a user can utilize. The tool is dependent on retaining users and if the product performs poorly this is unlikely.  Another metric will be response time, which ideally will be within a couple seconds at most, if not faster, in order to evoke the feeling of receiving instant feedback. 
- **Scalability:** We anticipate a growth in users and the data they submit, especially in the “Localized Tips Module” where community contributors are expected to consistently provide tips.  To handle this, the architecture must be capable of handling higher user submissions, in the realm of several thousand users in the beginning, and many more in the future.
- **Accessibility:** It is crucial for the implementation of a strong user interface, with purpose being of preventing low user retention. The plan to address is to promote a crisp, intuitive design and utilize thorough UX testing flesh out any negative flows. 
- **Security/Compliance:** There is a concern posed by potential legal liability related to relaying/exposing individuals to crowd-sourced advice. This is explicitly addressed via a strong, easy-to-understand disclaimer, as well as an advisory to consult a professional on any and all DIY tips. While not strictly a security requirement, this falls under legal and safety compliance. Furthermore, the use of an SQL database to store general contact information for verified, trusted service providers implies a need for secure data handling.  There will also be a need for authentication, especially for administrators and content moderators.
- **Reliability/Availability:** The application must be reliable in functionality. If the application fails to meet the functional requirements above, users will deem the product to be poor and take their attention elsewhere.  This cannot happen. Therefore, it is paramount that the application does what it must do and evoke a feeling of being approachable and effective for new users.
---
## 8. Dependencies
- **Internal system dependencies:** Django API for connecting the user interace to the core modules and SQL databases.
- **External APIs/third-party services:** N/A
- **Cross-team deliverables:** N/A
---
## 9. Risks & Assumptions
- **Risks:** 
  - The algorithm for the personalized maintenance schedule becomes too complex or churns out ineffective schedules.
      - Mitigation: Focus on common inputs for the MVA and use a dynamic, flexible design which will make room for future complexity.
  - Lackluster community participation could result in low-quality or low volume in terms of localized tips.
      - Mitigation: Incentivize early adopters to contribute and seed the database with high-quality, pre-researched tips, gathered from online research.
  - Legal liability could arise if a user attempts a DIY task based on a tip and causes damage or injury.
      - Mitigation: Implement a clear, bullet-proof disclaimer which specifies tips are user-generated and strongly advise users to consult a professional.
- **Assumptions:** Preconditions believed to be true.
  - Users will be willing to provide detailed information about their homes to generate a personalized schedule.
  - A community of experienced homeowners and contractors will be willing and able to contribute tips and advice to this specific application.
---
## 10. Acceptance Criteria
- The MVA will be accepted when:
    - A basic Personalized Maintenance Schedule generates a checklist based on user inputs within mere seconds. See FR-001.
    - The Task Profiles feature contains basic, pre-written step-by-step guides for 10-15 common maintenance items, along with a list of required tools and an estimated timetable.  See FR-002.
    - The Localized Tips Module has a simple submission and upvoting system. See FR-003.
    - The Localized Tips Module has a function/process in place to moderate and verify tips for quality. See FR-004.
    - The application is capable of interfacing with a database filled with home information essential to creating work schedules and vendor contact details.  See FR-005.
---
## 11. Success Metrics
- **Task Completion Rate:** Our primary success metric is a high percentage of users mark scheduled maintenance tasks as "complete" within a defined time frame.
- **Knowledge Acquisition:** Users spend a considerable amount of time viewing and interacting with the task profiles and localized tips. This can be measured by montitoring the number of users.
- **Community Engagement:** A consistent flow of new, unique tips and questions being submitted to the Localized Tips Module. This can be measured be the number of tips and the engagement (upvotes/downvotes) associated with each post.
- **User Retention:** A high rate of users return to the app after the initial launch, especially for seasonal tasks in particular. This would be measured by monitoring traffic and the percentage of the Task Completion Rate.
---
## 12. Rollout & Release Plan
- **Phasing:** Specifically, the first phase will be the MVA, which includes a basic personalized checklist, a limited number of task guides, and a simple tips module. Subsequent cycles will focus on creating an intuitive, user-friendly setup process and seeding the core task database with 10-15 common maintenance items; further  features will be expanded based on user feedback.
- **Release Channels:** Prototype, Beta, Initial Rollout and Final Product
- **Training/Documentation Needs:** There will be support guides posted on the GitHub repository for the development and maintenance process and an easy-to-read user guide on how to use the application.
---
## 13. Open Questions
- What are the necessary inputs to include in order to create a dynamic maintenance schedule to balance effectiveness and user effort?
- How do we incentivize local community contributors to contribute to the space and ensure a consistent flow of high-quality tips?

---
## 14. References
- Links to related PRDs, design records, ADRs, technical specs, or strategy docs.
  - [https://www.kin.com/blog/generational-homeownership-survey-2025/]
  - [https://www.opendoor.com/articles/homeseller-report]  - [https://newsroom.bankofamerica.com/content/newsroom/press-releases/2025/07/confronted-with-higher-living-costs--72--of-young-adults-take-ac.html]
  - [https://blog.thumbtack.com/investing-in-home-maintenance-pays-off-yet-the-majority-of-homeowners-are-under-budgeting-84426995b6c5]
  - [https://www.thumbtack.com/guide/content/survey-home-maintenance-stress-454171293741948943.]
  - [https://partnerships.homeserve.com/water-solutions/millennial-homeowners-surprised-by-maintenance-costs-2/]
  - [https://talkerresearch.com/gen-z-millennials-fall-behind-on-this-home-necessity/]
