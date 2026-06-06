# Skills Router — Agent & Skill Reference

**Purpose:** Quick lookup for which agent/skill to use for any task. Auto-loaded via CLAUDE.md.

**Last Updated:** 2026-06-03
**Total Agents:** 63 | **Skills:** Available via `/skill-name` slash commands

---

## Quick Decision Tree

```
Need to PLAN something new?
  ├─ New feature or refactor → planner
  ├─ System design / tradeoffs → architect
  └─ Feature with deep codebase analysis → code-architect

Need to REVIEW code?
  ├─ General code quality → code-reviewer
  ├─ Security-sensitive code → security-reviewer
  ├─ Language-specific (.ts/.py/.go/.rs/...) → *-reviewer
  ├─ Database queries/schema → database-reviewer
  ├─ ML/MLOps code → mle-reviewer
  ├─ Accessibility audit → a11y-architect
  ├─ Silent error hunting → silent-failure-hunter
  └─ Simplification pass → code-simplifier

Need to FIX something broken?
  ├─ Build/compile errors → *-build-resolver
  ├─ Tests failing → tdd-guide
  └─ Performance issues → performance-optimizer

Need to WRITE tests?
  ├─ New feature (TDD) → tdd-guide
  ├─ E2E flows → e2e-runner
  └─ PR test coverage check → pr-test-analyzer

Need to RESEARCH / EXPLORE?
  ├─ Understand existing code → code-explorer
  ├─ Library/API docs → docs-lookup
  └─ Conversation analysis → conversation-analyzer

Need MAINTENANCE?
  ├─ Dead code removal → refactor-cleaner
  ├─ Documentation updates → doc-updater
  └─ Performance optimization → performance-optimizer
```

---

## 1. Architecture & Planning

| Agent | What | When to Use | Why (Model) | Example Triggers |
|-------|------|-------------|-------------|------------------|
| **planner** | Creates detailed implementation plans with phases, file paths, risks, and testing strategy | Before implementing any complex feature or refactor. PROACTIVE use. | Opus — deep reasoning for multi-phase plans | "Add user authentication", "Refactor the payment system", "Implement dark mode" |
| **architect** | Designs system architecture, evaluates trade-offs, creates ADRs | Architectural decisions, new system design, scaling concerns | Opus — requires architectural depth | "Should we use Redis or Postgres for caching?", "Design a notification system", "How should we split our monolith?" |
| **code-architect** | Analyzes codebase patterns then provides implementation blueprints with concrete files, interfaces, and build order | Implementing features that need to match existing conventions | Sonnet — fast, pattern-matching | "Add a new CRUD endpoint matching our existing patterns", "Implement a new service following our conventions" |

---

## 2. Code Review & Quality

| Agent | What | When to Use | Why (Model) | Example Triggers |
|-------|------|-------------|-------------|------------------|
| **code-reviewer** | Reviews code for quality, security, maintainability. Outputs CRITICAL/HIGH/MEDIUM/LOW findings. | **MUST USE** after writing or modifying any code | Sonnet — fast, thorough | After every code change. "Review my changes", before any commit |
| **code-simplifier** | Simplifies and refines code for clarity, consistency, and maintainability. Preserves behavior. | After code-reviewer or when code feels overcomplicated | Sonnet | "This function is too complex", "Simplify this module", "Clean up this component" |
| **silent-failure-hunter** | Finds swallowed errors, bad fallbacks, missing error propagation, empty catch blocks | After error handling changes, before production deployment | Sonnet | "Check if we're silently swallowing errors", "audit error handling in the API layer" |
| **comment-analyzer** | Analyzes code comments for accuracy, completeness, maintainability, and comment rot risk | When comments seem stale, before releases, during code review | Sonnet | "Are these comments still accurate?", "audit docstrings for rot" |
| **type-design-analyzer** | Analyzes type design for encapsulation, invariant expression, usefulness, and enforcement | Type-heavy refactors, API design, library boundaries | Sonnet | "Review our domain types", "Are these types well-designed?" |
| **pr-test-analyzer** | Reviews pull request test coverage quality and completeness, emphasis on behavioral coverage | Before merging PRs | Sonnet | "Check if this PR has enough tests" |

---

## 3. Security

| Agent | What | When to Use | Why (Model) | Example Triggers |
|-------|------|-------------|-------------|------------------|
| **security-reviewer** | Detects OWASP Top 10, secrets, injection, unsafe crypto, SSRF. Flags CRITICAL issues. | **PROACTIVE** after auth, payment, user input, API, or file system code changes | Sonnet | Any auth change, new API endpoint, user input handling, payment code, file uploads |

---

## 4. Testing

| Agent | What | When to Use | Why (Model) | Example Triggers |
|-------|------|-------------|-------------|------------------|
| **tdd-guide** | Enforces write-tests-first methodology. Red-Green-Refactor cycle. 80%+ coverage. | **PROACTIVE** for new features, bug fixes, refactoring | Sonnet | "Add a new feature", "Fix this bug", "Refactor this module" |
| **e2e-runner** | Creates and runs E2E tests with Playwright. Manages flaky tests, artifacts, screenshots. | Critical user flows (auth, payments, core features). **PROACTIVE** for UI changes | Sonnet | "Test the login flow end-to-end", "Add E2E tests for checkout", "Debug flaky test" |

---

## 5. Language-Specific Reviewers

### Web & TypeScript Ecosystem

| Agent | What | When to Use | Why (Model) | Example Triggers |
|-------|------|-------------|-------------|------------------|
| **typescript-reviewer** | Type safety, async correctness, Node/web security, idiomatic TS/JS | All `.ts`/`.tsx`/`.js` changes. **MUST USE** for TS/JS projects | Sonnet | Any TypeScript/JavaScript change |
| **react-reviewer** | React hooks, render performance, RSC boundaries, a11y, React security | All `.tsx`/`.jsx` changes. **MUST USE** for React projects | Sonnet | React component changes, hook usage, state management |
| **react-build-resolver** | Fixes React build failures (Vite, webpack, Next.js, CRA) | When React build fails | Sonnet | `npm run build` failing in a React project |

### Python Ecosystem

| Agent | What | When to Use | Why (Model) | Example Triggers |
|-------|------|-------------|-------------|------------------|
| **python-reviewer** | PEP 8, Pythonic idioms, type hints, security, performance | All `.py` changes. **MUST USE** for Python projects | Sonnet | Any Python change |
| **django-reviewer** | ORM correctness, DRF patterns, migration safety, security | Django project changes. **MUST USE** for Django | Sonnet | Django model/view/serializer changes |
| **fastapi-reviewer** | Async correctness, DI, Pydantic schemas, security, OpenAPI | FastAPI project changes | Sonnet | FastAPI endpoint, dependency, or schema changes |

### JVM Ecosystem

| Agent | What | When to Use | Why (Model) | Example Triggers |
|-------|------|-------------|-------------|------------------|
| **java-reviewer** | Spring Boot/Quarkus layered architecture, JPA, security, concurrency | All `.java` changes. **MUST USE** for Java projects | Sonnet | Any Java change |
| **kotlin-reviewer** | Idiomatic Kotlin, coroutines, Compose, clean architecture | All `.kt` changes. **MUST USE** for Kotlin projects | Sonnet | Any Kotlin change |

### Systems Languages

| Agent | What | When to Use | Why (Model) | Example Triggers |
|-------|------|-------------|-------------|------------------|
| **rust-reviewer** | Ownership, lifetimes, error handling, unsafe usage, idiomatic Rust | All `.rs` changes. **MUST USE** for Rust projects | Sonnet | Any Rust change |
| **cpp-reviewer** | Memory safety, modern C++, concurrency, performance | All `.cpp`/`.h` changes. **MUST USE** for C++ projects | Sonnet | Any C++ change |
| **go-reviewer** | Idiomatic Go, concurrency (goroutines/channels), error handling | All `.go` changes. **MUST USE** for Go projects | Sonnet | Any Go change |

### Mobile & UI

| Agent | What | When to Use | Why (Model) | Example Triggers |
|-------|------|-------------|-------------|------------------|
| **swift-reviewer** | Protocol-oriented design, value semantics, ARC, Swift Concurrency | All `.swift` changes. **MUST USE** for Swift projects | Sonnet | Any Swift change |
| **flutter-reviewer** | Widget best practices, state management, Dart idioms, a11y | Flutter/Dart changes. **MUST USE** for Flutter | Sonnet | Any `.dart` change |
| **csharp-reviewer** | .NET conventions, async patterns, nullable types, security | All `.cs` changes. **MUST USE** for C# projects | Sonnet | Any C# change |
| **fsharp-reviewer** | Functional idioms, type safety, pattern matching, computation expressions | All `.fs` changes. **MUST USE** for F# projects | Sonnet | Any F# change |

### Specialized Reviewers

| Agent | What | When to Use | Why (Model) | Example Triggers |
|-------|------|-------------|-------------|------------------|
| **database-reviewer** | PostgreSQL query optimization, schema design, security, Supabase best practices | SQL queries, migrations, schema design, DB performance | Sonnet | "Review this migration", "Optimize this query", "Design this schema" |
| **healthcare-reviewer** | Clinical safety, CDSS accuracy, PHI compliance, medical data integrity | EMR/EHR, CDSS, health information systems | Sonnet | Healthcare application code changes |
| **mle-reviewer** | Data contracts, feature pipelines, training reproducibility, model serving, monitoring | ML/MLOps code, model training, inference, evaluation | Sonnet | "Review this training pipeline", "Check this model serving code" |
| **a11y-architect** | WCAG 2.2 compliance for Web and Native platforms | UI component design, design systems, accessibility audits | Sonnet | "Is this component accessible?", "Audit our design system for a11y" |

---

## 6. Language-Specific Build Resolvers

| Agent | What | When to Use | Why (Model) | Example Triggers |
|-------|------|-------------|-------------|------------------|
| **build-error-resolver** | Fixes general TypeScript/JS build errors, type errors, module resolution | When `npm run build` or `tsc` fails | Sonnet | Build failures in TS/JS projects |
| **cpp-build-resolver** | Fixes C++ build, CMake, linker, template errors | When C++ build fails | Sonnet | `cmake --build` or `make` failures |
| **dart-build-resolver** | Fixes Dart/Flutter analysis errors, compilation, dependency conflicts | When `dart analyze` or Flutter build fails | Sonnet | Flutter compilation failures |
| **django-build-resolver** | Fixes pip/Poetry errors, migration conflicts, Django config issues | When Django setup/startup fails | Sonnet | Migration conflicts, `collectstatic` failures |
| **go-build-resolver** | Fixes Go build, vet, linter errors | When `go build` or `go vet` fails | Sonnet | Go compilation errors |
| **java-build-resolver** | Fixes Maven/Gradle, Java compiler errors | When Java build fails | Sonnet | Maven/Gradle build failures |
| **kotlin-build-resolver** | Fixes Kotlin/Gradle, compiler errors | When Kotlin build fails | Sonnet | Kotlin compilation errors |
| **pytorch-build-resolver** | Fixes tensor shapes, device errors, gradient issues, DataLoader, mixed precision | When PyTorch training/inference crashes | Sonnet | CUDA errors, shape mismatches, DataLoader issues |
| **rust-build-resolver** | Fixes cargo build, borrow checker, Cargo.toml issues | When `cargo build` fails | Sonnet | Rust compilation errors |
| **swift-build-resolver** | Fixes Swift/Xcode build, SPM dependency, code signing issues | When Swift/Xcode build fails | Sonnet | Xcode build failures |
| **react-build-resolver** | Fixes React build failures across bundlers (Vite, webpack, Next.js) | When React project build fails | Sonnet | JSX/TSX compile errors, hydration mismatches |

---

## 7. Specialized Domains

### Networking & Infrastructure

| Agent | What | When to Use | Why (Model) | Example Triggers |
|-------|------|-------------|-------------|------------------|
| **homelab-architect** | Designs home/lab network plans from hardware inventory and goals | Planning or upgrading home networks | Sonnet | "Design a network for my home lab", "Segment my VLANs" |
| **network-architect** | Designs enterprise/multi-site network architecture | Enterprise network design from requirements | Sonnet | "Design our branch office network", "Plan network redundancy" |
| **network-config-reviewer** | Reviews router/switch configs for security, correctness, stale references | Before network change windows | Sonnet | "Review this switch config before deployment" |
| **network-troubleshooter** | Diagnoses connectivity, routing, DNS, interface, policy issues (read-only) | Network issues, connectivity problems | Sonnet | "Why can't host A reach host B?", "Debug this routing issue" |

### DevOps & Operations

| Agent | What | When to Use | Why (Model) | Example Triggers |
|-------|------|-------------|-------------|------------------|
| **harness-optimizer** | Analyzes and improves local agent harness config for reliability, cost, throughput | When agent performance/cost needs tuning | Sonnet | "Optimize my harness config", "Reduce token usage" |
| **loop-operator** | Operates autonomous agent loops, monitors progress, intervenes when loops stall | Managing long-running autonomous agent loops | Sonnet | "Monitor this autonomous loop", "Check loop progress" |

### Business & Communication

| Agent | What | When to Use | Why (Model) | Example Triggers |
|-------|------|-------------|-------------|------------------|
| **marketing-agent** | Marketing strategy, copywriting, campaign planning, content creation | Product launches, marketing campaigns | Sonnet | "Write landing page copy", "Plan our email campaign", "Draft social posts" |
| **seo-specialist** | Technical SEO audits, on-page optimization, structured data, Core Web Vitals | Site audits, meta tag reviews, schema markup | Sonnet | "Audit our site for SEO", "Add structured data", "Fix Core Web Vitals" |
| **chief-of-staff** | Email/Slack/LINE/Messenger triage, draft replies, follow-through enforcement | Managing multi-channel communications | Sonnet | "Triage my inbox", "Draft replies to these messages" |

### Specialized Platforms

| Agent | What | When to Use | Why (Model) | Example Triggers |
|-------|------|-------------|-------------|------------------|
| **harmonyos-app-resolver** | ArkTS/ArkUI development, V2 state management, Navigation routing | HarmonyOS/OpenHarmony projects | Sonnet | HarmonyOS app development, ArkUI component review |

### Open Source Pipeline

| Agent | What | When to Use | Why (Model) | Example Triggers |
|-------|------|-------------|-------------|------------------|
| **opensource-forker** | Copies files, strips secrets (20+ patterns), replaces internal refs, cleans git history | Preparing a project for open-sourcing (Stage 1) | Sonnet | "Prepare this repo for open source" |
| **opensource-sanitizer** | Verifies fork is clean. Scans for leaked secrets, PII, internal refs. PASS/FAIL report | Before public release (Stage 2) | Sonnet | "Sanitize check before public release" |
| **opensource-packager** | Generates CLAUDE.md, README, LICENSE, CONTRIBUTING.md, issue templates | Final packaging for open source (Stage 3) | Sonnet | "Package this project for GitHub" |

---

## 8. Maintenance & Performance

| Agent | What | When to Use | Why (Model) | Example Triggers |
|-------|------|-------------|-------------|------------------|
| **refactor-cleaner** | Finds and removes dead code, duplicates, unused deps. Runs knip/depcheck/ts-prune. | Code maintenance sprints, technical debt reduction. NOT during active feature dev. | Sonnet | "Clean up dead code", "Remove unused dependencies", "Consolidate duplicates" |
| **doc-updater** | Updates codemaps and documentation from actual code. Generates docs/CODEMAPS/*. | After major features, API changes, architecture changes | Haiku — frequent, cheap | "Update our docs", "Generate codemaps", "Refresh README" |
| **performance-optimizer** | Profiling, bottleneck identification, bundle size reduction, render optimization | Performance issues, slow pages, large bundles. PROACTIVE for optimization. | Sonnet | "This page is slow", "Reduce our bundle size", "Optimize render performance" |

---

## 9. Research & Exploration

| Agent | What | When to Use | Why (Model) | Example Triggers |
|-------|------|-------------|-------------|------------------|
| **code-explorer** | Traces execution paths, maps architecture layers, documents dependencies | Understanding how existing features work, onboarding to codebase areas | Sonnet (read-only) | "How does the auth system work?", "Map the payment flow", "What are the dependencies of this module?" |
| **docs-lookup** | Fetches current library/framework docs and code examples via Context7 MCP | Library/API usage questions, version-specific details | Sonnet | "How do I use React Server Components?", "What's the API for sqlalchemy 2.0?" |
| **conversation-analyzer** | Analyzes conversation transcripts to find behaviors worth preventing with hooks | Triggered by /hookify | Sonnet | "/hookify", "What hooks should I add?" |

---

## 10. GAN Harness (Generative-Adversarial Development)

| Agent | What | When to Use | Why (Model) | Example Triggers |
|-------|------|-------------|-------------|------------------|
| **gan-planner** | Expands a one-line prompt into a full product spec with features, sprints, eval criteria | Starting a new product/prototype from a high-level idea | Sonnet | "Build a todo app", "Create a chat application" |
| **gan-generator** | Implements features according to spec, reads evaluator feedback, iterates | Building features in GAN workflow | Sonnet | "Implement sprint 1 features", "Fix evaluator issues" |
| **gan-evaluator** | Tests live app via Playwright, scores against rubric, provides feedback | Evaluating GAN-generated features | Sonnet | "Evaluate sprint 1", "Score the current build" |

---

## 11. Agent Selection by Project Type

| If your project is... | Default reviewers | Default build resolvers |
|-----------------------|-------------------|------------------------|
| **TypeScript/Node.js** | typescript-reviewer, code-reviewer | build-error-resolver |
| **React/Next.js** | react-reviewer, typescript-reviewer, code-reviewer | react-build-resolver |
| **Python/FastAPI** | python-reviewer, fastapi-reviewer | — |
| **Python/Django** | django-reviewer, python-reviewer | django-build-resolver |
| **Go** | go-reviewer | go-build-resolver |
| **Rust** | rust-reviewer | rust-build-resolver |
| **Java/Spring Boot** | java-reviewer | java-build-resolver |
| **Kotlin** | kotlin-reviewer | kotlin-build-resolver |
| **C++** | cpp-reviewer | cpp-build-resolver |
| **C#** | csharp-reviewer | — |
| **F#** | fsharp-reviewer | — |
| **Swift/iOS** | swift-reviewer | swift-build-resolver |
| **Flutter/Dart** | flutter-reviewer | dart-build-resolver |
| **React Native** | react-reviewer, typescript-reviewer | build-error-resolver |
| **HarmonyOS** | harmonyos-app-resolver | — |
| **ML/PyTorch** | mle-reviewer, python-reviewer | pytorch-build-resolver |
| **PostgreSQL** | database-reviewer | — |
| **Healthcare** | healthcare-reviewer | — |

---

## 12. Skill Slash Commands

Skills are invoked via `/skill-name` slash commands:

| Skill | Category | What it does |
|-------|----------|-------------|
| `/code-review` | Quality | Code quality review (code-reviewer agent) |
| `/security-review` | Security | Security vulnerability scan |
| `/simplify` | Quality | Simplify and clean up code |
| `/verify` | Testing | Run app and verify behavior |
| `/test-coverage` | Testing | Check and improve test coverage |
| `/build-fix` | Build | Fix build errors |
| `/refactor-clean` | Maintenance | Dead code removal |
| `/update-docs` | Maintenance | Update documentation |
| `/update-codemaps` | Maintenance | Generate codemap files |
| `/plan` | Planning | Create implementation plan |
| `/pr` | Git | Create pull request |
| `/review-pr` | Review | Review a pull request |
| `/feature-dev` | Development | Full feature development workflow |
| `/tdd` | Testing | Test-driven development workflow |
| `/evolve` | Development | Iterative improvement loop |
| `/loop` | Operations | Run recurring task on interval |
| `/hookify` | Config | Create hooks from conversation analysis |
| `/project-init` | Setup | Initialize new project |
| `/init` | Setup | Initialize Claude Code in project |
| `/run` | Operations | Launch and test app |
| `/deep-research` | Research | Multi-source cited research report |
| `/frontend-design` | Design | Frontend UI design direction |

---

## Usage Notes

1. **MUST USE** agents should always be invoked for their target language/project type — no discretion.
2. **PROACTIVE** agents should be used without the user asking — the context makes it obvious.
3. **Model columns** indicate the default model; override via `model:` param if needed.
4. **Read-only agents** (code-explorer, architect, planner) can explore but cannot edit files.
5. **Parallel execution** — independent agents can and should run concurrently (e.g., security-reviewer + typescript-reviewer on the same diff).
