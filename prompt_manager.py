from google.genai import types
import logging

# Get logger for this module
logger = logging.getLogger(__name__)

class PromptManager:
    def __init__(self):
        # You could load prompts from config files here if needed
        self._resume_extractor_prompt_text = """<objective>
            Parse a text-formatted resume efficiently and extract diverse candidate's data into a structured JSON format.
            </objective>

            <input>
            The following text is the candidate's resume in plain text format:

            {resume_text}
            </input>

            <instructions>
            ## Follow these steps to extract and structure the resume information:

            1. Analyze Structure:
            - Examine the text-formatted resume to identify key sections (e.g., personal information, education, experience, skills, certifications).
            - Note any unique formatting or organization within the resume.

            2. Extract Information:
            - Systematically parse each section, extracting relevant details.
            - Pay attention to dates, titles, organizations, and descriptions.

            3. Handle Variations:
            - Account for different resume styles, formats, and section orders.
            - Adapt the extraction process to accurately capture data from various layouts.

            5. Optimize Output:
            - Handle missing or incomplete information appropriately (use null values or empty arrays/objects as needed).
            - Standardize date formats, if applicable.

            6. Validate:
            - Review the extracted data for consistency and completeness.
            - Ensure all required fields are populated if the information is available in the {resume_text}.

            7. Title/Headers Handling:
            - Maintain the order of clients in project/work experiences.
            - Identify the correct project names over general subheaders.

            ## Step to follow to write a JSON resume section of "Professional Summary" for the candidate.
            1. Analyze my `professional summary` details from {resume_text} to match job requirements.
            2. Create a JSON resume section that highlights strongest matches
            3. Optimize JSON section for clarity and relevance to the {resume_text}.

            Instructions:
            1. Focus: Craft relevant `professional summary` aligned with the {resume_text}.
            2. Content:
            2.1. Paragraph: single paragraph with limit of 4-6 lines, closely mirroring {resume_text}.
            2.2. Impact: Quantify paragraph point for measurable results.
            2.3. Storytelling: Utilize STAR methodology (Situation, Task, Action, Result) implicitly within paragraph text.
            2.4. Action Verbs: Showcase technical skills with strong, active verbs.
            2.5. Honesty: Prioritize truthfulness and objective language.
            2.6. Structure: Each paragraph follows "XX+ years of experience..." format.
            3. Honesty: Prioritize truthfulness and objective language.
            4. Specificity: Prioritize relevance to the {resume_text} over general `professional summary` details.
            5. Style:
            5.1. Voice: Use active voice whenever possible.
            5.2. Proofreading: Ensure impeccable spelling and grammar.

            <example>
            "professional summary": [
                {{
                "Seasoned Business Analyst/Project manager with over 10 years of consultancy expertise. Specializing in overseeing software development projects across Manufacturing, Banking, and Finance sectors. Proficient in both Waterfall and Agile methodologies. Effective in team management, stakeholder relations, and technology adaptation. Known for guiding teams to project success through coaching and mentoring."
                }},
                {{
                "As a Technical Lead with extensive experience in web application development, particularly in MERN stack projects, JavaScript, TypeScript and Next JS, I have worked across multiple domains, including assurance, telecom, IT infrastructure, and retail applications. I have participated in designing application architecture from the ground up and worked with Microsoft Azure DevOps and AWS services such as ECS, S3 for static site deployment and Elastic Beanstalk for Node JS applications."
                }},
                [and So on ...]
            ]
            </example>

            ## Step to follow to write a JSON resume section of "Professional Experience" for the candidate.
            if `professional experience` section present in {resume_text}:
                {{
                1. Analyze my `professional experience` details from {resume_text} to match job requirements.
                2. Create a JSON resume section that highlights strongest matches
                3. Optimize JSON section for clarity and relevance to the {resume_text}.

                Instructions:
                1. Focus: Craft relevant `professional experience` aligned with the {resume_text}.
                2. Content:
                2.1. Bullet points: all bullet points as per the {resume_text}.
                2.2. Impact: Quantify bullet points for measurable results.
                2.3. Storytelling: Utilize STAR methodology (Situation, Task, Action, Result) implicitly within each bullet point.
                2.4. Action Verbs: Showcase technical skills with strong, active verbs.
                2.5. Honesty: Prioritize truthfulness and objective language, mirrors to {resume_text}.
                2.6. Structure: Each bullet point follows "Did X by doing Y, achieved Z" format.
                2.7. Specificity: Prioritize relevance to the {resume_text} over general `professional experience`.
                3. Honesty: Prioritize truthfulness and objective language.
                4. Specificity: Prioritize relevance to the {resume_text} over general `professional experience` details.
                5. Honesty: Prioritize truthfulness and objective language.
                6. Style:
                6.1. Voice: Use active voice whenever possible.
                6.2. Proofreading: Ensure impeccable spelling and grammar.
                }}
            else:
                {{
                1. Analyze {resume_text} for `professional experience` details.
                2. Create a JSON resume section that highlights strongest matches
                3. Optimize JSON section for clarity and relevance to the {resume_text}.

                Instructions:
                1. Focus: Craft relevant `professional experience` aligned with the {resume_text}.
                2. Content:
                2.1. Bullet points: design all possible bullet points as per the {resume_text}.
                2.2. Impact: Quantify bullet points for measurable results.
                2.3. Storytelling: Utilize STAR methodology (Situation, Task, Action, Result) implicitly within each bullet point.
                2.4. Action Verbs: Showcase technical skills with strong, active verbs.
                2.5. Honesty: Prioritize truthfulness and objective language.
                2.6. Structure: Each bullet point follows "Did X by doing Y, achieved Z" format.
                2.7. Specificity: Prioritize relevance to the {resume_text} over general `professional experience`.
                3. Honesty: Prioritize truthfulness and objective language.
                4. Specificity: Prioritize relevance to the {resume_text} over general `professional experience` details.
                5. Honesty: Prioritize truthfulness and objective language.
                6. Style:
                6.1. Voice: Use active voice whenever possible.
                6.2. Proofreading: Ensure impeccable spelling and grammar.}}

            <example>
            "professional experience": [
                [
                    "Skilled in the formulation and implementation of pioneering software solutions, substantially elevating business productivity.",
                    "Proficient in utilizing a diverse set of programming languages, tools, databases for backend development, ensuring seamless integration and optimal performance.",
                    "Renowned for successfully implementing strategies that amplify overall performance of the software systems.",
                    "Exhibits resilient leadership characteristics, promoting team collaboration and propelling progress amidst intricate technical obstacles.",
                    [and So on ...],
                ],
                [
                    "10 Years of BFSI industry experience in Banking (HDFC Bank) and Insurance (ICICI Lombard), with MBA background.",
                    "Domain Knowledge: Retail and Corporate Banking - CASA, Term Deposits, Mortgages, Payments, Cards, Collections, Recoveries, Treasury, Insurance, Risk Management, Digital Banking, End-to-end Financial Processes.",
                    "Proficiency Forte: Customer journeys, Operations and processes, Regulatory compliance, Applications and functionality, IT Product hands-on, Platform migration, Workflow management, Digital transformation, UI and UX Enhancements, Business readiness, Data and MI reporting, Investments and Portfolio management,",
                    [and So on ...]
                ],
                [
                    "Requirement Elicitation",
                    "Stakeholder Management",
                    "Problem Solving",
                    "Effective Communication",
                    "Team Collaboration",
                    "Data Analysis",
                    "Risk Management",
                    "Project Management",
                    "Agile Methodologies",
                    [and So on ...]
                ],
                [and So on ...]
            ]
            </example>

            ## Step to follow to write a JSON resume section of "Awards" for the candidate.
            1. Analyze my achievements details to match job requirements.
            2. Create a JSON resume section that highlights strongest matches
            3. Optimize JSON section for clarity and relevance to the job description.

            Instructions:
            1. Focus: Craft relevant achievements aligned with the {resume_text}.
            2. Honesty: Prioritize truthfulness and objective language.
            3. Specificity: Prioritize relevance to the specific job over general achievements.
            4. Style:
            4.1. Voice: Use active voice whenever possible.
            4.2. Proofreading: Ensure impeccable spelling and grammar.

            <example>
            "awards": [
                "Won E-yantra Robotics Competition 2018 - IITB.",
                "1st prize in “Prompt Engineering Hackathon 2023 for Humanities”",
                "Received the 'Extra Miller - 2021' award at Winjit Technologies for outstanding performance.",
                [and So on ...]
            ]
            </example>

            ## Step to follow to write a JSON resume section of "Certifications" for an applicant applying for job posts.

            1. Analyze my certification details to match job requirements.
            2. Create a JSON resume section that highlights strongest matches
            3. Optimize JSON section for clarity and relevance to the job description.

            Instructions:
            1. Focus: Include relevant certifications aligned with the job description.
            2. Proofreading: Ensure impeccable spelling and grammar.

            <example>
            "certifications": [
                {{
                "certification": "Deep Learning Specialization by DeepLearning.AI, Coursera Inc.",
                }},
                {{
                "certification": "Server-side Backend Development by The Hong Kong University of Science and Technology.",
                }}
                ...
            ],
            </example>

            ## Step to follow to write a JSON resume section of "Education" for an candidate:

            1. Analyze my education details to match job requirements.
            2. Create a JSON resume section that highlights strongest matches
            3. Optimize JSON section for clarity and relevance to the job description.

            Instructions:
            - Keep education from Bachelor's degree onwards, igonre previous qualifications.
            - Maintain truthfulness and objectivity in listing experience.
            - Prioritize specificity - with respect to job - over generality.
            - Proofread and Correct spelling and grammar errors.
            - Aim for clear expression over impressiveness.
            - Prefer active voice over passive voice.

            <example>
            "education": [
            {{
                "education": "B.Tech in Information Technology, Full-time, Graduated in 2009"
            }}
            {{
                "education": "M. Tech Integrated Software Engineering, Vellore Institute of Technology, Tamil Nādu, India, 2021"
            }}
            {{
                "education": "Masters of Science - Computer Science (Thesis), Arizona State University, Tempe, USA, 2025"
            }}
            {{
                "education": "Passed with 75% Marks in B. E (E.C. E) at K. Ramakrishnan College of Technology, Trichy"
            }}
            [and So on ...]
            ],
            </example>

            ## Step to follow to write a JSON resume section of "Credits" for an candidate:

            1. Analyze my Credits details to match job requirements.
            2. Create a JSON resume section that highlights strongest matches.
            3. Optimize JSON section for clarity and relevance to the job description.

            Instructions:
            - look under the `skills` section to find the credits.
            - keep all the listed `skills` from extracted text.
            - Specificity: Prioritize relevance to the specific job over general achievements.
            - Proofreading: Ensure impeccable spelling and grammar.

            <example>
            "skill_section": [
                {{
                "category": "Programming Languages",
                "items": ["Python", "JavaScript", "C#", and so on ...]
                }},
                {{
                "category": "Cloud and DevOps",
                "items": [ "Azure", "AWS", and so on ... ]
                }},
                and so on ...
            ]
            </example>

            ## Step to follow to write a JSON resume section of "Work Experience" for an candidate:

            1. Analyze my Work details to match job requirements.
            2. Create a JSON resume section that highlights strongest matches
            3. Optimize JSON section for clarity and relevance to the job description.

            Instructions:
            1. Focus: Craft all the work experiences present in the {resume_text}.
            2. Content:
            2.1. Bullet points: all as per the {resume_text}, without making any modifications.
            2.2. Impact: Quantify each bullet point for measurable results.
            2.3. Storytelling: Utilize STAR methodology (Situation, Task, Action, Result) implicitly within each bullet point.
            2.4. Action Verbs: Showcase soft skills with strong, active verbs.
            2.5. Honesty: Prioritize truthfulness and objective language.
            2.6. Structure: Each bullet point follows "Did X by doing Y, achieved Z" format.
            2.7. Specificity: Prioritize relevance to the specific job over general achievements.
            3. Style:
            3.1. Clarity: Clear expression trumps impressiveness.
            3.2. Voice: Use active voice whenever possible.
            3.3. Proofreading: Ensure impeccable spelling and grammar.

            <example>
            "work_experience": [
                {{
                "client": "Winjit Technologies",
                "project": "DRYiCE - iAutomate/ Research & Development"
                "role": "Software Engineer",
                "location": "Pune, India",
                "duration": "jan 2020 - Feb 2022",
                "description": [
                    "Engineered 10+ RESTful APIs Architecture and Distributed services; Designed 30+ low-latency responsive UI/UX application features with high-quality web architecture; Managed and optimized large-scale Databases. (Systems Design)",  
                    "Initiated and Designed a standardized solution for dynamic forms generation, with customizable CSS capabilities feature, which reduces development time by 8x; Led and collaborated with a 12 member cross-functional team. (Idea Generation)"  
                    and so on ...
                ]
                }},
                {{
                "client": "IMATMI, Robbinsville",
                "project": "AE & Eservice of RL",
                "role": "Research Intern",
                "location": "New Jersey (Remote)",
                "duration": "Mar 2019 - Aug 2023",
                "description": [
                    "Conducted research and developed a range of ML and statistical models to design analytical tools and streamline HR processes, optimizing talent management systems for increased efficiency.",
                    "Created 'goals and action plan generation' tool for employees, considering their weaknesses to facilitate professional growth.",
                    and so on ...
                ]
                }}
            ],
            </example>


            ## Step to follow to write a JSON resume section of "Project Experience" for an candidate:

            1. Analyze my project details to match job requirements.
            2. Create a JSON resume section that highlights strongest matches
            3. Optimize JSON section for clarity and relevance to the job description.

            Instructions:
            1. Focus: Craft all project experiences present in the context.
            2. Content:
            2.1. Bullet points: all per experiences, without making any modifications.
            2.2. Impact: Quantify each bullet point for measurable results.
            2.3. Storytelling: Utilize STAR methodology (Situation, Task, Action, Result) implicitly within each bullet point.
            2.4. Action Verbs: Showcase soft skills with strong, active verbs.
            2.5. Honesty: Prioritize truthfulness and objective language.
            2.6. Structure: Each bullet point follows "Did X by doing Y, achieved Z" format.
            2.7. Specificity: Prioritize relevance to the specific job over general achievements.
            3. Style:
            3.1. Clarity: Clear expression trumps impressiveness.
            3.2. Voice: Use active voice whenever possible.
            3.3. Proofreading: Ensure impeccable spelling and grammar.

            <example>
            "projects": [
                {{
                "name": "Search Engine for All file types - Sunhack Hackathon - Meta & Amazon Sponsored",
                "Role": "Team Lead",
                "location": "Pune, Maharashtra",
                "duration": "Nov 2023 - Jan 2025"
                "tools": ["Node", "JS", ".NET", "Redux", "MSAL", "MongoDB", so on ... ]
                "description": [
                    "1st runner up prize in crafted AI persona, to explore LLM's subtle contextual understanding and create innovative collaborations between humans and machines. Devised a TabNet Classifier Model having 98.7% accuracy in detecting forest fire through IoT sensor data, deployed on AWS and edge devices 'Silvanet Wildfire Sensors' using technologies TinyML, Docker, Redis, and celery.",
                    [and So on ...]
                ],
                "responsibilities": [
                    "Envisioned Solution Architecture and Design for modernization efforts",
                    "Adopted DevOps practices including CI/CD, Test Automation, Deployment automation, etc.",
                    "Participated in release review/requirement analysis and design review meetings",
                    [and So on ...]
                ]
                }}
                [and So on ...]
            ]
            </example>



            </instructions>
        """

        self._resume_formatter_prompt_text = """<objective>
            Parse a text-formatted resume efficiently and extract diverse candidate's data into a structured JSON format.
            </objective>

            <input>
            The following text is the candidate's resume in plain text format:

            {resume_text}
            </input>

            <instructions>
            ## Follow these steps to extract and structure the {resume_text}:

            1. Analyze Structure:
            - Examine the text-formatted resume to identify key sections (e.g., personal information, education, experience, skills, certifications).
            - Note any unique formatting or organization within the resume.

            2. Extract Information:
            - Systematically parse each section, extracting relevant details.
            - Pay attention to dates, titles, organizations, and descriptions.

            3. Handle Variations:
            - Account for different resume styles, formats, and section orders.
            - Adapt the extraction process to accurately capture data from various layouts.

            5. Optimize Output:
            - Handle missing or incomplete information appropriately (use null values or empty arrays/objects as needed).

            6. Validate:
            - Review the extracted data for consistency and completeness.
            - Ensure all required fields are populated if the information is available in the resume.

            ## Instructions ##:
            - Identify all the sections from {resume_text}
            - Maintain truthfulness and objectivity in listing experience.
            - Prioritize authenticity - with respect {resume_text} - over generality.
            - Proofread and Correct spelling and grammar errors.
            - Aim for clear expression over impressiveness.
            - Prefer active voice over passive voice.
            - Proofreading: Ensure impeccable spelling and grammar.
            - Content:
                ```sections```: folllow the sequence of sections:
                <Sections>
                {professional_summary}
                {professional_experience}
                {awards}
                {certifications}
                {education}
                {credits}
                {work_experience}
                {project_experience}
                </Sections>
                ```authencity```: Prioritize keeping original context from {resume_text} for each section.

            </instructions>
        """

    def get_resume_extractor_prompt(self) -> types.Part:
        logger.info("Returning resume extractor prompt.")
        return types.Part.from_text(text=self._resume_extractor_prompt_text)

    def get_resume_formatter_prompt(self) -> types.Part:
        logger.info("Returning resume formatter prompt.")
        return types.Part.from_text(text=self._resume_formatter_prompt_text)

# Create a single instance of the PromptManager (Singleton pattern if needed)
prompt_manager = PromptManager()
