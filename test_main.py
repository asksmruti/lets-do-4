import json
from fastapi.testclient import TestClient
from main import app, survey_template

client = TestClient(app)

def test_get_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "API is up and running"}

def test_get_survey():
    response = client.get("/survey")
    assert response.status_code == 200
    assert response.json() == json.loads(json.dumps(survey_template))

# def test_add_section():
#     new_section = {
#         "section": "New Section",
#         "questions": []
#     }
#     response = client.post("/add-section", json=new_section)
#     assert response.status_code == 201
#     assert response.json() == {"message": "Section added successfully"}

def test_update_section():
    section_name = "Existing Section"
    updated_section = {
        "section": section_name,
        "questions": []
    }
    response = client.put(f"/update-section/{section_name}", json=updated_section)
    assert response.status_code == 200
    assert response.json() == {"message": "Section updated successfully"}

def test_delete_section():
    section_name = "Section to Delete"
    response = client.delete(f"/delete-section/{section_name}")
    assert response.status_code == 200
    assert response.json() == {"message": "Section deleted successfully"}

def test_delete_question():
    section_name = "Existing Section"
    question_idx = 0
    response = client.delete(f"/delete-question/{section_name}/{question_idx}")
    assert response.status_code == 200
    assert response.json() == {"message": "Question deleted successfully"}

def test_add_question():
    section_name = "Existing Section"
    new_question = {
        "question": "New Question",
        "options": []
    }
    response = client.post(f"/add-question/{section_name}", json=new_question)
    assert response.status_code == 201
    assert response.json() == {"message": "Question added successfully"}

def test_update_question():
    section_name = "Existing Section"
    question_idx = 0
    updated_question = {
        "question": "Updated Question",
        "options": []
    }
    response = client.put(f"/update-question/{section_name}/{question_idx}", json=updated_question)
    assert response.status_code == 200
    assert response.json() == {"message": "Question updated successfully"}

def test_get_question():
    section_name = "Needs"
    question_idx = 0
    response = client.get(f"/get-question/{section_name}/{question_idx}")
    assert response.status_code == 200
    assert response.json() == survey_template["survey"][0]["questions"][0]

def test_get_section():
    section_name = "Needs"
    response = client.get(f"/get-section/{section_name}")
    assert response.status_code == 200
    assert response.json() == survey_template["survey"][0]

def test_get_sections():
    response = client.get("/get-sections")
    assert response.status_code == 200
    assert response.json() == survey_template["survey"]