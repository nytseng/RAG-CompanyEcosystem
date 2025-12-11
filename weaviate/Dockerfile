# Start from the official Weaviate image you are using
FROM cr.weaviate.io/semitechnologies/weaviate:1.33.1

USER root
# Set the working directory to the persistence path
WORKDIR /var/lib/weaviate

# Copy your local backups into the "backups" directory within the image
# This assumes your local backups are in a directory named 'weaviate_backups'
# relative to where you run the 'docker build' command.
COPY ./weaviate_backups/ ./backups/
COPY ./weaviate_db_restore.py .


# The rest of the Weaviate configuration is handled by docker-compose environment variables
