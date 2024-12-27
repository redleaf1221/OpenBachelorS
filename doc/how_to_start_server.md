# How to Start Server

4 ways available. Choose one you like.

## 1st Way

```
python main.py
```

## 2nd Way

```
python -m src.app
```

## 3rd Way

```
flask --app src/app --debug run -h 127.0.0.1 -p 8443
```

`python -m flask` can be used instead of `flask`.

## 4th Way

```
waitress-serve --host=127.0.0.1 --port=8443 src.app:app
```

`python -m waitress` can be used instead of `waitress-serve`.
