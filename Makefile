.PHONY: build start

build:
		echo "Building images with Docker Compose"
		docker-compose build

start:
		echo "Starting containers with Docker Compose"
		docker-compose up -d

clean:
		echo "Cleaning up papusa services"
		docker rm -f papusa_nginx papusa_web papusa_redis papusa_db

test: build start
		echo "Running test script"
		./test.sh
