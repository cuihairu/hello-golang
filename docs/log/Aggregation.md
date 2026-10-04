### 日志聚合与集中管理

服务一多，日志就散在各台机器上，出了事得逐台 `ssh` 翻文件。日志聚合把各处的日志收拢到一个地方统一存储和检索，查问题、看监控都在一处完成。

#### 1. 日志聚合与集中管理的概念

- **日志聚合**：将分布在不同服务器或应用实例中的日志收集到集中存储和管理系统中。
- **集中管理**：对聚合后的日志进行统一存储、检索、分析和可视化。

#### 2. 常用工具和技术

##### 2.1 `fluentd`

`fluentd` 是一个开源的数据收集器，输入输出都靠插件对接，收上来的日志可以先过滤、缓冲，再转发到指定位置。

###### 安装与配置

```sh
# 安装 fluentd
gem install fluentd

# 创建配置文件
fluentd --setup ./fluent
```

###### 配置示例

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

`logstash` 是 Elastic Stack 中的数据收集和处理引擎，能够处理不同格式的数据，并将其发送到 Elasticsearch 进行存储和分析。

###### 安装与配置

```sh
# 下载并安装 logstash
wget https://artifacts.elastic.co/downloads/logstash/logstash-7.14.0.tar.gz
tar -xzf logstash-7.14.0.tar.gz
cd logstash-7.14.0

# 创建配置文件
vim logstash.conf
```

###### 配置示例

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

Elastic Stack 由 Elasticsearch、Logstash 和 Kibana 三件套组成：Logstash 负责收集和加工，Elasticsearch 负责存储和检索，Kibana 负责查询和出图。

###### 安装与配置

```sh
# 安装 Elasticsearch
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.14.0-linux-x86_64.tar.gz
tar -xzf elasticsearch-7.14.0-linux-x86_64.tar.gz
cd elasticsearch-7.14.0
./bin/elasticsearch

# 安装 Kibana
wget https://artifacts.elastic.co/downloads/kibana/kibana-7.14.0-linux-x86_64.tar.gz
tar -xzf kibana-7.14.0-linux-x86_64.tar.gz
cd kibana-7.14.0-linux-x86_64
./bin/kibana

# 使用上面的 logstash.conf 配置 Logstash
```

##### 2.4 云日志服务

- **AWS CloudWatch**：提供日志收集、存储和分析服务，支持自动化监控和警报。
- **Google Stackdriver**：提供日志收集和分析服务，集成了 Google Cloud 平台的监控工具。

#### 3. 日志聚合与集中管理的实现

##### 3.1 配置日志输出

在应用程序中配置日志输出到 `fluentd` 或 `logstash`。

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

##### 3.2 配置 Logstash 输入

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

##### 3.3 可视化和分析

通过 Kibana 配置和使用仪表板，可视化和分析日志数据。

###### 创建索引模式

1. 打开 Kibana 并导航到 “管理” 页面。
2. 在 “索引模式” 下，创建新的索引模式 `logstash-*`。

###### 创建仪表板

1. 在 Kibana 中导航到 “可视化” 页面。
2. 使用创建的索引模式，添加图表、表格和其他可视化组件。
3. 组合多个可视化组件创建仪表板，用于实时监控和分析日志数据。

#### 4. 日志聚合与集中管理的最佳实践

- **标准化日志格式**：使用一致的日志格式，便于日志的解析和分析。
- **集中管理**：将日志集中存储和管理，便于统一分析和监控。
- **自动化**：使用自动化工具和脚本进行日志收集和处理，减少人工操作。
- **安全性**：确保日志数据的安全传输和存储，保护敏感信息。
- **性能优化**：在高并发场景下，优化日志收集和处理的性能，避免影响应用程序的正常运行。
