# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Set environment variables individually
# MongoDB connection Credentials
ENV CONNECTION_STRING="mongodb+srv://phyozawlinn1852020:waiyanhtutgay@sarrmalcluster.pi3tc.mongodb.net/?retryWrites=true&w=majority&appName=SarrmalCluster"
# Secrete Key for JWT or other 
ENV SECRET_KEY="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ENV ALGORITHM="HS256"
# GEMINI api Key
ENV GEMINI_KEY="AIzaSyBrxMCNDnKxpSuWwAW4HF0vaWmq098Bw4Y"
#UNSPLASH access keys
ENV UNSPLASH_ACCESS_KEY1="cu3LKjL5__dbJt-cOgaINxfojsaOiWj1abQm-jbTItI"
ENV UNSPLASH_ACCESS_KEY2="TAxJ_BrVqBK7hBt9-5phmDwBNC7VPSd1ampp2EyoNyI"
#GOOGLE OAUTH FOR FAST api
ENV GOOGLE_CLIENT_ID="696113625872-9k81hf1irq37ou8eft9jukpcadrlr74f.apps.googleusercontent.com"
ENV GOOGLE_CLIENT_SECRET="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"
ENV GOOGLE_REDIRECT_URI="http://onebitmyanmar.site"
ENV DEBUG=False

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run FastAPI using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
