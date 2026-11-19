# Online Book Store – Backend (Django)

## Setup
```bash
python -m venv venv && source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_data          # optional demo books
export GEMINI_API_KEY=your-key      # Windows: set GEMINI_API_KEY=your-key
python manage.py runserver
```
Admin panel: http://127.0.0.1:8000/admin/   |   Tests: `python manage.py test`

## URL map
| URL | Name | Method | Purpose |
|---|---|---|---|
| `/` | store:home | GET | Best sellers, new arrivals, audiobooks |
| `/books/` | store:book_list | GET | All books. Query: `q`, `sort` (new, price_asc, price_desc, rating, title), `section` (best_sellers, new_arrivals, audiobooks), `page` |
| `/category/<slug>/` | store:category | GET | Books in a category (same query params) |
| `/books/<slug>/` | store:book_detail | GET | Book page |
| `/books/<slug>/summary/` | store:book_summary | GET | **JSON** AI summary `{summary, cached}` or `{error}` (502). `?refresh=1` regenerates |
| `/subscribe/` | store:subscribe | POST `email` | Newsletter |
| `/cart/` | store:cart | GET | Cart page |
| `/cart/add/<book_id>/` | store:cart_add | POST `quantity` | Add to cart |
| `/cart/update/<item_id>/` | store:cart_update | POST `quantity` | Set quantity (0 removes) |
| `/cart/remove/<item_id>/` | store:cart_remove | POST | Remove item |
| `/checkout/` | store:checkout | GET/POST `full_name,email,phone,address` | Dummy checkout |
| `/order/<id>/success/` | store:order_success | GET | Confirmation |

POST endpoints (subscribe, cart_*) return JSON when the request has header
`X-Requested-With: XMLHttpRequest`, otherwise they redirect with a flash message.
All POST forms need `{% csrf_token %}` (for fetch, send the `X-CSRFToken` header).

## Template context (for the frontend teammate)
Every template: `nav_categories`, `cart_count`, `messages`.
- `home.html`: `best_sellers`, `new_arrivals`, `audiobooks`, `categories`, `subscribe_form`
- `book_list.html`: `books`, `page_obj`, `category`, `q`, `section`, `sort`
- `book_detail.html`: `book`, `related_books`
- `cart.html`: `cart`, `items` (each: `.book`, `.quantity`, `.subtotal`), `total`
- `checkout.html`: `form`, `items`, `total`
- `order_success.html`: `order` (`order.items.all`)

Templates in `store/templates/store/` are plain placeholders – replace freely.
Put static files in a top-level `static/` folder.

## Database teammate
Models are in `store/models.py` (Category, Book, Subscriber, Cart, CartItem, Order, OrderItem).
After changing models: `python manage.py makemigrations && python manage.py migrate`.

## AI teammate
Only edit `store/services/ai.py`. Keep `get_book_summary(title, author='') -> str`
and raise `AIServiceError` on failure. Summaries are cached in `Book.ai_summary`.
Set `GEMINI_MODEL` if the default model name has been retired.
