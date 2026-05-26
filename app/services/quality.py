from app.models import ContentFormat, GeneratedContent

_MIN_VISUAL_DESC_LEN = 30
_MIN_VISUAL_LABELS = 3
_MIN_STEM_LINES = 6
_MIN_OPTIONS = 4
_MIN_EXPLANATION_LEN = 180
_MIN_RELEVANCE_LEN = 40
_MIN_ANSWERABILITY_LEN = 40


class ContentQualityError(ValueError):
    pass


class ContentQualityGate:
    def validate(self, content: GeneratedContent) -> None:
        if content.content_format == ContentFormat.image_based_question:
            self._validate_image_based_question(content)

    def _validate_image_based_question(self, content: GeneratedContent) -> None:
        errors: list[str] = []

        if not content.visual_description or len(content.visual_description) < _MIN_VISUAL_DESC_LEN:
            errors.append("visual_description must describe a specific medical image or visual pattern")

        if len(content.visual_labels) < _MIN_VISUAL_LABELS:
            errors.append("at least 3 visual_labels are required")

        if not content.question:
            errors.append("question is required")
        else:
            lines = [line for line in content.question.splitlines() if line.strip()]
            sentence_like_parts = [part for part in content.question.replace("\n", ".").split(".") if part.strip()]
            if len(lines) < _MIN_STEM_LINES and len(sentence_like_parts) < _MIN_STEM_LINES:
                errors.append("question must be a 6-8 line image-based stem")

        if len(content.options) < _MIN_OPTIONS:
            errors.append("4 options are required")

        if not content.correct_answer:
            errors.append("correct_answer is required")

        if not content.explanation or len(content.explanation) < _MIN_EXPLANATION_LEN:
            errors.append("explanation must be a proper paragraph")

        if not content.relevance_rationale or len(content.relevance_rationale) < _MIN_RELEVANCE_LEN:
            errors.append("relevance_rationale must explain why this is high-yield")

        if not content.image_answerability or len(content.image_answerability) < _MIN_ANSWERABILITY_LEN:
            errors.append("image_answerability must explain how the image alone helps answer")

        visual_terms = " ".join(content.visual_labels + content.image_based_data).lower()
        explanation = (content.explanation or "").lower()
        if visual_terms and not any(term.lower() in explanation for term in content.visual_labels[:3]):
            errors.append("explanation must reference at least one labelled image clue")

        if errors:
            raise ContentQualityError("; ".join(errors))
