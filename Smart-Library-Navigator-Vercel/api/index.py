"""Vercel Python entrypoint for Smart Library Navigator."""

from __future__ import annotations

from urllib.parse import quote_plus

import requests
from flask import Flask, request

from algorithms import run_algorithm
from data import find_book_by_title, get_books, get_filter_schema
from map import ENTRANCE, LIBRARY_GRID, is_walkable

app = Flask(__name__)


def cover_for_title(title: str) -> str:
    """Get real cover if possible, else title poster."""
    try:
        response = requests.get(
            "https://openlibrary.org/search.json",
            params={"title": title, "limit": 1},
            timeout=3,
        )
        if response.ok:
            docs = response.json().get("docs", [])
            if docs and docs[0].get("cover_i"):
                return f"https://covers.openlibrary.org/b/id/{docs[0]['cover_i']}-M.jpg"
    except requests.RequestException:
        pass
    return f"https://placehold.co/180x260/0f172a/e2e8f0?text={quote_plus(title[:25])}"


def layout(body_html: str) -> str:
    """Shared UI shell."""
    return f"""
    <!doctype html>
    <html>
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>Smart Library Navigator</title>
      <style>
        body {{ font-family: Inter, Arial, sans-serif; background:#000; color:#e8edf3; margin:0; }}
        .wrap {{ max-width:1200px; margin:0 auto; padding:16px; }}
        .top {{ background:#111827; border:1px solid #1f2937; border-radius:10px; padding:10px 12px; margin-bottom:16px; }}
        .grid {{ display:grid; grid-template-columns:280px 1fr; gap:14px; }}
        .panel {{ background:#0f172a; border:1px solid #1e293b; border-radius:10px; padding:12px; }}
        .small {{ color:#a9b5c8; font-size:12px; }}
        .cards {{ display:grid; grid-template-columns:repeat(5, minmax(0,1fr)); gap:10px; }}
        .card {{ background:#0f172a; border:1px solid #1e293b; border-radius:10px; padding:8px; }}
        .card img {{ width:100%; border-radius:8px; }}
        .title {{ font-weight:700; font-size:13px; margin:6px 0; min-height:34px; }}
        .meta {{ color:#b7c3d6; font-size:11px; min-height:32px; }}
        input, select {{ width:100%; background:#020617; color:#e8edf3; border:1px solid #334155; border-radius:6px; padding:8px; margin:4px 0 8px; }}
        button {{ width:100%; background:#2563eb; color:white; border:1px solid #1d4ed8; border-radius:8px; padding:8px; font-weight:600; cursor:pointer; }}
        .result {{ margin-top:14px; padding:12px; border-radius:10px; border:1px solid #1e293b; background:#0b1220; }}
        .path {{ background:#020617; border:1px solid #1e293b; border-radius:8px; padding:8px; color:#93c5fd; overflow:auto; }}
      </style>
    </head>
    <body>
      <div class="wrap">
        <div class="top">Smart Library Navigator - Vercel Deployment</div>
        {body_html}
      </div>
    </body>
    </html>
    """


@app.route("/", methods=["GET"])
def home() -> str:
    """Render main page with filters, suggestions, and path result."""
    books = get_books()
    schema = get_filter_schema()

    algorithm = request.args.get("algorithm", "A*")
    query = request.args.get("q", "").strip()
    category = request.args.get("category", "")
    subcategory = request.args.get("subcategory", "")

    categories = list(schema.keys())
    selected_categories = [category] if category in categories else categories
    sub_pool: list[str] = []
    for cat in selected_categories:
        sub_pool.extend(schema[cat])
    selected_subcategories = [subcategory] if subcategory in sub_pool else sub_pool

    filtered_books = [
        b
        for b in books
        if b["category"] in selected_categories and b["subcategory"] in selected_subcategories
    ]

    filter_options = "".join(
        [
            f'<option value="{c}" {"selected" if c == category else ""}>{c}</option>'
            for c in categories
        ]
    )
    sub_options = "".join(
        [
            f'<option value="{s}" {"selected" if s == subcategory else ""}>{s}</option>'
            for s in sorted(set(sub_pool))
        ]
    )
    algo_options = "".join(
        [
            f'<option value="{a}" {"selected" if a == algorithm else ""}>{a}</option>'
            for a in ["A*", "BFS", "DFS"]
        ]
    )

    cards = []
    for b in filtered_books[:15]:
        cards.append(
            f"""
            <div class="card">
              <img src="{cover_for_title(b['title'])}" alt="{b['title']}" />
              <div class="title">{b['title']}</div>
              <div class="meta">{b['category']} - {b['subcategory']}</div>
              <a href="/?q={quote_plus(b['title'])}&algorithm={quote_plus(algorithm)}&category={quote_plus(category)}&subcategory={quote_plus(subcategory)}"><button>Show Path</button></a>
            </div>
            """
        )

    result_html = ""
    if query:
        book = find_book_by_title(query, filtered_books if filtered_books else books)
        if book and is_walkable(tuple(book["coord"]), LIBRARY_GRID):
            path = run_algorithm(algorithm, LIBRARY_GRID, ENTRANCE, tuple(book["coord"]))
            path_len = max(len(path) - 1, 0)
            result_html = f"""
            <div class="result">
              <h3>Search Output</h3>
              <p><b>Book:</b> {book['title']} | <b>Rack:</b> {book['rack']} | <b>Container:</b> {book.get('container', '-')}</p>
              <p><b>Floor:</b> {book['floor']} | <b>Block:</b> {book['block']} | <b>Algorithm:</b> {algorithm} | <b>Path Length:</b> {path_len}</p>
              <div class="path">{' -> '.join(map(str, path)) if path else 'No path found'}</div>
            </div>
            """
        else:
            result_html = '<div class="result">Book not found in current filter selection.</div>'

    body = f"""
    <div class="grid">
      <div class="panel">
        <h3>Filters</h3>
        <form method="get" action="/">
          <label>Category</label>
          <select name="category"><option value="">All</option>{filter_options}</select>
          <label>Subcategory</label>
          <select name="subcategory"><option value="">All</option>{sub_options}</select>
          <label>Algorithm</label>
          <select name="algorithm">{algo_options}</select>
          <label>Search Book</label>
          <input name="q" value="{query}" placeholder="Enter title" />
          <button type="submit">Search</button>
        </form>
        <p class="small">Total books: {len(books)}<br/>Filtered: {len(filtered_books)}</p>
      </div>
      <div>
        <h3>Suggested Books</h3>
        <div class="cards">
          {''.join(cards) if cards else '<p>No books found for selected filters.</p>'}
        </div>
        {result_html}
      </div>
    </div>
    """
    return layout(body)

