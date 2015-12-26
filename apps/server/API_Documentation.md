**This documentation is automatically generated.**

**Output schemas only represent `data` and not the full output; see output examples and the JSend specification.**

# /v1/job/\(\[0\-9\]\+\)

    Content-Type: application/json

## GET


**Input Schema**
```json
null
```



**Output Schema**
```json
{
    "properties": {
        "fqid": {
            "type": "integer"
        },
        "status": {
            "type": "string"
        }
    },
    "type": "object"
}
```





## POST


**Input Schema**
```json
{
    "properties": {
        "fqid": {
            "type": "integer"
        },
        "queries": {
            "items": {
                "oneOf": [
                    {
                        "properties": {
                            "name": {
                                "type": "string"
                            },
                            "sql": {
                                "type": "string"
                            }
                        },
                        "required": [
                            "name",
                            "sql"
                        ],
                        "type": "object"
                    }
                ]
            },
            "type": "array"
        },
        "query_type": {
            "type": "string"
        }
    },
    "required": [
        "fqid",
        "query_type",
        "queries"
    ],
    "type": "object"
}
```



**Output Schema**
```json
null
```





<br>
<br>

# /v1/job/?

    Content-Type: application/json

## GET


**Input Schema**
```json
null
```



**Output Schema**
```json
{
    "properties": {
        "fqid": {
            "type": "integer"
        },
        "status": {
            "type": "string"
        }
    },
    "type": "object"
}
```





## POST


**Input Schema**
```json
{
    "properties": {
        "fqid": {
            "type": "integer"
        },
        "queries": {
            "items": {
                "oneOf": [
                    {
                        "properties": {
                            "name": {
                                "type": "string"
                            },
                            "sql": {
                                "type": "string"
                            }
                        },
                        "required": [
                            "name",
                            "sql"
                        ],
                        "type": "object"
                    }
                ]
            },
            "type": "array"
        },
        "query_type": {
            "type": "string"
        }
    },
    "required": [
        "fqid",
        "query_type",
        "queries"
    ],
    "type": "object"
}
```



**Output Schema**
```json
null
```





<br>
<br>

# /v1/status

    Content-Type: application/json

## GET


**Input Schema**
```json
null
```



**Output Schema**
```json
{
    "properties": {
        "status": {
            "type": "string"
        }
    },
    "type": "object"
}
```




