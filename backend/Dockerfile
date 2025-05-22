# Use an official Go runtime as a parent image
FROM golang:1.22-alpine

# Set the working directory in the container
WORKDIR /app

# Copy go.mod and go.sum files
COPY go.mod ./
# Assuming go.sum will be generated or copied if it exists. If not, `go mod download` will create it.
# COPY go.sum ./ 

# Download Go modules
RUN go mod download && go mod verify

# Copy the rest of the application source code
COPY . .

# Build the Go application
# The output binary will be named 'main' and placed in /app
RUN go build -o /app/main .

# Command to run the executable
CMD ["/app/main"]
