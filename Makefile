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
		docker rmi karimtabet/papusa

acceptance_test:
		echo "Running test script"
		sleep 20
		./acceptance_test.sh

test: build start acceptance_test clean

release:
		echo "Pushing to Docker Hub"
		./release.sh
