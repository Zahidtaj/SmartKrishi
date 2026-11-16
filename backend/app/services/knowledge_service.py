import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from backend.app.core.config import settings

class KnowledgeService:
    def __init__(self):
        self._load_articles()
        self._load_soil_reference()
        self._load_data_sources()

    def _load_articles(self):
        file_path = settings.DATA_PATH / "knowledge_articles.json"
        self.articles: List[Dict[str, Any]] = []
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                self.articles = json.load(f)

    def _load_soil_reference(self):
        file_path = settings.DATA_PATH / "soil_characteristics.json"
        self.soil_reference: Dict[str, Any] = {}
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                self.soil_reference = json.load(f)

    def _load_data_sources(self):
        file_path = settings.DATA_PATH / "data_sources.json"
        self.data_sources: List[Dict[str, Any]] = []
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                self.data_sources = json.load(f)

    def get_all_articles(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        if category:
            cat_clean = category.strip().lower()
            return [a for a in self.articles if a.get("category", "").strip().lower() == cat_clean]
        return self.articles

    def get_article_by_id(self, article_id: int) -> Optional[Dict[str, Any]]:
        for a in self.articles:
            if a["id"] == article_id:
                return a
        return None

    def get_soil_reference(self) -> Dict[str, Any]:
        return self.soil_reference

    def get_all_data_sources(self) -> List[Dict[str, Any]]:
        return self.data_sources

knowledge_service = KnowledgeService()
