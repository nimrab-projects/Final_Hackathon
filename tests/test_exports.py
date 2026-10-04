import json
from services.export_service import ExportService
from services.llm_service import LLMService
from models.schemas import FinalSpecification

def test_json_export():
    mock_spec = LLMService.generate_mock("test prompt", FinalSpecification)
    json_str = ExportService.to_json(mock_spec)
    
    parsed = json.loads(json_str)
    assert "project_title" in parsed
    assert "product_analysis" in parsed
    assert "solution_design" in parsed
    assert "technical_specification" in parsed

def test_markdown_export():
    mock_spec = LLMService.generate_mock("test prompt", FinalSpecification)
    md_str = ExportService.to_markdown(mock_spec)
    
    assert "# 🚀" in md_str
    assert "## 📋 Executive Summary" in md_str
    assert "## 💡 1. Product & Problem Analysis" in md_str
    assert "## 🎨 2. Solution & Product Design" in md_str
    assert "## 🛠️ 3. Technical Architecture & Requirements" in md_str
    assert "## 🔍 4. Critical Audit & Review Findings" in md_str
    assert "Must Have" in md_str or "FR-01" in md_str
