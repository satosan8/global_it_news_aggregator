import requests
from bs4 import BeautifulSoup

def get_news(url, site_name, tag, class_name=None):
    """Универсальная функция для сбора новостей"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Поиск заголовков (логика поиска немного отличается для разных сайтов)
        if class_name:
            articles = soup.find_all(tag, class_=class_name, limit=5)
        else:
            articles = soup.find_all(tag, limit=5)

        print(f"\n--- {site_name.upper()} ---")
        if not articles:
            print("Не удалось найти заголовки. Возможно, структура сайта изменилась.")
        
        for i, article in enumerate(articles, 1):
            title = article.get_text(strip=True)
            print(f"{i}. {title}")
            
    except Exception as e:
        print(f"Ошибка при чтении {site_name}: {e}")

def main():
    print("=== STARTING IT NEWS AGGREGATOR (2026 Edition) ===")
    
    # 1. Hacker News (Английский - Мировое комьюнити)
    get_news('https://news.ycombinator.com', 'Hacker News', 'span', 'titleline')
    
    # 2. The Verge (Английский - Гаджеты и Технологии)
    get_news('https://www.theverge.com', 'The Verge', 'h2')
    
    # 3. TechCrunch (Английский - Стартапы и Инвестиции)
    get_news('https://techcrunch.com', 'TechCrunch', 'h2', 'wp-block-post-title')
    
    # 4. Habr (Русский - Крупнейший IT ресурс в СНГ)
    get_news('https://habr.com', 'Habr', 'h2', 'tm-title tm-title_h2')

if __name__ == "__main__":
    main()
