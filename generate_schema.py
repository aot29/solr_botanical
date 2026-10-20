import csv, json

with open("herbarium/herbarium_benchmark.csv", encoding="utf-8") as f:
    header = next(csv.reader(f, delimiter=";"))

def ftype(name):
    n = name.strip().lower()
    if n.startswith("verbatim"): return "string"          # unparsed originals
    if "date" in n: return "pdate"
    if n in ("year","month","day"): return "pint"
    if "latitude" in n or "longitude" in n: return "pdouble"
    if n in ("scientificname","locality","occurrenceremarks","recordedby"):
        return "text_general"
    return "string"

fields = [{"name":c.strip(),"type":ftype(c),"multiValued":False} for c in header if c.strip()]
json.dump({"add-field": fields}, open("schema.json","w"), indent=2)
print(f"{len(fields)} fields written")
