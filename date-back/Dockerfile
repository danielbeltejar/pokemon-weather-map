FROM cgr.dev/chainguard/wolfi-base as build

RUN apk update && apk add openjdk-20 maven~3.9 openjdk-20-default-jvm

WORKDIR /app
ENV JAVA_HOME=/usr/lib/jvm/java-20-openjdk

COPY .mvn/ .mvn
COPY mvnw pom.xml ./
COPY src ./src

# Ensure mvnw has execute permissions
RUN chmod +x mvnw

USER root

RUN ./mvnw package

# Some Java apps may require extra locale files
# RUN apk add glibc-locale-en

USER nonroot


ENTRYPOINT ["java", "-jar", "/app/target/webservice-date.jar"]
