# Telegram Engagement Plan

## Daily Schedule (IST)
| Time | Activity | Type |
|------|----------|------|
| 08:00 | Morning Revision | Rapid revision, concise notes, flashcards |
| 09:00 | Daily Challenge | MCQ poll |
| 14:00 | Afternoon MCQ | MCQ, clinical case, image-based |
| 20:00 | Evening Revision | PYQ, mnemonics, true/false |
| 22:00 | Weak Topic Recall | Personalized weak-spot revision |

## Engagement Features

### Streak System
- Tracks consecutive active days
- Milestone messages: 1 day 🔥, 7 days ⚡, 30 days 🏆, 100 days 👑
- Persisted to `logs/engagement/engagement_stats.json`
- Displayed in `/status` and `/engagement` commands

### Daily Challenge
- Posted at 9:00 AM IST daily
- MCQ format with poll
- Accuracy tracking per session
- Result message based on performance
- Files stored in `logs/engagement/daily_challenge.json`

### Weekly Revision Battle
- Starts Sunday 9:00 AM IST
- Ends Monday 8:00 AM IST
- Users score points by answering questions correctly
- Leaderboard with top 10 displayed
- Winner announced at end
- Scores in `logs/engagement/weekly_battle.json`

### Engagement Summary
- `/engagement` command shows: streak, accuracy, total questions, battle score
- Sent as a rich Telegram message

## Bot Commands (Admin)
| Command | Description |
|---------|-------------|
| `/mode <name>` | Set education mode |
| `/challenge` | Post daily challenge |
| `/streak` | Show current streak |
| `/battle` | Check battle status |
| `/engagement` | Show engagement summary |

## User Interaction
- All MCQ posts use Telegram polls for automated scoring
- True/False and fill-in-blank use spoiler-tagged reveal
- Streak messages sent daily via scheduler
- Weekly battle intro and results sent via scheduler

## Data Persistence
- All engagement data stored as JSON files in `logs/engagement/`
- No database required
- Restart-safe: state recovered from files on startup
- Three files: `engagement_stats.json`, `daily_challenge.json`, `weekly_battle.json`
