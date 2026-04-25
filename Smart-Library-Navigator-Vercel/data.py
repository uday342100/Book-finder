"""Book data module for Smart Library Navigator."""

from __future__ import annotations

from typing import Dict, Optional

from map import LIBRARY_GRID


FILTER_SCHEMA = {
    "Engineering Books": [
        "Artificial Intelligence (AI)",
        "Computer Engineering",
        "Mechanical Engineering",
        "Civil Engineering",
        "Robotics",
    ],
    "Story Books": ["Fiction", "Mystery", "Fantasy", "Adventure"],
    "Medical": ["Anatomy", "Pharmacology", "Physiology"],
    "Computer Science": ["Algorithms", "Programming", "Data Science", "Cybersecurity"],
    "Self Help": ["Productivity", "Mindset"],
    "Competitive Exams": ["JEE", "NEET", "UPSC"],
    "Science": ["Physics", "Chemistry", "Biology"],
    "History": ["World History", "Ancient History", "Modern History"],
}


BOOK_CATALOG = {
    "Engineering Books": {
        "Artificial Intelligence (AI)": [
            "Applied AI Blueprint",
            "Neural Models Simplified",
            "Machine Vision in Practice",
            "Probabilistic Learning Paths",
            "Intelligent Systems Studio",
            "AI Engineering Handbook",
        ],
        "Computer Engineering": [
            "Digital Logic Workshop",
            "Microprocessor Design Track",
            "Embedded Systems Core",
            "Parallel Architecture Notes",
            "Computer Hardware Deep Dive",
            "VLSI Basics for Engineers",
        ],
        "Mechanical Engineering": [
            "Thermodynamics Concepts",
            "Strength of Materials",
            "Heat Transfer Roadmap",
            "Design of Machine Elements",
            "Industrial Manufacturing Guide",
            "Fluid Mechanics Lab Notes",
        ],
        "Civil Engineering": [
            "Concrete Technology Manual",
            "Structural Analysis Primer",
            "Soil Mechanics Illustrated",
            "Surveying Essentials",
            "Highway Engineering Methods",
            "Construction Planning Toolkit",
        ],
        "Robotics": [
            "Robotic Motion Planning",
            "Sensors and Actuators Lab",
            "Autonomous Robots Fieldbook",
            "Kinematics for Robotics",
            "Robot Control Systems",
            "Service Robotics Projects",
        ],
    },
    "Story Books": {
        "Fiction": [
            "Whispers of Rain",
            "Last Train to Orion",
            "Echoes of the Valley",
            "Paper Boat Summer",
            "Moonlight Letters",
            "The Quiet Horizon",
        ],
        "Mystery": [
            "The Locked Observatory",
            "Night at Raven House",
            "Murder on Birch Street",
            "The Vanishing Ledger",
            "Cipher in the Library",
            "Case of the Hollow Bell",
        ],
        "Fantasy": [
            "Crown of Ember",
            "Dragon Song Chronicle",
            "Forest of Silver Keys",
            "Mage of the North Gate",
            "The Last Sky Kingdom",
            "Runes of Dawn",
        ],
        "Adventure": [
            "Island Beyond Maps",
            "Journey to Copper Cliffs",
            "Trail of the Blue Falcon",
            "Voyage Across Red Sea",
            "Tunnel of Lost Suns",
            "Expedition Zero",
        ],
    },
    "Medical": {
        "Anatomy": [
            "Human Anatomy Atlas",
            "Musculoskeletal Anatomy",
            "Neuroanatomy Essentials",
            "Clinical Anatomy Cases",
            "Atlas of Organ Systems",
            "Anatomy Revision Cards",
        ],
        "Pharmacology": [
            "Drug Mechanisms Simplified",
            "Clinical Pharmacology Primer",
            "Pharma Calculations Handbook",
            "Essential Medicines Guide",
            "Pharmacology in Practice",
            "Therapeutics Quick Notes",
        ],
        "Physiology": [
            "Cardiovascular Physiology",
            "Respiratory Physiology",
            "Renal Physiology Basics",
            "Endocrine System Concepts",
            "Cell Physiology Toolkit",
            "Integrated Physiology Review",
        ],
    },
    "Computer Science": {
        "Algorithms": [
            "Algorithmic Thinking",
            "Greedy to Dynamic Programming",
            "Graph Algorithms in Action",
            "Sorting and Searching Lab",
            "Complexity and Computation",
            "Interview Algorithms 101",
        ],
        "Programming": [
            "Python Patterns",
            "Clean Programming Practice",
            "Object Oriented Craft",
            "Practical Software Design",
            "Code Refactoring Journey",
            "Programming Fundamentals Plus",
        ],
        "Data Science": [
            "Data Science Workflow",
            "Statistics for Insights",
            "Feature Engineering Tactics",
            "Model Evaluation Handbook",
            "Data Visualization Recipes",
            "Real World Data Projects",
        ],
        "Cybersecurity": [
            "Network Security Basics",
            "Ethical Hacking Essentials",
            "Web Security Lab Manual",
            "Cryptography Foundations",
            "SOC Analyst Playbook",
            "Cloud Security Essentials",
        ],
    },
    "Self Help": {
        "Productivity": [
            "Focus by Design",
            "Atomic Workflows",
            "Deep Work Planner",
            "Seven Hours Better",
            "Goal Systems Blueprint",
            "Personal Output Engine",
        ],
        "Mindset": [
            "Growth Mindset Journal",
            "Resilience Daily",
            "Confidence with Clarity",
            "Habits for Calm Living",
            "Self Leadership Notes",
            "Mind over Distraction",
        ],
    },
    "Competitive Exams": {
        "JEE": [
            "JEE Physics Master Set",
            "JEE Chemistry Drillbook",
            "JEE Math Precision",
            "JEE Mock Tests Pro",
            "JEE Formula Revision",
            "JEE Rank Booster",
        ],
        "NEET": [
            "NEET Biology Max",
            "NEET Chemistry Concepts",
            "NEET Physics Solved",
            "NEET Practice Capsule",
            "NEET Fast Revision",
            "NEET Test Marathon",
        ],
        "UPSC": [
            "UPSC Polity Notes",
            "UPSC Economy Explorer",
            "UPSC History Matrix",
            "UPSC Geography Drill",
            "UPSC Ethics Handbook",
            "UPSC Essay Framework",
        ],
    },
    "Science": {
        "Physics": [
            "Modern Physics Intro",
            "Quantum Ideas Simplified",
            "Electromagnetics Core",
            "Classical Mechanics Primer",
            "Optics and Waves",
            "Physics Problem Vault",
        ],
        "Chemistry": [
            "Organic Chemistry Path",
            "Inorganic Chemistry Snapshot",
            "Physical Chemistry Practice",
            "Reaction Mechanisms",
            "Analytical Chemistry Basics",
            "Chemistry Lab Companion",
        ],
        "Biology": [
            "Cell Biology Handbook",
            "Genetics Fundamentals",
            "Microbiology Concepts",
            "Ecology and Environment",
            "Evolutionary Biology Notes",
            "Biology Practical Workbook",
        ],
    },
    "History": {
        "World History": [
            "World Civilizations Timeline",
            "Empires Through Ages",
            "Global Wars Explained",
            "Trade Routes and Cultures",
            "Nations and Revolutions",
            "History of Modern World",
        ],
        "Ancient History": [
            "Ancient India Compendium",
            "Greece and Rome Survey",
            "Egyptian Civilization",
            "Mesopotamia and Beyond",
            "Ancient Trade Networks",
            "Myths and Monarchies",
        ],
        "Modern History": [
            "Industrial Age Story",
            "Freedom Movements Archive",
            "Twentieth Century Turning Points",
            "Constitutional Histories",
            "Colonial to Contemporary",
            "Modern India Chronicle",
        ],
    },
}


def _walkable_cells() -> list[tuple[int, int]]:
    """Collect walkable coordinates from the library grid."""
    cells: list[tuple[int, int]] = []
    for row_idx, row in enumerate(LIBRARY_GRID):
        for col_idx, value in enumerate(row):
            if value == 0:
                cells.append((row_idx, col_idx))
    return cells


def _build_books() -> list[dict]:
    """Generate a large demo dataset (100+ books)."""
    walkable = _walkable_cells()
    books: list[dict] = []
    blocks = ["A", "B", "C", "D"]

    idx = 0
    for category, subcategories in BOOK_CATALOG.items():
        for subcategory, titles in subcategories.items():
            for title in titles:
                coord = walkable[idx % len(walkable)]
                books.append(
                    {
                        "title": title,
                        "author": f"Author {idx + 1}",
                        "category": category,
                        "subcategory": subcategory,
                        "floor": (idx % 3) + 1,
                        "block": blocks[idx % len(blocks)],
                        "rack": f"R{idx + 1:03d}",
                        "container": f"Container-{(idx % 20) + 1:02d}",
                        "coord": coord,
                    }
                )
                idx += 1

    return books


BOOKS_DB = _build_books()


def get_books() -> list[dict]:
    """Return the full demo books list."""
    return BOOKS_DB


def get_filter_schema() -> dict[str, list[str]]:
    """Return available category and subcategory filters."""
    return FILTER_SCHEMA


def find_book_by_title(query: str, books: Optional[list[dict]] = None) -> Optional[Dict]:
    """Find a book by title using exact match first, then partial match."""
    search_space = books if books is not None else BOOKS_DB
    normalized_query = query.strip().lower()
    if not normalized_query:
        return None

    exact_match = next(
        (book for book in search_space if book["title"].lower() == normalized_query),
        None,
    )
    if exact_match:
        return exact_match

    partial_match = next(
        (book for book in search_space if normalized_query in book["title"].lower()),
        None,
    )
    return partial_match
