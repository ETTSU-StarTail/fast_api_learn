from enum import Enum

from fastapi import FastAPI


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app: FastAPI = FastAPI()


@app.get("/")
async def root() -> dict[str, str]:
    """# Hello World

    ```python
    from fastapi import FastAPI

    app: FastAPI = FastAPI()

    @app.get("/") # get メソッドで / アクセスしたとき
    async def root() -> dict[str, str]: # この関数を処理
        return {"message": "Hello, world!"}
    ```

    ## app: FastAPI = FastAPI()

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

    ## API と HTTP メソッドの関係

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

    ## async def root():

    path operations といい、 decorator 直下の関数を指す。

    decorator で指定した operation と path によって FastAPI が呼び出す関数。
    `async def` でも `def` でも定義可能。

    FastAPI は非同期で高速に動作するのでどちらでもよい、と記載されている。
    サードパーティーライブラリに応じて切り替えることを推奨しているっぽい。

    ## return {"message": "Hello World"}

    path operations は `dict`, `list`, `str`, `int` もしくは、pydantic モデルを返せる。
    JSON に自動的に変換されるオブジェクトやモデルは他にもたくさんある模様。OR マッパーなど。"""

    return {"message": "Hello, world!"}


@app.get("/items/{item_id}")
async def read_item(item_id: int) -> dict[str, int]:
    """# path parameter

    ```python
    from fastapi import FastAPI

    app = FastAPI()


    @app.get("/items/{item_id}")
    async def read_item(item_id: int):
        return {"item_id": item_id}
    ```

    ## @app.get("/items/{item_id}")

    format 文字列同様にパラメータを宣言できる。

    ## async def read_item(item_id: int):

    パラメータの方は型アノテーションにより定義できる。

    これによって FastAPI は自動的に解析する。
    バリデーションも実施される。
    """

    return {"item_id": item_id}


@app.get("users/me")
async def read_user_me() -> dict[str, str]:
    """# path operations の順序

    ```python
    @app.get("users/me")
    async def read_user_me() -> dict[str, str]:
        return {"user_id": "the current user"}


    @app.get("users/{user_id}")
    async def read_user(user_id: str) -> dict[str, str]:
        return {"user_id": user_id}
    ```

    `/users/me` と `users/{user_id}` は別の API であり、上述はその想定通り動作する。

    もし `/users/me` の上部に `/users/{user_id}` がある場合、想定外の動作となる。具体的には下記。

    1. `/users/me` で GET リクエストを受信
    1. 先に作成された path operations である `/users/{user_id}` にヒット
    1. `/users/{user_id}` が `me` を受け取る"""

    return {"user_id": "the current user"}


@app.get("users/{user_id}")
async def read_user(user_id: str) -> dict[str, str]:
    """# path operations の順序

    ```python
    @app.get("users/me")
    async def read_user_me() -> dict[str, str]:
        return {"user_id": "the current user"}


    @app.get("users/{user_id}")
    async def read_user(user_id: str) -> dict[str, str]:
        return {"user_id": user_id}
    ```

    `/users/me` と `users/{user_id}` は別の API であり、上述はその想定通り動作する。

    もし `/users/me` の上部に `/users/{user_id}` がある場合、想定外の動作となる。具体的には下記。

    1. `/users/me` で GET リクエストを受信
    1. 先に作成された path operations である `/users/{user_id}` にヒット
    1. `/users/{user_id}` が `me` を受け取る"""

    return {"user_id": user_id}


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName) -> dict[str, str]:
    """# Enum 型アノテーション

    ```python
    from enum import Enum

    from fastapi import FastAPI


    class ModelName(str, Enum):
        alexnet = "alexnet"
        resnet = "resnet"
        lenet = "lenet"


    app = FastAPI()


    @app.get("/models/{model_name}")
    async def get_model(model_name: ModelName):
        if model_name == ModelName.alexnet:
            return {"model_name": model_name, "message": "Deep Learning FTW!"}

        if model_name.value == "lenet":
            return {"model_name": model_name, "message": "LeCNN all the images"}

        return {"model_name": model_name, "message": "Have some residuals"}
    ```

    `str`, `Enum` を継承したサブクラスを作成する。これにより API ドキュメントに `str` であることを伝えられ、正確にレンダリングされる（`str` で渡される `Enum` のデータだと判断される）

    あとは、サブクラスを path parameter の型アノテーションに定義すればよい。

    """

    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str) -> dict[str, str]:
    """# ファイルパスを含む path parameter の宣言

    ```python
    from fastapi import FastAPI

    app = FastAPI()

    @app.get("/files/{file_path:path}")

    async def read_file(file_path: str):
        return {"file_path": file_path}
    ```

    path parameter に param_name: path とすることで
    いかなるファイルパスとマッチする path parameter を宣言できる

    OpenAPI ではサポートしていないが、FastAPI もとい Starlette の内部ツールにより実現されている

    ただし、`files//path/to/file.txt` のようにパラメータ部分が `/` から始まる必要がある。
    """

    return {"file_path": file_path}
