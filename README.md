# FastAPI를 이용해서 웹으로 LLM과 대화를 해봅니다.

![image](https://github.com/user-attachments/assets/a4eed516-104d-4d79-9718-427551d92f01)


## 0. 세팅 

```
conda create -n fastapi python=3.10 -y
```

```
pip install -r requirements.txt
```

GPU가 있는 경우 

```
pip install faiss-cpu
```

GPU가 없는 경우 

```
pip install faiss-gpu
```


## 1. ChatGPT API 사용하기 

### 1.1 .env 파일

.env.example 파일을 .env로 이름을 바꿔주세요. 

### 1.2 api key 발급 

[openai api key 발급 ](https://platform.openai.com/settings/organization/api-keys)


해당 페이지에서 + Chreate new secret key 버튼을 클릭합니다. 

이름은 아무거나 정해주고 

defalut project를 선택해줍니다. 

api key를 copy 해줍니다. 

.env 파일에 붙여넣기를 합니다.

OPENAI_API_KEY = sk-xxxxxx 


### 1.3 실행하기 

main.py를 실행합니다. 


http://0.0.0.0:8000/ 에 접속합니다. 

예제로 아래 URL를 입력해봅니다. 

https://aws.amazon.com/ko/what-is/retrieval-augmented-generation/


Process URL 버튼을 클릭합니다. 

대화를 진행해봅니다. 

![스크린샷 2025-01-16 16-56-46](https://github.com/user-attachments/assets/89228a7f-10c1-4df9-8462-e59780f13cbb)
