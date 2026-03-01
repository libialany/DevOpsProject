**Building & Compiling Java Spring Boot**

**Container Images for ARM64**

*A Practical Guide for DevOps Engineers*

Targeting Raspberry Pi • AWS Graviton • ARM64 Platforms

Using Docker Buildx for Cross-Platform Builds on x86/Linux

**1. Introduction**

This tutorial walks beginner DevOps engineers through the process of
building and compiling a Java Spring Boot application into a Docker
container image that targets the ARM64 architecture. You will use Docker
Buildx on an x86 Linux host to produce images that run natively on ARM64
devices such as the Raspberry Pi and AWS Graviton-based EC2 instances.

+-----------------------------------------------------------------------+
| **What You Will Learn**                                               |
|                                                                       |
| How to set up Docker Buildx for cross-platform builds • How to write  |
| an optimized multi-stage Dockerfile for Spring Boot • How to build    |
| and push an ARM64 image from an x86 host • How to reduce image size   |
| using layering and JRE-only base images                               |
+-----------------------------------------------------------------------+

**1.1 Prerequisites**

This guide assumes you already have basic familiarity with:

- Docker concepts: images, containers, Dockerfiles, and docker build

- Spring Boot: project structure, Maven or Gradle builds

- Linux command line: file navigation, running commands

**1.2 Why ARM64?**

ARM64 (also called AArch64) is increasingly common in production
environments. AWS Graviton instances offer up to 40% better
price-performance than x86 equivalents. Raspberry Pi devices are popular
for edge computing and local development clusters. Building ARM64 images
ahead of time avoids runtime overhead from emulation layers.

  ----------------------- ----------------------- -----------------------
  **Platform**            **Use Case**            **ARM64 Benefit**

  Raspberry Pi 4/5        Edge, IoT, local dev    Native performance, no
                                                  QEMU slowdown

  AWS Graviton2/3         Cloud production        Up to 40% better
                          workloads               price-perf vs x86

  Apple Silicon Mac       Local container dev     Native execution for
                                                  M1/M2/M3 hosts
  ----------------------- ----------------------- -----------------------

**2. Environment Setup**

Before writing any code, ensure your Linux host has the required tools
installed and configured correctly.

**2.1 Installed Versions**

  ----------------------- ----------------------- -----------------------
  **Tool**                **Minimum Version**     **Check Command**

  Docker Engine           24.x (with Buildx       docker \--version
                          built-in)               

  Java (JDK)              21 (LTS)                java \--version

  Spring Boot             3.3.x                   See pom.xml /
                                                  build.gradle

  Maven or Gradle         3.9+ / 8.x              mvn \--version OR
                                                  gradle \--version
  ----------------------- ----------------------- -----------------------

**2.3 OFFTOPIC Enabling QEMU for ARM Emulation**

Docker Buildx uses QEMU under the hood to emulate ARM64 on your x86 host
during the build. Register QEMU binary formats with the kernel using the
following command:

+-----------------------------------------------------------------------+
| \# Register QEMU handlers for ARM64 emulation                         |
|                                                                       |
| docker run \--privileged \--rm tonistiigi/binfmt \--install arm64     |
|                                                                       |
| \# Verify arm64 is listed                                             |
|                                                                       |
| docker buildx ls                                                      |
+-----------------------------------------------------------------------+

+-----------------------------------------------------------------------+
| **✔ Tip: Persistent QEMU Setup**                                      |
|                                                                       |
| The binfmt registration above persists across reboots on most modern  |
| Linux distributions (using systemd-binfmt). On bare-metal servers,    |
| you may need to re-run it after kernel updates.                       |
+-----------------------------------------------------------------------+

**2.4 Creating a Buildx Builder**

The default Docker builder does not support multi-platform builds.
Create a dedicated builder that uses the docker-container driver:

+-----------------------------------------------------------------------+
| \# Create a new builder instance                                      |
|                                                                       |
| docker buildx create \--name arm64-builder \--driver docker-container |
| \--bootstrap                                                          |
|                                                                       |
| \# Set it as the active builder                                       |
|                                                                       |
| docker buildx use arm64-builder                                       |
|                                                                       |
| \# Inspect the builder to confirm arm64 support                       |
|                                                                       |
| docker buildx inspect \--bootstrap                                    |
+-----------------------------------------------------------------------+

You should see linux/arm64 listed under the Platforms column in the
inspect output.

**3. Creating the Spring Boot Application**

**3.1 Generating the Project**

Use Spring Initializr (start.spring.io) or the Spring CLI to generate a
new project. For this tutorial we use Maven with Java 21:

+-----------------------------------------------------------------------+
| \# Using the Spring CLI (optional)                                    |
|                                                                       |
| curl -s \"https://start.spring.io/starter.tgz\" \\                    |
|                                                                       |
| -d type=maven-project \\                                              |
|                                                                       |
| -d language=java \\                                                   |
|                                                                       |
| -d bootVersion=3.3.4 \\                                               |
|                                                                       |
| -d javaVersion=21 \\                                                  |
|                                                                       |
| -d dependencies=web,actuator \\                                       |
|                                                                       |
| -d name=demo \\                                                       |
|                                                                       |
| -d artifactId=demo \\                                                 |
|                                                                       |
| \| tar -xzvf -                                                        |
+-----------------------------------------------------------------------+

**3.2 Sample Application**

The tutorial application exposes a simple REST endpoint. The key file is
DemoApplication.java:

+-----------------------------------------------------------------------+
| package com.example.demo;                                             |
|                                                                       |
| import org.springframework.boot.SpringApplication;                    |
|                                                                       |
| import org.springframework.boot.autoconfigure.SpringBootApplication;  |
|                                                                       |
| import org.springframework.web.bind.annotation.GetMapping;            |
|                                                                       |
| import org.springframework.web.bind.annotation.RestController;        |
|                                                                       |
| \@SpringBootApplication                                               |
|                                                                       |
| \@RestController                                                      |
|                                                                       |
| public class DemoApplication {                                        |
|                                                                       |
| public static void main(String\[\] args) {                            |
|                                                                       |
| SpringApplication.run(DemoApplication.class, args);                   |
|                                                                       |
| }                                                                     |
|                                                                       |
| \@GetMapping(\"/\")                                                   |
|                                                                       |
| public String hello() {                                               |
|                                                                       |
| return \"Hello from ARM64!\";                                         |
|                                                                       |
| }                                                                     |
|                                                                       |
| }                                                                     |
+-----------------------------------------------------------------------+

**3.3 Building the JAR**

Package the application into an executable JAR before writing the
Dockerfile. Spring Boot Maven plugin produces a fat JAR containing all
dependencies:

+-----------------------------------------------------------------------+
| \# Build the JAR (skip tests for speed during this tutorial)          |
|                                                                       |
| mvn clean package -DskipTests                                         |
|                                                                       |
| \# The output will be at:                                             |
|                                                                       |
| \# target/demo-0.0.1-SNAPSHOT.jar                                     |
+-----------------------------------------------------------------------+

+-----------------------------------------------------------------------+
| **ℹ Spring Boot Layered JARs**                                        |
|                                                                       |
| Spring Boot 2.3+ produces layered JARs by default. This is critical   |
| for Docker image optimization because it separates dependencies,      |
| snapshot-dependencies, spring-boot-loader, and application code into  |
| distinct layers that can be cached independently by Docker.           |
+-----------------------------------------------------------------------+

**4. Writing the Dockerfile**

A well-structured multi-stage Dockerfile is essential for building
small, secure ARM64 images. We use a two-stage build: one stage to
extract layers, and one stage to assemble the final runtime image.

**4.1 Multi-Stage Dockerfile**

+-----------------------------------------------------------------------+
| \#                                                                    |
| ───────────────────────────────────────────────────────────────────── |
|                                                                       |
| \# Stage 1: Extract Spring Boot layers from the JAR                   |
|                                                                       |
| \#                                                                    |
| ───────────────────────────────────────────────────────────────────── |
|                                                                       |
| FROM eclipse-temurin:21-jre-jammy AS builder                          |
|                                                                       |
| WORKDIR /app                                                          |
|                                                                       |
| \# Copy the fat JAR produced by Maven                                 |
|                                                                       |
| COPY target/\*.jar application.jar                                    |
|                                                                       |
| \# Extract the layered JAR into separate directories                  |
|                                                                       |
| RUN java -Djarmode=layertools -jar application.jar extract            |
|                                                                       |
| \#                                                                    |
| ───────────────────────────────────────────────────────────────────── |
|                                                                       |
| \# Stage 2: Assemble the optimized runtime image                      |
|                                                                       |
| \#                                                                    |
| ───────────────────────────────────────────────────────────────────── |
|                                                                       |
| FROM eclipse-temurin:21-jre-jammy                                     |
|                                                                       |
| \# Create a non-root user for security                                |
|                                                                       |
| RUN groupadd \--system appgroup && useradd \--system \--gid appgroup  |
| appuser                                                               |
|                                                                       |
| WORKDIR /app                                                          |
|                                                                       |
| \# Copy layers in order (most stable first = better layer caching)    |
|                                                                       |
| COPY \--from=builder /app/dependencies/ ./                            |
|                                                                       |
| COPY \--from=builder /app/spring-boot-loader/ ./                      |
|                                                                       |
| COPY \--from=builder /app/snapshot-dependencies/ ./                   |
|                                                                       |
| COPY \--from=builder /app/application/ ./                             |
|                                                                       |
| \# Switch to non-root user                                            |
|                                                                       |
| USER appuser                                                          |
|                                                                       |
| \# Expose the default Spring Boot port                                |
|                                                                       |
| EXPOSE 8080                                                           |
|                                                                       |
| \# JVM flags optimized for containers                                 |
|                                                                       |
| ENV JAVA_OPTS=\"-XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0\"  |
|                                                                       |
| ENTRYPOINT \[\"java\", \"-cp\", \"BOOT-INF/lib/\*:.\",                |
| \"org.springframework.boot.loader.launch.JarLauncher\"\]              |
+-----------------------------------------------------------------------+

**4.2 Dockerfile Explained**

  ----------------------------------- -----------------------------------
  **Instruction**                     **Purpose**

  eclipse-temurin:21-jre-jammy        Slim JRE-only base image (no JDK)
                                      --- smaller than full JDK images

  jarmode=layertools extract          Splits the fat JAR into separate
                                      layer folders for cache-friendly
                                      COPY

  groupadd / useradd                  Creates a non-root system user ---
                                      security best practice

  COPY layers in order                Stable deps first so Docker cache
                                      hits on incremental code changes

  -XX:+UseContainerSupport            Tells JVM to respect container
                                      CPU/RAM limits instead of host
                                      limits

  -XX:MaxRAMPercentage=75.0           JVM uses up to 75% of container
                                      memory for heap
  ----------------------------------- -----------------------------------

**4.3 .dockerignore**

Add a .dockerignore file to prevent copying unnecessary files into the
build context, which speeds up the build:

+-----------------------------------------------------------------------+
| .git                                                                  |
|                                                                       |
| .github                                                               |
|                                                                       |
| \*.md                                                                 |
|                                                                       |
| target/\*.original                                                    |
|                                                                       |
| target/surefire-reports                                               |
|                                                                       |
| target/test-classes                                                   |
|                                                                       |
| \*\*/.DS_Store                                                        |
+-----------------------------------------------------------------------+

**5. Building the ARM64 Image**

**5.1 Build and Push to a Registry**

The most common workflow is to build for ARM64 and push directly to a
container registry such as Docker Hub or Amazon ECR. The \--platform
flag specifies the target architecture:

+-----------------------------------------------------------------------+
| \# Build for ARM64 and push to Docker Hub                             |
|                                                                       |
| docker buildx build \\                                                |
|                                                                       |
| \--platform linux/arm64 \\                                            |
|                                                                       |
| \--tag yourusername/spring-demo:latest \\                             |
|                                                                       |
| \--push \\                                                            |
|                                                                       |
| .                                                                     |
|                                                                       |
| \# Build for multiple platforms simultaneously (arm64 + amd64)        |
|                                                                       |
| docker buildx build \\                                                |
|                                                                       |
| \--platform linux/amd64,linux/arm64 \\                                |
|                                                                       |
| \--tag yourusername/spring-demo:latest \\                             |
|                                                                       |
| \--push \\                                                            |
|                                                                       |
| .                                                                     |
+-----------------------------------------------------------------------+

+-----------------------------------------------------------------------+
| **⚠ Important: \--push is Required for Multi-Platform Builds**        |
|                                                                       |
| Docker Buildx with multiple platforms cannot export to the local      |
| Docker daemon because the daemon can only store one architecture per  |
| image tag. You must push to a registry, or use \--load with a single  |
| platform.                                                             |
+-----------------------------------------------------------------------+

**5.2 Build and Load Locally (Single Platform)**

If you only want to test locally and do not need to push to a registry,
use \--load with a single platform:

+-----------------------------------------------------------------------+
| \# Build ARM64 and load into the local Docker daemon                  |
|                                                                       |
| docker buildx build \\                                                |
|                                                                       |
| \--platform linux/arm64 \\                                            |
|                                                                       |
| \--tag spring-demo:arm64 \\                                           |
|                                                                       |
| \--load \\                                                            |
|                                                                       |
| .                                                                     |
|                                                                       |
| \# Verify the image was created                                       |
|                                                                       |
| docker images spring-demo                                             |
|                                                                       |
| \# Inspect the architecture                                           |
|                                                                       |
| docker inspect spring-demo:arm64 \| grep Architecture                 |
+-----------------------------------------------------------------------+

**5.3 Running the ARM64 Image**

On your x86 Linux host, QEMU automatically handles the emulation when
you run an ARM64 container. On a native ARM64 device (Raspberry Pi,
Graviton), it runs directly:

+-----------------------------------------------------------------------+
| \# Run the container (QEMU emulation on x86, native on ARM64)         |
|                                                                       |
| docker run -d -p 8080:8080 \--name spring-demo spring-demo:arm64      |
|                                                                       |
| \# Test the endpoint                                                  |
|                                                                       |
| curl http://localhost:8080/                                           |
|                                                                       |
| \# Expected output:                                                   |
|                                                                       |
| \# Hello from ARM64!                                                  |
|                                                                       |
| \# View logs                                                          |
|                                                                       |
| docker logs spring-demo                                               |
+-----------------------------------------------------------------------+

**5.4 Verifying on AWS Graviton**

When you pull and run the image on an AWS Graviton (arm64) EC2 instance,
you can confirm it is running natively:

+-----------------------------------------------------------------------+
| \# On your Graviton EC2 instance                                      |
|                                                                       |
| uname -m                                                              |
|                                                                       |
| \# Expected: aarch64                                                  |
|                                                                       |
| \# Pull and run                                                       |
|                                                                       |
| docker pull yourusername/spring-demo:latest                           |
|                                                                       |
| docker run -d -p 8080:8080 yourusername/spring-demo:latest            |
|                                                                       |
| \# Check that no QEMU layer is present                                |
|                                                                       |
| docker inspect yourusername/spring-demo:latest \| grep Architecture   |
|                                                                       |
| \# Expected: \"Architecture\": \"arm64\"                              |
+-----------------------------------------------------------------------+

**5.5 Deploying to Raspberry Pi**

On a Raspberry Pi 4 or 5 running Raspberry Pi OS (64-bit) or Ubuntu
Server ARM64, the deployment is identical to any other ARM64 Linux host:

+-----------------------------------------------------------------------+
| \# On Raspberry Pi (64-bit OS required)                               |
|                                                                       |
| uname -m                                                              |
|                                                                       |
| \# Expected: aarch64                                                  |
|                                                                       |
| \# Pull the image from your registry                                  |
|                                                                       |
| docker pull yourusername/spring-demo:latest                           |
|                                                                       |
| \# Run with memory limit appropriate for Raspberry Pi                 |
|                                                                       |
| docker run -d \\                                                      |
|                                                                       |
| -p 8080:8080 \\                                                       |
|                                                                       |
| \--memory=512m \\                                                     |
|                                                                       |
| \--name spring-demo \\                                                |
|                                                                       |
| yourusername/spring-demo:latest                                       |
+-----------------------------------------------------------------------+

**6. Image Size Optimization**

Reducing image size improves pull times, reduces storage costs, and
shrinks the attack surface. The following techniques are ordered from
highest to lowest impact.

**6.1 Use JRE Instead of JDK**

The JDK includes a compiler, debugger, and tools not needed at runtime.
Switching from a JDK to a JRE base image typically saves 200-400 MB:

  ---------------------------------- ----------------------- -----------------------
  **Base Image**                     **Approx. Size**        **Recommendation**

  eclipse-temurin:21-jdk-jammy       \~450 MB                Development only

  eclipse-temurin:21-jre-jammy       \~250 MB                Recommended for
                                                             production

  eclipse-temurin:21-jre-alpine      \~170 MB                Smallest, musl libc
                                                             (test thoroughly)

  amazoncorretto:21-alpine3.19-jdk   \~200 MB                Good for Graviton,
                                                             AWS-optimized
  ---------------------------------- ----------------------- -----------------------

**6.2 Leverage Layer Caching**

The multi-stage Dockerfile in Section 4 already uses Spring Boot layer
extraction. The key insight is that dependency layers change far less
often than your application code. Docker reuses cached layers unless
those specific layers change:

+-----------------------------------------------------------------------+
| \# Layer order in the Dockerfile (most stable first):                 |
|                                                                       |
| COPY \--from=builder /app/dependencies/ \# 3rd-party libs - rarely    |
| changes                                                               |
|                                                                       |
| COPY \--from=builder /app/spring-boot-loader/ \# Spring loader -      |
| rarely changes                                                        |
|                                                                       |
| COPY \--from=builder /app/snapshot-dependencies/ \# SNAPSHOT libs -   |
| changes sometimes                                                     |
|                                                                       |
| COPY \--from=builder /app/application/ \# Your code - changes often   |
|                                                                       |
| \# Result: only the last 1-2 layers are invalidated on code changes   |
|                                                                       |
| \# instead of rebuilding the entire image                             |
+-----------------------------------------------------------------------+

**6.3 Using Alpine-Based Images**

Alpine Linux images are significantly smaller than Ubuntu/Debian-based
images. However, Alpine uses musl libc instead of glibc, which can cause
issues with some Java native libraries. Always test thoroughly before
using Alpine in production:

+-----------------------------------------------------------------------+
| \# Replace the base image in Stage 2 with Alpine                      |
|                                                                       |
| FROM eclipse-temurin:21-jre-alpine                                    |
|                                                                       |
| \# Some apps may need gcompat for glibc compatibility                 |
|                                                                       |
| RUN apk add \--no-cache gcompat                                       |
+-----------------------------------------------------------------------+

**6.4 Custom JRE with jlink**

For the smallest possible image, use jlink to create a custom JRE
containing only the modules your application actually needs. This can
reduce the JRE size from \~250 MB to under 80 MB:

+-----------------------------------------------------------------------+
| FROM eclipse-temurin:21-jdk-jammy AS jre-builder                      |
|                                                                       |
| \# Analyze your JAR\'s module dependencies                            |
|                                                                       |
| RUN jdeps \--ignore-missing-deps \\                                   |
|                                                                       |
| \--print-module-deps \\                                               |
|                                                                       |
| \--multi-release 21 \\                                                |
|                                                                       |
| application.jar \> modules.txt                                        |
|                                                                       |
| \# Create a minimal custom JRE                                        |
|                                                                       |
| RUN jlink \\                                                          |
|                                                                       |
| \--add-modules \$(cat modules.txt) \\                                 |
|                                                                       |
| \--strip-debug \\                                                     |
|                                                                       |
| \--no-man-pages \\                                                    |
|                                                                       |
| \--no-header-files \\                                                 |
|                                                                       |
| \--compress=2 \\                                                      |
|                                                                       |
| \--output /custom-jre                                                 |
|                                                                       |
| \# Final stage: use the custom JRE                                    |
|                                                                       |
| FROM debian:bookworm-slim                                             |
|                                                                       |
| COPY \--from=jre-builder /custom-jre /opt/jre                         |
|                                                                       |
| ENV PATH=\"/opt/jre/bin:\$PATH\"                                      |
+-----------------------------------------------------------------------+

**6.5 Size Comparison Summary**

  -------------------------------- ----------------------- -----------------------
  **Optimization Strategy**        **Approximate Image     **Complexity**
                                   Size**                  

  JDK base (no optimization)       \~480 MB                Low

  JRE base                         \~270 MB                Low
  (eclipse-temurin:21-jre-jammy)                           

  JRE + layered JAR caching        \~270 MB (faster        Low
                                   builds)                 

  JRE Alpine base                  \~180 MB                Medium

  Custom jlink JRE + distroless    \~90-120 MB             High
  -------------------------------- ----------------------- -----------------------

**7. Troubleshooting**

**7.1 Common Issues**

  -------------------------------- ----------------------- -----------------------
  **Error / Symptom**              **Likely Cause**        **Solution**

  exec format error when running   Image built for wrong   Rebuild with
  container                        arch                    \--platform linux/arm64

  \"multiple platforms\" error     Limitation of local     Use \--push or specify
  with \--load                     daemon                  single \--platform

  Build is very slow (QEMU         Full emulation of ARM64 Normal for first build;
  emulation)                       on x86                  use cache for
                                                           subsequent builds

  java.lang.UnsatisfiedLinkError   musl vs glibc native    Add gcompat or switch
  on Alpine                        lib conflict            to jammy/debian base

  Container OOMKilled on Raspberry JVM heap too large      Set
  Pi                                                       -XX:MaxRAMPercentage
                                                           and \--memory on docker
                                                           run

  binfmt: cannot execute binary    QEMU not registered     Re-run: docker run
                                                           \--privileged \--rm
                                                           tonistiigi/binfmt
                                                           \--install arm64
  -------------------------------- ----------------------- -----------------------

**7.2 Inspecting the Built Image**

+-----------------------------------------------------------------------+
| \# Check the OS and architecture of the image                         |
|                                                                       |
| docker inspect spring-demo:arm64 \| grep -E \'Architecture\|Os\'      |
|                                                                       |
| \# Analyze image layer sizes                                          |
|                                                                       |
| docker history spring-demo:arm64                                      |
|                                                                       |
| \# Dive tool for interactive layer inspection (install separately)    |
|                                                                       |
| dive spring-demo:arm64                                                |
+-----------------------------------------------------------------------+

**8. Summary and Next Steps**

You have learned how to build a production-ready ARM64 Docker image for
a Spring Boot application from an x86 Linux host. Here is a recap of the
key steps:

1.  Installed Docker with Buildx and registered QEMU for ARM64 emulation

2.  Created a dedicated Buildx builder with the docker-container driver

3.  Packaged a Spring Boot application into a layered fat JAR with Maven

4.  Wrote a multi-stage Dockerfile using JRE-only base images and layer
    extraction

5.  Built and pushed an ARM64 image using docker buildx build
    \--platform linux/arm64

6.  Applied image size optimizations including JRE selection, layer
    caching, and jlink

**8.1 Recommended Next Steps**

- Integrate the docker buildx build command into a CI/CD pipeline
  (GitHub Actions, GitLab CI)

- Explore Buildkit cache mounts to share Maven local repository across
  builds

- Investigate GraalVM native-image for sub-second startup times and even
  smaller images

- Use multi-platform manifests (linux/amd64 + linux/arm64) for
  transparent deployment across architectures

- Set up Amazon ECR or GitHub Container Registry as your private image
  registry

+-----------------------------------------------------------------------+
| **★ Going Further: GraalVM Native Image**                             |
|                                                                       |
| Spring Boot 3.x has first-class support for compiling to a GraalVM    |
| native executable. Native images start in milliseconds and consume    |
| far less memory than JVM-based containers. They are an excellent fit  |
| for ARM64 edge devices. See the Spring Boot Native documentation for  |
| details.                                                              |
+-----------------------------------------------------------------------+

**Appendix: Quick Reference**

**Key Commands**

+-----------------------------------------------------------------------+
| \# Setup                                                              |
|                                                                       |
| docker run \--privileged \--rm tonistiigi/binfmt \--install arm64     |
|                                                                       |
| docker buildx create \--name arm64-builder \--driver docker-container |
| \--bootstrap                                                          |
|                                                                       |
| docker buildx use arm64-builder                                       |
|                                                                       |
| \# Build                                                              |
|                                                                       |
| mvn clean package -DskipTests                                         |
|                                                                       |
| \# Build & push ARM64 image                                           |
|                                                                       |
| docker buildx build \--platform linux/arm64 \--tag user/app:latest    |
| \--push .                                                             |
|                                                                       |
| \# Build & push multi-arch image                                      |
|                                                                       |
| docker buildx build \--platform linux/amd64,linux/arm64 \--tag        |
| user/app:latest \--push .                                             |
|                                                                       |
| \# Load locally (single platform only)                                |
|                                                                       |
| docker buildx build \--platform linux/arm64 \--tag app:arm64 \--load  |
| .                                                                     |
|                                                                       |
| \# Verify architecture                                                |
|                                                                       |
| docker inspect app:arm64 \| grep Architecture                         |
+-----------------------------------------------------------------------+

**Recommended Base Images for ARM64 + Java**

  ------------------------------- ----------------------- -----------------------
  **Image**                       **Size**                **Notes**

  eclipse-temurin:21-jre-jammy    \~250 MB                Best general-purpose
                                                          choice

  eclipse-temurin:21-jre-alpine   \~170 MB                Smallest; test native
                                                          libs

  amazoncorretto:21-alpine3.19    \~200 MB                AWS-optimized; good for
                                                          Graviton

  azul/zulu-openjdk:21-jre        \~220 MB                Azul Zulu,
                                                          well-maintained
  ------------------------------- ----------------------- -----------------------
