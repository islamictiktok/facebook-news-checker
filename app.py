from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

# مفتاح API من NewsAPI
NEWS_API_KEY = "30be20afcef3449eaebfddd02b220f5a"  # استبدل بمفتاحك الخاص

# دالة لجلب محتوى المنشور من فيسبوك
def fetch_facebook_post(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        post_text = soup.find("meta", property="og:description")
        return post_text["content"] if post_text else "لم يتم العثور على النص"
    
    return "خطأ في جلب المنشور"

# دالة للتحقق من صحة المنشور عبر البحث عن أخبار مشابهة باستخدام NewsAPI
def check_news_validity(text):
    # تقليل النص إلى كلمات رئيسية (بدون علامات الترقيم)
    words = text.split()
    keywords = " ".join(words[:5])  # استخدام أول 5 كلمات من المنشور للبحث، أو يمكن تحسين ذلك

    url = f"https://newsapi.org/v2/everything?q={keywords}&language=ar&pageSize=10&sortBy=relevance&apiKey={NEWS_API_KEY}"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        articles = data.get("articles", [])

        if articles:
            # إرجاع تفاصيل المقالات (العنوان، الرابط، المصدر)
            return [
                f"<a href='{article['url']}' target='_blank'>{article['title']}</a> - <em>{article['source']['name']}</em>"
                for article in articles
            ]
        else:
            return ["❌ لم يتم العثور على أخبار مشابهة."]
    
    return ["⚠ حدث خطأ أثناء التحقق من الأخبار."]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        post_url = request.form.get("post_url")
        post_text = fetch_facebook_post(post_url)
        
        # التحقق من صحة المنشور عبر البحث عن أخبار مشابهة
        sources = check_news_validity(post_text)

        return jsonify({
            "post_text": post_text,
            "sources": sources
        })

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
