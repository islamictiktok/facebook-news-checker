from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
from googlesearch import search

app = Flask(__name__)

# دالة لجلب محتوى المنشور من فيسبوك
def fetch_facebook_post(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        post_text = soup.find("meta", property="og:description")
        return post_text["content"] if post_text else "لم يتم العثور على النص"
    return "خطأ في جلب المنشور"

# دالة للتحقق من صحة المنشور عبر البحث عن أخبار مشابهة
def check_news_validity(text):
    try:
        query = f"{text} site:bbc.com OR site:cnn.com OR site:aljazeera.com"
        results = list(search(query))  # نستخدم البحث بدون الوسائط الإضافية
        if len(results) > 0:
            accuracy = len(results) * 10  # كل نتيجة تعتبر 10% من الصحة
            accuracy = min(accuracy, 100)  # التأكد من أن النسبة لا تتجاوز 100%
            return {"validity": "صحيح", "accuracy": accuracy}
        else:
            return {"validity": "غير صحيح", "accuracy": 0}
    except Exception as e:
        return {"validity": "خطأ في التحقق", "accuracy": 0}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        post_url = request.form.get("post_url")
        post_text = fetch_facebook_post(post_url)
        result = check_news_validity(post_text)
        return jsonify(result)  # إرسال النتيجة في شكل JSON
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
