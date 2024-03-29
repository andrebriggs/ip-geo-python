# Azure Log Analytics to IP to Geo

This is a simple example of how to get more accurate location data from Azure Monitor's [Log Analytics](https://docs.microsoft.com/en-us/azure/azure-monitor/log-query/log-query-overview) using [GeoIP2](https://github.com/maxmind/GeoIP2-python). The use of Azure Monitor isn't required, any list of IP addresses will work.

## Requirements

* A GeoLite2 database. You can download a database [here](https://dev.maxmind.com/geoip/geoip2/geolite)
* A CSV with a list of IP addresses (IPv4 and IPv6 supported)

## Use a Kusto Query (optional)

You can use Log Analytics feature in Azure Monitor to perform a query that can return IP addresses. Queries use the [Kusto](https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/) langauge.

An example Kusto query that pulls 12 hours of distinct request IP addresses from an Azure CDN instance is below. Queries can be performed from the Azure Portal or programmatically.

```code
AzureDiagnostics
| where TimeGenerated >= now(-12h)
| where OperationName == "Microsoft.Cdn/Profiles/AccessLog/Write" and Category == "AzureCdnAccessLog"
| where isReceivedFromClient_b == true
| distinct clientIp_s
```


## Running the code
Create a virtual environment and install requirements via `pip`.

```console
$ python3 -m venv env`
$ pip install -r requirements.txt`
```

Run 
```console
$ python geo_from_ip.py (path to IP CSV) (path to Database file)
```

## Example of output
```csv
country_code,sub_division,ip_count
US,New Jersey,980
US,Massachusetts,5
KR,Seoul,3
AU,Victoria,1
HK,Sha Tin,1
IN,Maharashtra,1
KR,Gyeonggi-do,1
TH,Bangkok,1
TW,Taichung City,1
TW,Taipei City,1
```

## Thinking about Privacy Preservation

Apparently Log Analytics is [HIPAA compliant](https://azure.microsoft.com/mediahandler/files/resourcefiles/microsoft-azure-compliance-offerings/Microsoft%20Azure%20Compliance%20Offerings.pdf) in the Azure Public and Government Clouds. In this example we are getting data from Azure CDN via Azure Monitor Log Analytics. When clients connect to on a CDN, they should know the privacy policy. If Log Analytics provided an option to disable [IP address](https://docs.microsoft.com/en-us/azure/cdn/enable-raw-logs#raw-logs-properties) logging or at least provide a less privileged view of the log data the privacy posture would be improved. This is especially true for fields such as Healthcare.
