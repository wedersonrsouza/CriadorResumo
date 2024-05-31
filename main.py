import os

from crewai import Agent, Crew, Task
from langchain_openai import ChatOpenAI
from PyPDF2 import PdfReader

# Configuração do CrewAI
os.environ["OPENAI_API_KEY"] = "sua_chave_api_aqui"

# Inicialize o modelo Llama 2 com a URL base do seu servidor local
llm = ChatOpenAI(model="crewai-llama3", base_url="http://localhost:11434/v1")

# Agente para extrair texto do PDF
pdf_extractor_agent = Agent(
    role="PDF Text Extractor",
    goal="Extract all the text from the given PDF file.",
    backstory="You are a skilled agent capable of reading PDF files and extracting their content.",
    allow_delegation=False,
    verbose=True,
    llm=llm
)

# Agente para criar a apostila
professor_agent = Agent(
    role="Experienced Cursinho Teacher",
    goal="Create a study guide based on the extracted PDF content for a specific subject.",
    backstory="""You are an experienced cursinho teacher with a deep understanding of various subjects.
                 You can create comprehensive study guides that help students prepare for exams.""",
    allow_delegation=False,
    verbose=True,
    llm=llm
)

# Função para ler o PDF e extrair o texto
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

# Função para criar a apostila
def create_study_guide(subject, pdf_text):
    task_description = f"Create a study guide about {subject} using the following content:\n{pdf_text}"
    expected_output = "Um guia de estudo detalhado sobre o assunto fornecido."
    task = Task(description=task_description, agent=professor_agent, expected_output=expected_output)
    crew = Crew(agents=[professor_agent])
    result = crew.complete_task(task)
    return result

# Caminho para o arquivo PDF
pdf_path = 'Book - Sistemas Operacionais Modernos - Tanenbaum - 4 Edicao (1).pdf'

# Assunto da apostila
subject = 'Princípios de sistemas operacionais'

# Executar o script
pdf_text = extract_text_from_pdf(pdf_path)
study_guide = create_study_guide(subject, pdf_text)

# Salvar a apostila em um arquivo
with open('apostila.txt', 'w') as file:
    file.write(study_guide)
