This is a toy project I created when we were naming our first son. The principle was to use reinforcement learning to focus in on the perfect names.

<img src="https://i.imgflip.com/2l86z8.gif" title="made at imgflip.com"/>
<br />

There is a mobile app in `/frontend` based on QuasarJS for rating names, and a Python app that predicts, ranks, and serves the names in online fashion.


## Quickstart

### Client
**Local**

```
cd frontend && quasar dev
```

**Mobile App (for the misses)**
1. Enter the ML Server API/hostname in `frontend/src/config.js`
2. Download [Quasar Play](https://play.google.com/store/apps/details?id=com.quasarframework.quasarplay)
3. run `frontend/quasar dev --play`
4. scan the QR code to run the app locally
```
quasar dev --play
```

### Server

```python
#pip install requirements.txt
hug -f api.py
```


## Contributing

Efforts are better directed towards a fresh codebase. If you are working on that, here's some easy improvements to build on:

**Name pool**
```
mysql> SELECT gender, COUNT(1) FROM names GROUP BY 1;
+--------+----------+
| gender | COUNT(1) |
+--------+----------+
| M      |      292 |
| F      |      353 |
+--------+----------+
2 rows in set (0.00 sec)
```

At the surface this seems like a lot of names, but having rated them multiple times it is very limiting.

**Features**

This is the current feature set:
```
features = [
        , len(name) # length
        , sum(name.count(c) for c in consonants) # number of consonants
        , sum(name.count(c) for c in vowels) #" number_of_vowels":
        , syllables(name) # number of syllables
        , lookup["year"] # popular in year
        , lookup["rank"] # rank in ^ year
        , name[1] #  "first_letter":
        , name[-1] # "last_letter":
        , lookup["year"]
        , lookup["rank"]
    ]
```
