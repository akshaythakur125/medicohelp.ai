# MedicoHelp.ai — Development Roadmap

## Vision
To become the most effective AI-powered medical exam preparation platform for Indian PG medical entrance aspirants, delivering personalised, spaced-repetition-based learning through an autonomous content engine that adapts to each learner's weak topics, preferred formats, and performance trends — all accessible via Telegram, web, and mobile.

## Current Status (v1.0-mvp-stable)
What's shipped:
- Content library: 19 MBBS subjects, 190 topics, 8 formats
- Autonomous rotation engine with format mixing and weak-topic prioritization
- SmartContentEngine with SM-2 spaced repetition
- Engagement enrichment (hooks, exam tags, memory tricks, Bloom's taxonomy)
- Analytics system
- Anti-duplication and emergency recovery
- Telegram bot with admin commands and quiz polls
- REST API for monitoring and manual control

## Short-Term (Next 30 Days)

### PostgreSQL Migration
- Replace file-based JSONL/JSON with PostgreSQL
- Motivation: concurrent write safety, query performance, scaling
- Effort: medium

### User Subscription System
- Multi-user support with Telegram-based authentication
- Per-user performance tracking
- Personalized weak-topic recommendations
- Effort: high

### Web Dashboard
- Flask/Django admin panel
- Content preview and editing
- Analytics visualisation (charts, trends)
- Manual post scheduling
- Effort: medium

### Email/Notification System
- Daily digest emails
- Weak-topic alerts
- Exam countdown reminders
- Effort: low

## Medium-Term (30-90 Days)

### AI-Powered Content Generation
- Full integration with Claude/GPT-4/Gemini for dynamic content
- Real-time MCQ generation from any textbook passage
- Image-based question generation with DALL-E/Imagen
- Effort: medium

### Mobile App (React Native / Flutter)
- Push notifications
- Offline content access
- Spaced repetition flashcards
- Progress tracking dashboard
- Effort: high

### Community Features
- User-submitted questions with moderation
- Peer discussion on each post
- Upvoting and quality ranking
- Effort: high

## Long-Term (90+ Days)

### Clinical Decision Support Integration
- Link content to clinical guidelines (API-based)
- Case-based learning pathways
- Specialty-specific content streams
- Effort: high

### Marketplace
- Premium subject packs
- Mock test series (AI-generated)
- One-on-one tutoring matching
- Effort: very high

### Multi-Language Support
- Hindi, Tamil, Bengali, etc.
- Regional language content library
- Code-switched teaching (Hinglish medical education)
- Effort: high

## Technical Debt & Improvements
- [ ] Add comprehensive type hints across all modules
- [ ] Increase test coverage to >85%
- [ ] Implement CI/CD pipeline (GitHub Actions)
- [ ] Add Docker Compose for local development
- [ ] Performance benchmark and optimization
- [ ] API versioning (v1 prefix)
- [ ] Rate limiting on REST endpoints
- [ ] HTTPS enforcement in production
