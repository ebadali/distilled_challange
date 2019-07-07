FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

RUN chmod 644 ./run.py

# CMD [ "python", "./run.py" ]
CMD ["gunicorn", "-w","1" ,"-b", "0.0.0.0:5000", "run:app", "--reload"]
