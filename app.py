from flask import Flask, request, jsonify
from googlesearch import search

app = Flask(__name__)

def check_news_validity(news_text):
    """التحقق من صحة الخبر من خلال البحث عنه في Google"""
    query = news_text + " site:bbc.com OR site:cnn.com OR site:reuters.com OR site:aljazeera.net"
    search_results = list(search(query, num_results=5))

    if search_results:
        return {"status": "صحيح", "sources": search_results}
    else:
        return {"status": "غير مؤكد", "sources": []}

@app.route('/check_news', methods=['POST'])
def check_news():
    data = request.get_json()
    news_text = data.get("news_text", "")

    if not news_text:
        return jsonify({"error": "يرجى إرسال نص الخبر"}), 400

    result = check_news_validity(news_text)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
