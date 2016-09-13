# Additive Manufacturing Processing Ontology
AMPO(Additive Manufacturing Processing Ontology) Faceted Search using ElasticSearch

Please check out the ontology Cmap [here]( https://cmapscloud.ihmc.us:443/rid=1Q2LYB6N7-HKDXKF-82/AMOnto_v1.7.cmap).

Please check out the live demo of the faceted browsers here:

https://dofamp.tw.rpi.edu/equipment.html

https://dofamp.tw.rpi.edu/material.html

## Installation

To log in the server:
`$ ssh -l <username> -p 2229 dofamp.tw.rpi.edu`

The location of apache2 config file:
`/etc/apache2/sites-enabled/000-default.conf`

To run Elasticsearch as a service:
https://www.elastic.co/guide/en/elasticsearch/reference/current/setup-service.html

Front end for ElasticSearch search indices:
https://github.com/CottageLabs/facetview2

Another web front end for an Elasticsearch cluster:
https://github.com/mobz/elasticsearch-head

Version 1.7.0 DEB package was used. It is available [here](https://www.elastic.co/downloads/past-releases/elasticsearch-1-7-0).

1. Install Elasticsearch 1.7.0: 
  `$ sudo dpkg -i elasticsearch-1.7.0.deb`

   List files installed to the system from the DEB package: 
  `$ dpkg -L elasticsearch`

2. Modify the config file located here:
  ` /etc/elasticsearch/elasticsearch.yml`

3. Install elasticsearch-head:
   ```
   $ sudo /usr/share/elasticsearch/bin/plugin -install mobz/elasticsearch-head/1.x
   ```

4. Run Elasticsearch as a service on the server:
   ```
    $ sudo update-rc.d elasticsearch defaults 95 10
    $ sudo /etc/init.d/elasticsearch start
   ```

