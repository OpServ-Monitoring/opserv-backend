---
layout: doc-entry
title:  "RESTful API"
---

The frontend utilizes a RESTful-API to retrieve historical and real-time data from the backend as well as to persist the users preferences.

All endpoints are available under subpaths of `/api`

To separate user data from the gathered data there are distinct endpoints for both of them, each defining their own versions as well. 

# General response structure

In general each response from the RESTful api consists of a data and a links section. The data section varies depending on the requested resource. To get more details about the data section read the documentation of the specific endpoint. The links section includes different references based on the requested endpoint, namely a self-reference and if possible a reference to the direct parent and references to any child resources. 

Each reference consists of a hyperlink and a name identifying the resource type. Please note that the name does not represent the resource itself but the type of the resource, thus there can be mutiple references with the same name but different hyperlinks.

### reference example

    {
        "href": "https://adress:port/api/path",
        "name": "demo endpoint"
    }

### complete response example

    {
        "data": {
            ...
        },
        "links": {
            "self": {
                "href": "https://adress:port/api/path", 
                "name": "demo endpoint"
            },
            "parent": {
                "href": "https://adress:port/api", 
                "name": "demo api root"
            },
            "children": [
                {"href": "https://adress:port/api/path/subpath-1", "name": "demo endpoint child"},
                ...
                {"href": "https://adress:port/api/path/subpath-n", "name": "demo endpoint child"}
            ]
        }
    }

# Gathered data

All endpoints to the data api are available under subpaths of `/api` followed by `/data` and the api version, e.g. `/api/data/v1`. To always use the last version exchange the version code with the keyword _current_ as such `/api/data/current`

See the belonging references for more details to each version:
+ [data - version 1](https://github.com/OpServ-Monitoring/opserv-backend/wiki/RESTful-API-reference:-data-v1)

#User preferences

Similar to the data api, all endpoints to the preferences api are available under subpaths of `/api` followed by `/preferences` and the api version, e.g. `/api/preferences/v1`. To always use the last version exchange the version code with the keyword _current_ as such `/api/preferences/current`

See the belonging references for more details to each version:
+ [preferences - version 1](https://github.com/OpServ-Monitoring/opserv-backend/wiki/RESTful-API-reference:-preferences-v1)
