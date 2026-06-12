from app.modules.notifications.renderer import render_template_string


def test_simple_template_rendering() -> None:
    result = render_template_string("Hello {{title}}", {"title": "World"})
    assert result == "Hello World"


def test_missing_placeholder_becomes_empty_string() -> None:
    result = render_template_string("Value: {{missing}}", {})
    assert result == "Value: "
