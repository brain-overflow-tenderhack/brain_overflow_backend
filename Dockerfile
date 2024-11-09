# At this stage we convert Poetry's dependency file into a more traditional
# requirements.txt to avoid installing Poetry into the final container.
# Although very slow, this cannot be skipped, as we need to resolve dependencies
# for the exact platform the client is using.
FROM python:3.12
WORKDIR .
RUN pip install --upgrade pip
# Final container build. Uses pre-compiled dependencies and requirements.txt
# obtained in the previous steps
FROM python:3.12
WORKDIR /src
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
COPY . /src
