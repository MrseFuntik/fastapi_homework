from fastapi import FastAPI, Path
from fastapi.responses import PlainTextResponse, HTMLResponse, FileResponse

app = FastAPI()


@app.get("/")
def root():
    return 'Hello, student'


@app.get("/add")
def add(x: int, y: int) -> int:
    return x + y


@app.get("/double/{number}")
def double(number: int) -> int:
    return number * 2


@app.get("/welcome/{name}")
def func1(name: str = Path(min_length=2, max_length=6)):
    return f'Good luck, {name}'


@app.get('/text')
def get_text():
    content = 'Lorum insop'
    return PlainTextResponse(content=content)


@app.get('/html')
def get_html():
    content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>МОВС</title>
</head>
<body>
<h1>Привет!</h1>
<h2>Пока!</h2>
</body>
</html>
    '''
    return HTMLResponse(content=content)


@app.get('/file')
def get_file():
    content = 'index.html'
    return FileResponse(content, media_type='application/octet-stream', filename='index_2.html')

