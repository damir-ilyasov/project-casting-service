from models import Candidate
from models.candidates import add_candidate, find_candidate


def test_candidate_creation():
    candidate = Candidate(1, "Иван Иванов", "ivan@example.com")
    assert candidate.id == 1
    assert candidate.name == "Иван Иванов"
    assert candidate.contact == "ivan@example.com"


def test_candidate_from_data():
    data = {"id": 1, "name": "Иван Иванов", "contact": "ivan@example.com"}
    candidate = Candidate.from_data(data)
    assert candidate.id == 1
    assert candidate.name == "Иван Иванов"


def test_add_candidate():
    candidates = []
    candidate = add_candidate(candidates, "Иван Иванов", "ivan@example.com")
    assert len(candidates) == 1
    assert candidate.name == "Иван Иванов"


def test_find_candidate():
    candidates = []
    add_candidate(candidates, "Иван Иванов", "ivan@example.com")
    assert find_candidate(candidates, "иван")
    assert find_candidate(candidates, "петр") == []
