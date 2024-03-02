# Install Chrome WebDriver
FROM python:3.9-slim

WORKDIR /app

# Install necessary packages to run WebDriver
RUN apt-get update \
  && apt-get install -y --no-install-recommends curl wget unzip libglib2.0 libnss3 libgconf-2-4 libfontconfig1 chromium \
  #&& wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
  #&& dpkg -i google-chrome-stable_current_amd64.deb || apt-get install -yf \
  #&& rm google-chrome-stable_current_amd64.deb \
  && wget https://storage.googleapis.com/chrome-for-testing-public/122.0.6261.94/linux64/chromedriver-linux64.zip \
  && unzip chromedriver-linux64.zip \
  && cd chromedriver-linux64 \
  && chmod +x chromedriver \
  && mv chromedriver /usr/local/bin/ \
  && cd .. \
  && apt-get remove -y wget unzip curl \
  && rm chromedriver-linux64.zip \
  && rm -rf /var/lib/apt/lists/*

# Add Chrome binary to the PATH
#ENV PATH="/usr/bin/google-chrome:${PATH}"

# Copy the requirements.txt file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Make port 1876 available to the world outside this container
EXPOSE 1876

# Run the command to start uvcorn server and scraper
CMD ["./start.sh"]