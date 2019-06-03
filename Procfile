web echo "http://drexel-cs583-final.s3.us-east-2.amazonaws.com/model.zip" | python src/threaded_download.py -v -d ./src/trained_models --clobber\
    && python src/unzip_files.py src/trained_models/model.zip src/trained_models\
    && mv src/trained_models/result_Sony/* src/trained_models/.\
    && python src/app.py
