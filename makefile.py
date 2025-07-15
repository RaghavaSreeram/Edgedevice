# Makefile for Re-Play EdgeDevice

install:
	./install.sh

start:
	sudo systemctl start edge-core.service

stop:
	sudo systemctl stop edge-core.service

restart:
	sudo systemctl restart edge-core.service

status:
	sudo systemctl status edge-core.service

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

update:
	python3 ota_updater.py

logs:
	journalctl -u edge-core.service -f
