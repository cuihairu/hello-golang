### Log Aggregation and Centralized Management

Once there are many services, logs scatter across machines, and when something breaks you have to `ssh` onto each box and dig through files one by one. Log aggregation collects the logs from everywhere into a single place for unified storage and search, so investigation and monitoring happen in one spot.

#### 1. Concepts of Log Aggregation and Centralized Management

- **Log aggregation**: collect logs distributed across different servers or application instances into a centralized storage and management system.
- **Centralized management**: unified storage, search, analysis and visualization of the aggregated logs.

#### 2. Common Tools and Techniques

##### 2.1 `fluentd`

`fluentd` is an open-source data collector whose inputs and outputs are wired up with plugins. Collected logs can be filtered and buffered first, then forwarded to the target destination.

###### Installation and Configuration

```sh
# install fluentd
gem install fluentd

# create the configuration file
fluentd --setup ./fluent
```

###### Configuration Example

`fluent.conf`:

```plaintext
<source>
  @type forward
  port 24224
</source>

<match **>
  @type stdout
</match>
```

##### 2.2 `logstash`

`logstash` is the data collection and processing engine in the Elastic Stack; it can handle data in different formats and send it to Elasticsearch for storage and analysis.

###### Installation and Configuration

```sh
# download and install logstash
wget https://artifacts.elastic.co/downloads/logstash/logstash-7.14.0-linux-x86_64.tar.gz
tar -xzf logstash-7.14.0-linux-x86_64.tar.gz
cd logstash-7.14.0

# create the configuration file
vim logstash.conf
```

###### Configuration Example

`logstash.conf`:

```plaintext
input {
  file {
    path => "/var/log/*.log"
    start_position => "beginning"
  }
}

output {
  elasticsearch {
    hosts => ["localhost:9200"]
    index => "logstash-%{+YYYY.MM.dd}"
  }
}
```

##### 2.3 `Elastic Stack (ELK)`

The Elastic Stack is made up of three pieces: Elasticsearch, Logstash and Kibana. Logstash collects and processes, Elasticsearch stores and indexes for search, and Kibana does the querying and the visualizations.

###### Installation and Configuration

```sh
# install Elasticsearch
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.14.0-linux-x86_64.tar.gz
tar -xzf elasticsearch-7.14.0-linux-x86_64.tar.gz
cd elasticsearch-7.14.0
./bin/elasticsearch

# install Kibana
wget https://artifacts.elastic.co/downloads/kibana/kibana-7.14.0-linux-x86_64.tar.gz
tar -xzf kibana-7.14.0-linux-x86_64.tar.gz
cd kibana-7.14.0-linux-x86_64
./bin/kibana

# configure Logstash with the logstash.conf above
```

##### 2.4 Cloud Log Services

- **AWS CloudWatch**: provides log collection, storage and analysis, with automated monitoring and alerting.
- **Google Stackdriver**: provides log collection and analysis, integrated with the Google Cloud Platform monitoring toolset.

#### 3. Implementing Log Aggregation and Centralized Management

##### 3.1 Configuring Log Output

Configure the application to send logs to `fluentd` or `logstash`.

```go
package main

import (
	"github.com/sirupsen/logrus"
	"github.com/fluent/fluent-logger-golang/fluent"
)

func main() {
	logger := logrus.New()

	fluentConfig := fluent.Config{
		FluentHost: "localhost",
		FluentPort: 24224,
	}

	fluentLogger, err := fluent.New(fluentConfig)
	if err != nil {
		logger.Fatal(err)
	}

	logger.Hooks.Add(fluentHook{fluentLogger})
	logger.Info("This is a log message sent to Fluentd")
}

type fluentHook struct {
	*fluent.Fluent
}

func (hook fluentHook) Levels() []logrus.Level {
	return logrus.AllLevels
}

func (hook fluentHook) Fire(entry *logrus.Entry) error {
	data := make(map[string]interface{})
	for k, v := range entry.Data {
		data[k] = v
	}
	data["message"] = entry.Message
	data["level"] = entry.Level.String()
	data["time"] = entry.Time

	tag := "app.log"
	return hook.Post(tag, data)
}
```

##### 3.2 Configuring Logstash Input

`logstash.conf`:

```plaintext
input {
  tcp {
    port => 5000
    codec => json_lines
  }
}

output {
  elasticsearch {
    hosts => ["localhost:9200"]
    index => "logstash-%{+YYYY.MM.dd}"
  }
}
```

##### 3.3 Visualization and Analysis

Use Kibana dashboards to visualize and analyze the log data.

###### Creating an Index Pattern

1. Open Kibana and navigate to the "Management" page.
2. Under "Index Patterns", create a new index pattern `logstash-*`.

###### Creating a Dashboard

1. Navigate to the "Visualization" page in Kibana.
2. Using the index pattern you created, add charts, tables and other visualization components.
3. Combine multiple visualization components into a dashboard for real-time monitoring and analysis of the log data.

#### 4. Best Practices for Log Aggregation and Centralized Management

- **Standardize the log format**: use a consistent log format so logs are easier to parse and analyze.
- **Centralized management**: store and manage logs centrally to enable unified analysis and monitoring.
- **Automation**: use automated tools and scripts for log collection and processing to cut down on manual work.
- **Security**: ensure log data is transmitted and stored securely, protecting sensitive information.
- **Performance optimization**: under high concurrency, optimize log collection and processing so that it does not disturb the application's normal operation.

## References

- [log standard library](https://pkg.go.dev/log)
- [Official blog · Structured Logging with slog](https://go.dev/blog/slog)

## Sibling pages

- [LibLog](/log/LibLog.md)
- [Log](/log/Log.md)
- [ModLog](/log/ModLog.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [LibLog](/log/LibLog.md)
- [Log](/log/Log.md)
- [ModLog](/log/ModLog.md)
