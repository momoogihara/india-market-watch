import os
from openai import OpenAI
import json


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

#AIサービスを1本化する
class AIService:

    @staticmethod
    def analyze_article(content: str):

        prompt = f"""
            You are a financial news analyst.

            Return ONLY valid JSON.
            Do not include markdown.
            Do not include backticks.

            Strict rules:
            - sector must be EXACTLY one of: 
                IT
                ,Banking
                ,Finance
                ,Energy
                ,FMCG
                ,Auto
                ,Telecom
                ,Pharma
                ,Healthcare
                ,Consumer
                ,Retail
                ,Infrastructure
                ,Real Estate
                ,Metals
                ,Manufacturing
                ,Otherr
            - sentiment must be one of: Bullish, Bearish, Neutral

            Output format:
            {{
            "summary": "short summary",
            "sentiment": "Bullish / Bearish / Neutral",
            "sector":  "IT / Banking / Finance / Energy / FMCG / Auto / Telecom / Pharma / Healthcare / Consumer / Retail / Infrastructure / Real Estate / Metals / Manufacturing / Other"
            }}
            Sector definitions:

            IT = software, technology, digital services

            Banking = banks and lenders

            Finance = insurance, mutual funds, asset management

            Telecom = telecom operators, mobile services

            Pharma = drug makers and pharmaceutical companies

            Healthcare = hospitals and healthcare providers

            Consumer = consumer brands and discretionary spending

            Retail = retail chains and e-commerce

            Infrastructure = roads, ports, airports, construction

            Real Estate = housing and property development

            Metals = steel, aluminum, mining

            Manufacturing = industrial production and factories

            Energy = oil, gas, power, renewable energy

            FMCG = packaged consumer goods

            Auto = automobile manufacturers and suppliers

            Use Other only when no sector clearly matches.

            Article:
            {content}
            """

        try:

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0
            )

            return response.choices[0].message.content

        except Exception as e:

            print(f"OPENAI ERROR: {e}")

            return json.dumps({
                "summary": "",
                "sentiment": "Neutral",
                "sector": "Other"
            })
    
    
    @staticmethod
    def safe_parse_ai_response(response_text: str) -> dict:

        default_data = {
            "summary": "",
            "sentiment": "Neutral",
            "sector": "Other"
        }

        try:
            data = json.loads(response_text)

            summary = data.get("summary", "")
            sentiment = data.get("sentiment", "Neutral")
            sector = data.get("sector", "Other")

            # summary検証
            if not isinstance(summary, str):
                summary = ""

            summary = summary.strip()
            summary = summary[:500]

            # sentiment検証
            allowed_sentiments = [
                "Bullish",
                "Bearish",
                "Neutral"
            ]

            if sentiment not in allowed_sentiments:
                sentiment = "Neutral"

            # sector検証
            allowed_sectors = [
                "IT",
                "Banking",
                "Finance",
                "Energy",
                "FMCG",
                "Auto",
                "Telecom",
                "Pharma",
                "Healthcare",
                "Consumer",
                "Retail",
                "Infrastructure",
                "Real Estate",
                "Metals",
                "Manufacturing",
                "Other"
            ]

            if sector not in allowed_sectors:
                sector = "Other"

            return {
                "summary": summary,
                "sentiment": sentiment,
                "sector": sector
            }

        except Exception:
            return default_data

    #AI市場サマリー生成機能DAY17
    @staticmethod
    def generate_market_summary(
        snapshot: dict,
        news_summaries: list[str]
    ) -> str:

            prompt = f"""
            You are a professional financial analyst.

            Analyze the following Indian market data.

            Market Snapshot:
            {snapshot}

            Recent News:
            {news_summaries}

            Return:
            - 3 to 5 sentences
            - Professional tone
            - Mention key sectors
            - Mention possible drivers
            """

            try:

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.3
                )

                return response.choices[0].message.content.strip()

            except Exception as e:

                print(f"MARKET SUMMARY ERROR: {e}")

                return "Market summary unavailable."   
            


# class AIService:

#     @staticmethod
#     def summarize(text: str) -> str:

#         if not text:
#             return ""

#         response = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[
#                 {
#                     "role": "system",
#                     "content": (
#                         "あなたは経済ニュースのアナリストです。"
#                         "記事を日本語で3行程度に要約してください。"
#                     ),
#                 },
#                 {
#                     "role": "user",
#                     "content": text,
#                 },
#             ],
#             temperature=0.3,
#         )

#         return response.choices[0].message.content
    
#     @staticmethod
#     def classify(text: str) -> str:

#         prompt = f"""
#     Classify the following news article into exactly one category.

#     Categories:
#     - Stock
#     - Economy
#     - Policy
#     - Company
#     - Currency
#     - Other

#     Return only category name.

#     Article:
#     {text}
#     """

#         response = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[
#                 {
#                     "role": "user",
#                     "content": prompt
#                 }
#             ],
#             temperature=0
#         )

#         return response.choices[0].message.content.strip()


#     @staticmethod
#     def analyze_sentiment(text: str) -> str:

#         prompt = f"""
#     Classify the sentiment of this financial news.

#     Return only one word:
#     Bullish
#     Bearish
#     Neutral

#     Article:
#     {text}
#     """

#         response = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[
#                 {"role": "user", "content": prompt}
#             ],
#             temperature=0
#         )

#         return response.choices[0].message.content.strip().split()[0]

