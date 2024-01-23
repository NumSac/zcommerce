# Start from the official Golang base image for the build stage
FROM golang:1.18 as builder

# Set the current working directory inside the container
WORKDIR /app

# Copy go.mod and go.sum if you are using Go modules
COPY go.mod go.sum ./
# Download all dependencies. Dependencies will be cached if the go.mod and go.sum files are not changed
RUN go mod download

# Copy the source code into the container
COPY . .

# Build the Go app as a static binary (without C dependencies)
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main .

# Start from a small base image for the final stage
FROM alpine:latest  

# Add certificates for SSL
RUN apk --no-cache add ca-certificates

# Set the working directory
WORKDIR /root/

# Copy the pre-built binary from the previous stage
COPY --from=builder /app/main .

# Expose the port the app runs on
EXPOSE 8080

# Command to run the executable
CMD ["./main"]
