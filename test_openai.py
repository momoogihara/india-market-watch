from app.services.ai_service import AIService

text = """
India's economy is expected to grow faster this year,
supported by strong domestic demand and government investment.
"""

summary = AIService.summarize(text)

print(summary)