To add new api docs you must:

1. Create a new json file based on any of the already existing json files:

```sh
cp <file>.json <your_docs_file>.json
# (make sure there aren't any files already named what you want to name your docs file) 
```

2. Edit your docs as to reflect what that API does.

3. Execute the py script
```sh
python3  convert.py > test.html
```

4. Open the test.html file in your favorite browser to check that it worked.

5. If it worked just fine you can replace the old api.html file with the test.html file.

```sh
mv test.html api.html
```

6. Now commit your changes to github and the api should be up and running in no time :)
