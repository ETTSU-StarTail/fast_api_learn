# チュートリアルメモ

## Hello World

```python
from fastapi import FastAPI

app: FastAPI = FastAPI()

@app.get("/") # get メソッドで / アクセスしたとき
async def root() -> dict[str, str]: # この関数を処理
    return {"message": "Hello, world!"}
```

### app: FastAPI = FastAPI()

```python
app: FastAPI = FastAPI()
```

`app` は API を作成する為の主要なポイント（コア）となる。
ASGI サーバ Uvicorn を稼働させるときは `uvicorn app.main:app` で参照させる。

例えば `app` を `myapp` とした場合は下記のように変わる。

```python
from fastapi import FastAPI

myapp: FastAPI = FastAPI()

@myapp.get("/") # get メソッドで / アクセスしたとき
async def root() -> dict[str, str]: # この関数を処理
    return {"message": "Hello, world!"}
```

ASGI サーバ Uvicorn を稼働させるときは `uvicorn app.main:myapp` で参照させる。

# API と HTTP メソッドの関係

データ処理は下記がある。

- CREATE
- READ
- UPDATE
- DELETE

API サーバでは HTTP プロトコルのメソッドでこれを指示することが多く、それぞれ下記で表す。

- CREATE → POST
- READ → GET
- UPDATE → PUT
- DELETE → DELETE

HTTP メソッドには、その他に下記がある。

- OPTIONS
- HEAD
- PATCH
- TRACE

FastAPI のチュートリアルによれば、GraphQL の場合は POST で完結するようだ。

OpenAPI ではこれらの HTTP メソッドを Operation と定義している。

FastAPI では下記を decorator としてメソッドを指定し API を実装

- POST → `@app.post`
- GET → `@app.get`
- PUT → `@app.put`
- DELETE → `@app.delete`
- OPTIONS → `@app.options`
- HEAD → `@app.head`
- PATCH → `@app.patch`
- TRACE → `@app.trace`

### async def root():

path operation 関数といい、 decorator 直下の関数を指す。

decorator で指定した operation と path によって FastAPI が呼び出す関数。

`async def` でも `def` でも定義可能

FastAPI は非同期で高速に動作するのでどちらでもよい、と記載されている。

サードパーティーライブラリに応じて切り替えることを推奨しているっぽい。

### return \{"message": "Hello World"\}

path operation 関数は `dict`, `list`, `str`, `int` もしくは、pydantic モデルを返せる。

JSON に自動的に変換されるオブジェクトやモデルは他にもたくさんある模様。OR マッパーなど。
