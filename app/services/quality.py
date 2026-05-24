from app.models import ContentFormat, GeneratedContent


class ContentQualityError(ValueError):
    pass


class ContentQualityGate:
    def validate(self, content: GeneratedContent) -> None:
        if content.content_format == ContentFormat.image_based_question:
            self._validate_image_based_question(content)

    def _validate_image_based_question(self, content: GeneratedContent) -> None:
        errors: list[str] = []

        if not content.visual_description or len(content.visual_description) < 30:
            errors.append("visual_description must describe a specific medical image or visual pattern")

        if len(content.visual_labels) < 3:
            errors.append("at least 3 visual_labels are required")

        if not content.question:
            errors.append("question is required")
        else:
            lines = [line for line in content.question.splitlines() if line.strip()]
            sentence_like_parts = [part for part in content.question.replace("\n", ".").split(".") if part.strip()]
            if len(lines) < 6 and len(sentence_like_parts) < 6:
                errors.append("question must be a 6-8 line image-based stem")

        if len(content.options) < 4:
            errors.append("4 options are required")

        if not content.correct_answer:
            errors.append("correct_answer is required")

        if not content.explanation or len(content.explanation) < 180:
            errors.append("explanation must be a proper paragraph")

        if not content.relevance_rationale or len(content.relevance_rationale) < 40:
            errors.append("relevance_rationale must explain why this is high-yield")

        if not content.image_answerability or len(content.image_answerability) < 40:
            errors.append("image_answerability must explain how the image alone helps answer")

        visual_terms = " ".join(content.visual_labels + content.image_based_data).lower()
        explanation = (content.explanation or "").lower()
        if visual_terms and not any(term.lower() in explanation for term in content.visual_labels[:3]):
            errors.append("explanation must reference at least one labelled image clue")

        if errors:
            raise ContentQualityError("; ".join(errors))
