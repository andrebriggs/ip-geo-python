# Azure Log Analytics to IP to Geo

This is a simple example of how to get more accurate location data from Azure Montior's [Log Analytics](https://docs.microsoft.com/en-us/azure/azure-monitor/log-query/log-query-overview) using [GeoIP2](https://github.com/maxmind/GeoIP2-python).

## Requirements
* A GeoLite2 database. You can download a database [here](https://dev.maxmind.com/geoip/geoip2/geolite)
* A CSV with a list of IP addresses (IPv4 and IPv6 supported)

You can the Log Analytics feature in Azure Monitor to perform a query that can return IP addresses of requests amongst other metadata. Queries use the [Kusto](https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/) langauge.

## Thinking about Privacy Preservation

Ideally, it woudl be great is features like Log Analytics could be HIPAA 


Run 
```console
$ python geo_from_ip.py 
```