# solr_botanical

First time
```
docker run -d -p 8983:8983 --name solr solr solr-precreate herbarium
```

Generate the schema:
`python generate_schema.py`
Then upload it
```
curl -X POST -H "Content-Type: application/json" \
  "http://localhost:8983/solr/herbarium/config" \
  -d '{"set-user-property":{"update.autoCreateFields":"false"}}'

curl -X POST -H "Content-Type: application/json" \
  "http://localhost:8983/solr/herbarium/schema" -d @schema.json

curl "http://localhost:8983/solr/herbarium/update/csv?commit=true&header=true" --data-binary @./herbarium/herbarium-benchmark.csv -H "Content-Type: text/plain"

```

Add full-text search
```
# 1. create the catch-all field
curl -X POST -H "Content-Type: application/json" \
  "http://localhost:8983/solr/herbarium/schema" \
  -d '{"add-field":{"name":"text_search","type":"text_general","multiValued":true}}'

# 2. wire the sources into it
curl -X POST -H "Content-Type: application/json" \
  "http://localhost:8983/solr/herbarium/schema" \
  -d '{
    "add-copy-field":[
      {"source":"scientificName","dest":"text_search"},
      {"source":"locality","dest":"text_search"},
      {"source":"verbatimLocality","dest":"text_search"},
      {"source":"recordedBy","dest":"text_search"}
    ]
  }'

# 3. re-index (copy-fields are applied at indexing time, not query time!)
curl "http://localhost:8983/solr/herbarium/update/csv?commit=true&header=true" \
  --data-binary @./herbarium/herbarium-benchmark.csv -H "Content-Type: text/plain"
```

Check the import
```
# how much landed?
curl "http://localhost:8983/solr/herbarium/select?q=*:*&rows=0"

# and a first real query – specimens from a date range:
curl -g "http://localhost:8983/solr/herbarium/select?q=eventDate:[2000-01-01T00:00:00Z+TO+2010-12-31T23:59:59Z]&rows=3&wt=json"

# or a full-text search (if you set up text_search):
curl "http://localhost:8983/solr/herbarium/select?q=text_search:Abelia&rows=3"
```

FRom now on
```
docker compose up -d
http://localhost:8983/
```


## References
Dillen Mathias. (2018). A benchmark dataset of herbarium specimen images with label data: Summary [Dataset]. Zenodo. https://doi.org/10.5281/zenodo.6372393

