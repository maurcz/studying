# Prometheus and Grafana

Basics on how to connect Prometheus to Grafana

- Prometheus basic guide: https://prometheus.io/docs/prometheus/latest/getting_started/
- Grafana installation guide: https://grafana.com/docs/grafana/latest/setup-grafana/installation/debian/
- Connecting Prometheus to Grafana: https://prometheus.io/docs/visualization/grafana/

## Running

Extract the all binaries from `./binaries/` using `tar -xvfz` (use `sudo` for granafa). Then run the following commands:

```
# Prometheus Folder
./prometheus --config.file=../../prometheus.yaml

# Node Export Folder
./node_exporter --web.listen-address 127.0.0.1:8080
./node_exporter --web.listen-address 127.0.0.1:8081
./node_exporter --web.listen-address 127.0.0.1:8082

# Grafana
sudo ./bin/grafana-server web
```

Follow the steps from [this](https://prometheus.io/docs/visualization/grafana/) guide to connect prometheus to grafana.

The `prometheus.yaml` has configs to allow this to be used in grafana dashboards: `job_instance_mode:node_cpu_seconds:avg_rate5m`.

## Map

The steps above will run Prometheus locally and export two sets of metrics: prometheus metrics and OS metrics using Node Explorer. We then connect Prometheus to Grafana, allowing any Prometheus query to be transformed into Grafana dashboards.

I made copies of the binaries just in case the websites are taken down, so that the installation steps above can be reproduced.

## Resources:

List of prometheus exporters: https://prometheus.io/docs/instrumenting/exporters/
Creating new exporters: https://prometheus.io/docs/instrumenting/writing_exporters/ .

