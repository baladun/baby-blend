# BabyBlend — AI Rules

## Project

BabyBlend — web app for analyzing child-parent facial resemblance from photos. Two modes:
1. **"Who does the baby look like"** — upload mom, dad, baby photos → similarity percentages by facial zones + morphing slider
2. **"How will the baby look"** — AI-generated images from parent photos

Monetization: freemium (basic results free, HD + details via Stripe paywall).

## Architecture

Monorepo:
- `apps/api` — Python backend (FastAPI)
- `apps/web` — Frontend (Astro 5 + Svelte 5)

## Tech Stack

### Backend
| Technology | Purpose |
|---|---|
| Python 3.11 | Language |
| FastAPI + uvicorn | Web framework, ASGI server |
| Pydantic v2 | Data schemas |
| InsightFace (buffalo_l) | Face detection, embedding (512-d), landmarks (106 pts), quality score |
| OpenCV + numpy | Face morphing (Delaunay triangulation), image processing |
| onnxruntime | CPU inference for InsightFace |
| Pillow | Image resize, crop, conversion |
| SQLite | Database for MVP (sessions, files, embeddings) |
| boto3 | Cloudflare R2 storage (S3-compatible) |
| Stripe | Payments (Checkout + webhook) |
| Fal.ai / Replicate | AI image generation |
| ffmpeg | Video export |
| Docker | Containerization, deploy to Railway |

### Frontend
| Technology | Purpose |
|---|---|
| Astro 5 | Static site generator |
| Svelte 5 (runes) | UI components |
| TypeScript (strict) | Type safety |
| CSS custom properties | Styling (no Tailwind) |

## Code Style

- Functional style: logic in functions, data in Pydantic/dataclass
- Avoid service classes (UserService, Manager, etc.)
- Minimal abstractions — MVP first

## Constraints

- DO NOT add comments to code
- DO NOT commit without explicit request
- DO NOT add dependencies without discussion
- DO NOT use Tailwind
- DO NOT overengineer — simplicity > flexibility
- DO NOT generate blur versions on backend (blur via CSS on frontend)

## Priorities

- MVP first — working code > perfect code
- Simplicity > flexibility
- Existing solutions > new dependencies

## Verification

Run relevant checks based on changes:
- Backend changes: `ruff check . && pytest` (mypy optional)
- Frontend changes: `astro check && svelte-check`

## AI Communication

- Be concise
- Ask before architectural decisions
