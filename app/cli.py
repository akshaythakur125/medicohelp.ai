import argparse
import asyncio
import json

from app.config import get_settings
from app.logging_config import configure_logging
from app.models import ContentCategory, ContentFormat, NewsTopic, Subject
from app.services.orchestrator import PostOrchestrator


async def main() -> None:
    parser = argparse.ArgumentParser(description="Generate or post MedicoHelp AI content.")
    parser.add_argument("--category", choices=[category.value for category in ContentCategory], default=None)
    parser.add_argument("--subject", choices=[subject.value for subject in Subject], default=None)
    parser.add_argument("--format", choices=[content_format.value for content_format in ContentFormat], default=None)
    parser.add_argument("--all-subjects", action="store_true", help="Generate one post for each MBBS subject.")
    parser.add_argument("--news-topic", choices=[topic.value for topic in NewsTopic], default=None)
    parser.add_argument("--post", action="store_true", help="Publish generated poster to Telegram.")
    parser.add_argument("--instagram", action="store_true", help="Generate and post an Instagram carousel.")
    parser.add_argument("--instagram-topic", default=None, metavar="TOPIC",
                        help="Ophthalmology topic for the Instagram carousel (random if omitted).")
    args = parser.parse_args()

    settings = get_settings()
    configure_logging(settings)
    orchestrator = PostOrchestrator(settings)

    category = ContentCategory(args.category) if args.category else None
    subject = Subject(args.subject) if args.subject else None
    content_format = ContentFormat(args.format) if args.format else None
    news_topic = NewsTopic(args.news_topic) if args.news_topic else None

    if args.instagram or args.instagram_topic:
        result = await orchestrator.generate_instagram_post(topic=args.instagram_topic)
        print(json.dumps(result, indent=2))
        return

    if news_topic:
        result = await orchestrator.generate_news_post(topic=news_topic, publish_to_telegram=args.post)
        print(result.model_dump_json(indent=2))
        return
    if args.all_subjects:
        results = []
        for selected_subject in Subject:
            result = await orchestrator.generate_post(
                subject=selected_subject,
                content_format=content_format,
                publish_to_telegram=args.post,
            )
            results.append(result.model_dump(mode="json"))
        print(json.dumps(results, indent=2))
        return

    result = await orchestrator.generate_post(
        subject=subject,
        content_format=content_format,
        category=category,
        publish_to_telegram=args.post,
    )
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())
