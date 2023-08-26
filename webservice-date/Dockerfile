# Use an official Java runtime as a parent image
FROM amazoncorretto:20-alpine 

# Set the working directory in the container
WORKDIR /app

# Copy the application JAR file and the application.properties file (if needed) into the container
COPY target/webservice-date.jar /app/webservice-date.jar

# Expose the port that your Spring Boot application will run on (default is 8080)
EXPOSE 8080

# Specify the command to run your application
CMD ["java", "-jar", "webservice-date.jar"]
