import json
import os
from typing import List, Dict, Any

FILE_NAME = "tarefas.json"
FILE_PATH = os.path.join(os.path.dirname(__file__), FILE_NAME)


def carregar_tarefas() -> List[Dict[str, Any]]:
    if not os.path.exists(FILE_PATH):
        return []
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except Exception:
        return []


def salvar_tarefas(tarefas: List[Dict[str, Any]]) -> None:
    try:
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(tarefas, f, ensure_ascii=False, indent=2)
    except Exception as e:
        raise IOError(f"Não foi possível salvar tarefas: {e}")
