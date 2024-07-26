from typing import List, Literal
from pydantic import BaseModel

class Question(BaseModel):
    """
    Represents a question in a survey.
    
    Attributes:
        type (str): The type of the question.
        question (str): The text of the question.
        options (List[str]): The list of options for the question.
    """
    type: str
    question: str
    options: List[str]

class Section(BaseModel):
    """
    Represents a section in a survey.
    
    Attributes:
        section (str): The name of the section.
        questions (List[Question]): The list of questions in the section.
    """
    section: str
    questions: List[Question]

class Survey(BaseModel):
    """
    Represents a survey.
    
    Attributes:
        survey (List[Section]): The list of sections in the survey.
    """
    survey: List[Section]

class QuestionCreate(BaseModel):
    """
    Represents a question for creating new sections.
    
    Attributes:
        type (str): The type of the question.
        question (str): The text of the question.
        options (List[str]): The list of options for the question.
    """
    type: str
    question: str
    options: List[str]

class SectionUpdate(BaseModel):
    """
    Represents an update for a section.
    
    Attributes:
        section (str): The name of the section.
        questions (List[QuestionCreate]): The list of questions for the section.
    """
    section: str
    questions: List[QuestionCreate]