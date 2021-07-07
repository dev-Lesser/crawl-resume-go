FROM golang:alpine AS builder

ENV GO111MODULE=on \
    CGO_ENABLED=0 \
    GOOS=linux \
    GOARCH=amd64

WORKDIR /build
COPY go.mod crawl-resume.go ./
RUN go mod download
RUN go build -o main crawl-resume.go
WORKDIR /dist
RUN cp /build/main .
RUN mkdir /build/data

FROM scratch
COPY --from=builder /dist/main .
ENTRYPOINT ["/main"]