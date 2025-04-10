from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl

class Awards(BaseModel):
    awards: List[str] = Field(description="job relevant key accomplishments, awards, or recognitions that demonstrate your skills and abilities.")

class Certification(BaseModel):
    certification: str = Field(description="The name of the certification and the organization or institution that issued the certification.")

class Certifications(BaseModel):
    certifications: List[Certification] = Field(description="job relevant certifications that candidate have earned, including the name, issuing organization to verify the certification.")

class Education(BaseModel):
    degree: str = Field(description="The degree or qualification obtained and The major or field of study. e.g., Bachelor of Science in Computer Science, Arizona State University, Tempe, USA, 2025")

class Educations(BaseModel):
    education: List[Education] = Field(description="Educational qualifications, including degree, institution, dates, and relevant courses.")

class Credits(BaseModel):
    category: str
    items: List[str]

class ExperienceResponsibility(BaseModel):
    responsibilities: List[str]

class ProjectExperience(BaseModel):
    # client: str = Field(description="The name of the company or organization.")
    Project: str = Field(description="The name or title of the project.")
    role: str = Field(description="The job title or position held. e.g. Software Engineer, Machine Learning Engineer.")
    location: Optional[str] = None
    duration: str = Field(description="The start date and end date for the project. e.g. Aug 2023 - Nov 2025, Jan 2021 to Dec 2023")
    tools: Optional[List[str]] = None
    # description: str
    description: List[str] = Field(description="A list of 3 bullet points describing the work experience, tailored to match job requirements. Each bullet point should follow the 'Did X by doing Y, achieved Z' format, quantify impact, implicitly use STAR methodology, use strong action verbs, and be highly relevant to the specific job. Ensure clarity, active voice, and impeccable grammar.")
    responsibilities: List[str] = Field(description="Focus on essential functions, their frequency and importance, level of decision-making, areas of accountability, and any supervisory responsibilities.")


class SkillSection(BaseModel):
    name: str = Field(description="name or title of the skill group and competencies relevant to the job, such as programming languages, data science, tools & technologies, cloud & DevOps, full stack,  or soft skills.")
    skills: List[str] = Field(description="Specific skills or competencies within the skill group, such as Python, JavaScript, C#, SQL in programming languages.")

class SkillSections(BaseModel):
    skill_section: List[SkillSection] = Field(description="Skill sections, each containing a group of skills and competencies relevant to the job.")

class Experience(BaseModel):
    client: str = Field(description="The name of the company or organization.")
    Project: Optional[str] = Field(description="The name or title of the project.")
    role: str = Field(description="The job title or position held. e.g. Software Engineer, Machine Learning Engineer.")
    location: str = Field(description="The location of the company or organization. e.g. San Francisco, USA.")
    duration: str = Field(description="The start date and end date for the project. e.g. Aug 2023 - Nov 2025, Jan 2021 to Dec 2023")
    description: List[str] = Field(description="A list of 3 bullet points describing the work experience, tailored to match job requirements. Each bullet point should follow the 'Did X by doing Y, achieved Z' format, quantify impact, implicitly use STAR methodology, use strong action verbs, and be highly relevant to the specific job. Ensure clarity, active voice, and impeccable grammar.")

class Experiences(BaseModel):
    work_experience: List[Experience] = Field(description="Work experiences, including job title, company, location, dates, and description.")


class ResumeSchema(BaseModel):
    professional_summary: Optional[str] = Field(description="""A brief summary or objective statement highlighting key skills, experience, and career goals.
                                                                format:
                                                                    - Paragraph only (no bullets)
                                                                    - First line = "XX+ years of experience..."
                                                                    - Use provided experience details
                                                                    - Limit to 4-6 lines
                                                                """)
    professional_experience: Optional[str] = Field(description="""A brief pointwise summary of professional experience of candidate's whole career.
                                                                format:
                                                                    - Use bullet points
                                                                    - No individual client headers
                                                                    - Summarize key contributions
                                                                    - Example:
                                                                        - 'Implemented scriptless automation design using UFT.'
                                                                        - 'Handled a 7-member team as an Automation Lead.'
                                                                """)
    awards: List[str] = Field(description="job relevant key accomplishments, awards, or recognitions that demonstrate your skills and abilities.")
    certifications: List[Certification] = Field(description="job relevant certifications that you have earned, including the name, issuing organization to verify the certification.")
    education: List[Education] = Field(description="Educational qualifications, including degree, institution, dates, and relevant courses.")
    credits: List[Credits] = Field(description="Grouped skills and tools, each containing a group of skills and competencies relevant to the job.")
    work_experience: List[Experience] = Field(description="Work experiences, including job title, company, location, dates, and description.")
    project_experience: List[ProjectExperience] = Field(description="Project-based work experience including client, role, tools, and responsibilities.")