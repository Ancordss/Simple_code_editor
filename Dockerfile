from python:3.7.2-alpine3.9
copy . .
RUN apk add --no-cache gcc musl-dev linux-headers
run pip install -r requirements.txt

CMD ["python", "main.py"]
