

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from openai import OpenAI

client = OpenAI(api_key="OPENAI_API_KEY")

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "answer": None})

@app.post("/")
async def ask_question(request: Request, question: str = Form(...)):
    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo-0125",
        # model="text-davinci-003",
        messages=[{"role": "user", "content": f"Correct the grammar of the following text:\n\n{question}"}],
        max_tokens=150)
        answer = response.choices[0].message.content
        return templates.TemplateResponse("index.html", {"request": request, "question": question, "answer": answer})
    except Exception as e:
        return templates.TemplateResponse("index.html", {"request": request, "question": question, "answer": f"Error: {e}"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)



