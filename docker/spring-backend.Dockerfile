# Build stage
FROM maven:3.8.5-openjdk-17-slim AS build
WORKDIR /app

# Copy pom and go offline to cache dependencies
COPY backend/pom.xml .
RUN mvn dependency:go-offline -B

# Copy source files and build jar
COPY backend/src ./src
RUN mvn package -DskipTests -B

# Run stage
FROM openjdk:17-slim
WORKDIR /app

COPY --from=build /app/target/conciergeiq-1.0.0.jar app.jar

EXPOSE 8080

# Run JVM jar
CMD ["java", "-jar", "app.jar"]
