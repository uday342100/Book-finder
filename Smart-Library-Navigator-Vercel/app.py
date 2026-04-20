"""Streamlit app for Smart Library Navigator."""

from __future__ import annotations

import copy
from urllib.parse import quote_plus

import matplotlib.pyplot as plt
import numpy as np
import requests
import streamlit as st

from algorithms import run_algorithm
from data import find_book_by_title, get_books, get_filter_schema
from map import ENTRANCE, LIBRARY_GRID, is_walkable


def build_visual_grid(
    grid: list[list[int]],
    path: list[tuple[int, int]],
    start: tuple[int, int],
    goal: tuple[int, int],
) -> np.ndarray:
    """
    Build numeric matrix for visualization.

    Legend:
    - 0: walkable
    - 1: obstacle
    - 2: path
    - 3: entrance
    - 4: goal
    """
    vis = copy.deepcopy(grid)
    for r, c in path:
        if (r, c) not in {start, goal}:
            vis[r][c] = 2

    sr, sc = start
    gr, gc = goal
    vis[sr][sc] = 3
    vis[gr][gc] = 4
    return np.array(vis)


def plot_path_grid(
    grid: list[list[int]],
    path: list[tuple[int, int]],
    start: tuple[int, int],
    goal: tuple[int, int],
) -> plt.Figure:
    """Plot library grid with path, start and goal."""
    matrix = build_visual_grid(grid, path, start, goal)
    fig, ax = plt.subplots(figsize=(8, 8))

    cmap = plt.matplotlib.colors.ListedColormap(
        ["#101418", "#2f3640", "#4aa3ff", "#22c55e", "#ff6b6b"]
    )
    ax.imshow(matrix, cmap=cmap, interpolation="nearest")

    ax.set_title("Clear Path Visualization", fontsize=13, pad=10, color="#e8edf3")
    ax.set_xticks(range(matrix.shape[1]))
    ax.set_yticks(range(matrix.shape[0]))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.grid(color="#4b5563", linestyle="-", linewidth=0.3)
    ax.set_facecolor("#0b0f14")
    fig.patch.set_facecolor("#0b0f14")

    # Add legend markers.
    handles = [
        plt.Line2D([0], [0], marker="s", color="w", markerfacecolor="#101418", markersize=10, label="Walkable"),
        plt.Line2D([0], [0], marker="s", color="w", markerfacecolor="#2f3640", markersize=10, label="Obstacle"),
        plt.Line2D([0], [0], marker="s", color="w", markerfacecolor="#4aa3ff", markersize=10, label="Path"),
        plt.Line2D([0], [0], marker="s", color="w", markerfacecolor="#22c55e", markersize=10, label="Start"),
        plt.Line2D([0], [0], marker="s", color="w", markerfacecolor="#ff6b6b", markersize=10, label="Book"),
    ]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.05), ncol=3, frameon=False)

    for step_index, (row, col) in enumerate(path):
        if (row, col) not in {start, goal} and step_index % 2 == 0:
            ax.text(col, row, str(step_index), ha="center", va="center", fontsize=7, color="#dbeafe")

    plt.tight_layout()
    return fig


def main() -> None:
    """Run Streamlit UI."""
    st.set_page_config(page_title="Smart Library Navigator", page_icon="📚", layout="wide")

    st.markdown(
        """
        <style>
            .stApp {
                background-color: #000000;
                color: #e8edf3;
            }
            div[data-testid="stSidebar"] {
                background-color: #0b0f14;
                border-right: 1px solid #1f2937;
            }
            p, label, span, li, div, h1, h2, h3, h4 {
                color: #e8edf3;
            }
            .topbar {
                background: #111827;
                color: #e8edf3;
                padding: 8px 12px;
                border-radius: 8px;
                margin-bottom: 12px;
                font-size: 0.9rem;
                border: 1px solid #1f2937;
            }
            .card {
                background: #0f172a;
                border: 1px solid #1e293b;
                border-radius: 10px;
                padding: 8px;
                margin-bottom: 8px;
            }
            .card-title {
                font-size: 0.86rem;
                font-weight: 700;
                color: #f8fafc;
                margin-bottom: 4px;
                min-height: 34px;
            }
            .card-meta {
                font-size: 0.72rem;
                color: #cbd5e1;
                margin-bottom: 4px;
            }
            .section-title {
                font-size: 1.4rem;
                font-weight: 600;
                color: #f8fafc;
                margin-bottom: 0.2rem;
            }
            .stButton > button {
                background-color: #2563eb;
                color: #ffffff;
                border: 1px solid #1d4ed8;
                font-weight: 600;
            }
            .stButton > button:hover {
                background-color: #1d4ed8;
                color: #ffffff;
                border-color: #1e40af;
            }
            div[data-testid="stSidebar"] .stMarkdown,
            div[data-testid="stSidebar"] label {
                color: #e8edf3 !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    start_node = ENTRANCE
    books = get_books()
    filter_schema = get_filter_schema()

    st.markdown('<div class="topbar">Smart Library Navigator Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Search Books</div>', unsafe_allow_html=True)

    @st.cache_data(show_spinner=False)
    def get_cover_url(title: str) -> str:
        """
        Resolve a cover image by book title from Open Library.

        If no real cover is found, generate a clean title poster so every
        book always has an image.
        """
        try:
            response = requests.get(
                "https://openlibrary.org/search.json",
                params={"title": title, "limit": 1},
                timeout=4,
            )
            if response.ok:
                docs = response.json().get("docs", [])
                if docs:
                    cover_id = docs[0].get("cover_i")
                    if cover_id:
                        return f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
        except requests.RequestException:
            pass

        poster_text = quote_plus(title[:40].replace(" ", "\n"))
        return f"https://placehold.co/200x300/0f172a/e2e8f0?text={poster_text}"

    # Left sidebar filters panel.
    st.sidebar.markdown("## Filters Panel")
    selected_categories = st.sidebar.multiselect(
        "Categories",
        options=list(filter_schema.keys()),
        default=list(filter_schema.keys()),
    )

    available_subcategories: list[str] = []
    for category in selected_categories:
        available_subcategories.extend(filter_schema[category])

    selected_subcategories = st.sidebar.multiselect(
        "Subcategories",
        options=sorted(set(available_subcategories)),
        default=sorted(set(available_subcategories)),
    )

    algorithm = st.sidebar.selectbox("Algorithm", options=["A*", "BFS", "DFS"], index=0)

    filtered_books = [
        book
        for book in books
        if book["category"] in selected_categories and book["subcategory"] in selected_subcategories
    ]

    st.sidebar.metric("Total Books", len(books))
    st.sidebar.metric("Filtered Books", len(filtered_books))
    st.sidebar.metric("Selected Algorithm", algorithm)

    if "query_text" not in st.session_state:
        st.session_state.query_text = ""
    if "pending_query_text" in st.session_state:
        st.session_state.query_text = st.session_state.pending_query_text
        del st.session_state["pending_query_text"]

    st.markdown('<div class="card">', unsafe_allow_html=True)
    query = st.text_input(
        "Book Search",
        placeholder="Search by book title",
        key="query_text",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("### Suggested Books")
    if filtered_books:
        suggestion_cols = st.columns(5, gap="small")
        for idx, suggested in enumerate(filtered_books[:15]):
            cover_url = get_cover_url(suggested["title"])
            with suggestion_cols[idx % 5]:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.image(
                    cover_url,
                    use_container_width=True,
                )
                st.markdown(
                    f'<div class="card-title">{suggested["title"]}</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    (
                        '<div class="card-meta">'
                        f'{suggested["category"]} • {suggested["subcategory"]}<br/>'
                        f'Rack: {suggested["rack"]} • Container: {suggested["container"]}'
                        "</div>"
                    ),
                    unsafe_allow_html=True,
                )
                if st.button("Show Path", key=f"show_path_{idx}", width="stretch"):
                    st.session_state.pending_query_text = suggested["title"]
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("No books found for current filters.")

    if not query.strip():
        st.info("Search a book name to see availability, location, and algorithm path.")
        return

    book = find_book_by_title(query, filtered_books if filtered_books else books)
    if not book:
        st.error("Book not found in the selected filters. Try another title or adjust filters.")
        return

    goal = tuple(book["coord"])
    if not is_walkable(goal, LIBRARY_GRID):
        st.error("Book location is blocked on map. Update the data.")
        return

    path = run_algorithm(algorithm, LIBRARY_GRID, start_node, goal)
    path_length = len(path) - 1 if path else 0
    st.sidebar.metric("Path Length", path_length if path else "No Path")

    st.markdown("---")
    st.subheader("Search Output")
    st.success("Book is available in the library.")

    details_col1, details_col2, details_col3 = st.columns(3)
    details_col1.metric("Book Name", book["title"])
    details_col2.metric("Rack", book["rack"])
    details_col3.metric("Container", book["container"])

    details_col4, details_col5, details_col6 = st.columns(3)
    details_col4.metric("Floor", book["floor"])
    details_col5.metric("Block", book["block"])
    details_col6.metric("Coordinates", str(goal))

    if not path:
        st.warning("No valid path found by selected algorithm.")
        return

    st.markdown("### Pathfinding Result")
    st.write(f"Algorithm: **{algorithm}**")
    st.write(f"Path Length: **{path_length} steps**")
    st.code(" -> ".join([str(step) for step in path]), language="text")

    fig = plot_path_grid(LIBRARY_GRID, path, start_node, goal)
    st.pyplot(fig, width="stretch")


if __name__ == "__main__":
    main()
