# Frontend Comparison — Angular vs Vue.js

I built the Week 3 frontend in Angular. This note compares it with Vue.js conceptually.

| Aspect           | Angular                                        | Vue.js                                                 |
| ---------------- | ---------------------------------------------- | ------------------------------------------------------ |
| Type             | Full framework (batteries included)            | Progressive framework (lighter core)                   |
| Language         | TypeScript by default                          | JavaScript or TypeScript                               |
| Structure        | Opinionated: modules, components, services, DI | Flexible; less enforced structure                      |
| Components       | Class-based with decorators (`@Component`)     | Single-file components (`.vue`): template/script/style |
| Data binding     | Two-way with `[(ngModel)]` / reactive forms    | Two-way with `v-model`                                 |
| State / services | Services + dependency injection                | Composition API / Pinia (or Vuex)                      |
| HTTP             | Built-in `HttpClient`                          | No built-in client (use `fetch`/`axios`)               |
| Learning curve   | Steeper — more concepts up front               | Gentler — easier to start small                        |

## Takeaways

- Angular gives a lot out of the box (routing, HttpClient, forms, DI), which suits larger, structured apps but means more to learn early.
- Vue is lighter and quicker to pick up, giving more freedom in how you organize things.
- For this exercise, Angular's built-in HttpClient and reactive forms made wiring the API and validation straightforward without extra libraries.

## Main challenges faced

- ***
- ***
