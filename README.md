# tinyURL

## Requirement
* python 3.5.2
* flask 1.1.1
* redis 3.3.8

## Usage

### 0) To begin using the virtual environment, it needs to be activated
```bash
source env/bin/activate
```

### 1) Synchronizes the database state with the current set of models and migrations
```bash
python manage.py

```

## Description

A project about how to transform a long url to shorter one is implemented here. We creared two methods to store the key-value pair data: one is hashtable and the other is redis database.

## Requirements

1. Flask web framework
2. NoSQL Redis

## Snapshot
![](https://i.imgur.com/BViFBru.png)
