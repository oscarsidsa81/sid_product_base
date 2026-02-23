{
    "name" : "sid_product_base",
    "version" : "15.0.1.0.0",
    "category" : "Inventory",
    "author" : "oscarsidsa81",
    "website" : "http://www.sidsaindustrial.com",
    "license" : "AGPL-3",
    "summary" : "Módulo de inclusión de pasillos y ubicaciones en stock",
    "depends" : ["product","stock"],
    "data" : [
        "security/ir.model.access.csv",
        "views/sid_location_views.xml",
        "data/sid_location_data.xml"
    ],
    "installable" : True,
    "application" : False
}
