import logging
from fastapi import FastAPI, HTTPException, status
from model import Survey, SectionUpdate, QuestionCreate
import json
from threading import Lock
from copy import deepcopy


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# File path
survey_template_path = 'survey_template.json'

# Thread lock for synchronized access to file
file_lock = Lock()

# In-memory store for survey data
survey_template = None

def load_survey_template():
    """
    Load the survey template from the JSON file.

    Returns:
        dict: The loaded survey template.
    
    Raises:
        Exception: If an error occurs while loading the survey template.
    """
    try:
        with open(survey_template_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        logger.exception(f"An error occurred while loading survey template: {e}")
        raise

def save_survey_template(data):
    """
    Save the survey template to the JSON file.

    Args:
        data (dict): The survey template to be saved.
    
    Raises:
        Exception: If an error occurs while saving the survey template.
    """
    with file_lock:
        try:
            with open(survey_template_path, 'w') as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            logger.exception(f"An error occurred while saving survey template: {e}")
            raise

# Initialize in-memory store
try:
    survey_template = load_survey_template()
except Exception as e:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to load initial survey template.")


# Initialize FastAPI
app = FastAPI(
    title="Survey Template Management API",
    description="API to manage survey questions .",
    version="1.0.0"
)


@app.get("/", tags=["Root"], summary="Check API status")
def read_root():
    """
    Check the status of the API.

    Returns:
        dict: A JSON response indicating that the API is up and running.
    """
    return {"status": "API is up and running"}  # Return a simple JSON response

@app.get("/survey", response_model=Survey, tags=["Survey"], summary="Get survey questions")
def get_survey():
    """
    Get the survey questions.

    Returns:
        dict: A deep copy of the survey template.
    """
    return deepcopy(survey_template)

@app.post("/add-section", status_code=status.HTTP_201_CREATED)
def add_section(new_section: SectionUpdate):
    """
    Add a new section to the survey template.

    Args:
        new_section (SectionUpdate): The new section to be added.
    
    Returns:
        dict: A message indicating that the section was added successfully.
    
    Raises:
        HTTPException: If an error occurs while adding the new section.
    """
    try:
        survey_template['survey'].append(new_section.model_dump())
        save_survey_template(survey_template)
        return {"message": "Section added successfully"}
    except Exception as e:
        logger.exception("Failed to add new section.")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.put("/update-section/{section_name}", status_code=status.HTTP_200_OK)
def update_section(section_name: str, section_data: SectionUpdate):
    """
    Update a section in the survey template.

    Args:
        section_name (str): The name of the section to be updated.
        section_data (SectionUpdate): The updated section data.
    
    Returns:
        dict: A message indicating that the section was updated successfully.
    
    Raises:
        HTTPException: If an error occurs while updating the section.
    """
    try:
        updated = False
        for i, section in enumerate(survey_template['survey']):
            if section['section'] == section_name:
                survey_template['survey'][i] = section_data.model_dump()
                updated = True
                break
        
        if not updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Section not found")
        
        # Save the updated survey template
        save_survey_template(survey_template)
        return {"message": "Section updated successfully"}
    
    except Exception as e:
        logger.exception("Failed to update section.")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))   

@app.delete("/delete-section/{section_name}", status_code=status.HTTP_200_OK)
def delete_section(section_name: str):
    """
    Delete a section from the survey template.

    Args:
        section_name (str): The name of the section to be deleted.
    
    Returns:
        dict: A message indicating that the section was deleted successfully.
    
    Raises:
        HTTPException: If an error occurs while deleting the section.
    """
    try:
        survey_template['survey'] = [section for section in survey_template['survey'] if section['section'] != section_name]
        save_survey_template(survey_template)
        return {"message": "Section deleted successfully"}
    except Exception as e:
        logger.exception("Failed to delete section.")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.delete("/delete-question/{section_name}/{question_idx}", status_code=status.HTTP_200_OK)
def delete_question(section_name: str, question_idx: int):
    """
    Delete a question from a section in the survey template.

    Args:
        section_name (str): The name of the section containing the question.
        question_idx (int): The index of the question to be deleted.
    
    Returns:
        dict: A message indicating that the question was deleted successfully.
    
    Raises:
        HTTPException: If an error occurs while deleting the question.
    """
    # Find the section containing the question
    section_to_update = next((section for section in survey_template['survey'] if section['section'] == section_name), None)

    # Check if the section exists
    if not section_to_update:
        logger.error("Section not found")
        raise HTTPException(status_code=404, detail="Section not found")

    # Check if the question index is valid
    if question_idx < 0 or question_idx >= len(section_to_update['questions']):
        logger.error("Question index out of range")
        raise HTTPException(status_code=404, detail="Question index out of range")

    # Delete the question
    try:
        del section_to_update['questions'][question_idx]
        save_survey_template(survey_template)
        return {"message": "Question deleted successfully"}
    except Exception as e:
        logger.exception("Failed to delete question")
        raise HTTPException(status_code=500, detail="Failed to delete question")

@app.post("/add-question/{section_name}", status_code=status.HTTP_201_CREATED)
def add_question(section_name: str, new_question: QuestionCreate):
    """
    Add a new question to a section in the survey template.

    Args:
        section_name (str): The name of the section to add the question to.
        new_question (QuestionCreate): The new question to be added.
    
    Returns:
        dict: A message indicating that the question was added successfully.
    
    Raises:
        HTTPException: If an error occurs while adding the question.
    """
    try:
        # Find the section containing the question
        section_to_update = next((section for section in survey_template['survey'] if section['section'] == section_name), None)

        # Check if the section exists
        if not section_to_update:
            logger.error("Section not found")
            raise HTTPException(status_code=404, detail="Section not found")

        # Add the new question
        section_to_update['questions'].append(new_question.dict())

        # Save the updated survey template
        save_survey_template(survey_template)
        return {"message": "Question added successfully"}
    except Exception as e:
        logger.exception("Failed to add question")
        raise HTTPException(status_code=500, detail="Failed to add question")
    
@app.put("/update-question/{section_name}/{question_idx}", status_code=status.HTTP_200_OK)
def update_question(section_name: str, question_idx: int, updated_question: QuestionCreate):
    """
    Update a question in a section of the survey template.

    Args:
        section_name (str): The name of the section containing the question.
        question_idx (int): The index of the question to be updated.
        updated_question (QuestionCreate): The updated question data.
    
    Returns:
        dict: A message indicating that the question was updated successfully.
    
    Raises:
        HTTPException: If an error occurs while updating the question.
    """
    try:
        # Find the section containing the question
        section_to_update = next((section for section in survey_template['survey'] if section['section'] == section_name), None)

        # Check if the section exists
        if not section_to_update:
            logger.error("Section not found")
            raise HTTPException(status_code=404, detail="Section not found")

        # Check if the question index is valid
        if question_idx < 0 or question_idx >= len(section_to_update['questions']):
            logger.error("Question index out of range")
            raise HTTPException(status_code=404, detail="Question index out of range")

        # Update the question
        section_to_update['questions'][question_idx] = updated_question.dict()

        # Save the updated survey template
        save_survey_template(survey_template)
        return {"message": "Question updated successfully"}
    except Exception as e:
        logger.exception("Failed to update question")
        raise HTTPException(status_code=500, detail="Failed to update question")
    
@app.get("/get-question/{section_name}/{question_idx}", status_code=status.HTTP_200_OK)
def get_question(section_name: str, question_idx: int):
    """
    Get a question from a section in the survey template.

    Args:
        section_name (str): The name of the section containing the question.
        question_idx (int): The index of the question to be retrieved.
    
    Returns:
        dict: The question data.
    
    Raises:
        HTTPException: If an error occurs while getting the question.
    """
    try:
        # Find the section containing the question
        section = next((section for section in survey_template['survey'] if section['section'] == section_name), None)

        # Check if the section exists
        if not section:
            logger.error("Section not found")
            raise HTTPException(status_code=404, detail="Section not found")

        # Check if the question index is valid
        if question_idx < 0 or question_idx >= len(section['questions']):
            logger.error("Question index out of range")
            raise HTTPException(status_code=404, detail="Question index out of range")

        # Return the question
        return section['questions'][question_idx]
    except Exception as e:
        logger.exception("Failed to get question")
        raise HTTPException(status_code=500, detail="Failed to get question")

@app.get("/get-section/{section_name}", status_code=status.HTTP_200_OK)
def get_section(section_name: str):
    """
    Get a section from the survey template.

    Args:
        section_name (str): The name of the section to be retrieved.
    
    Returns:
        dict: The section data.
    
    Raises:
        HTTPException: If an error occurs while getting the section.
    """
    try:
        # Find the section containing the question
        section = next((section for section in survey_template['survey'] if section['section'] == section_name), None)

        # Check if the section exists
        if not section:
            logger.error("Section not found")
            raise HTTPException(status_code=404, detail="Section not found")

        # Return the section
        return section
    except Exception as e:
        logger.exception("Failed to get section")
        raise HTTPException(status_code=500, detail="Failed to get section")

@app.get("/get-sections", status_code=status.HTTP_200_OK)
def get_sections():
    """
    Get all sections from the survey template.

    Returns:
        list: The list of sections in the survey template.
    
    Raises:
        HTTPException: If an error occurs while getting the sections.
    """
    try:
        return survey_template['survey']
    except Exception as e:
        logger.exception("Failed to get sections")
        raise HTTPException(status_code=500, detail="Failed to get sections")

