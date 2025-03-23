from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup

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
    search_url = f"https://www.google.com/search?q={text} site:bbc.com OR site:cnn.com OR site:aljazeera.com"
    
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(search_url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("h3")  # البحث عن عناوين الأخبار
    
        if results:
            return [result.text for result in results[:5]]  # إرجاع أول 5 نتائج
        else:
            return ["لم يتم العثور على أخبار مشابهة لتأكيد صحة المنشور."]
    
    return ["حدث خطأ أثناء التحقق من صحة الأخبار."]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        post_url = request.form.get("post_url")
        post_text = fetch_facebook_post(post_url)
        
        # التحقق من صحة المنشور
        sources = check_news_validity(post_text)
        
        return jsonify({
            "post_text": post_text,
            "sources": sources
        })
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
