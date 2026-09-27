"""Пакет моделей предметной области: Project, Role, Candidate, Application."""

from .applications import Application
from .candidates import Candidate
from .projects import Project, Role

__all__ = ["Project", "Role", "Candidate", "Application"]
