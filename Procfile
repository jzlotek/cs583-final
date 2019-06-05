web echo "http://drexel-cs583-final.s3.us-east-2.amazonaws.com/model.zip" | python src/threaded_download.py -v -d ./src/trained_model --clobber\
    && python src/unzip_files.py src/trained_model/model.zip src/trained_model\
    && mv src/trained_model/result_Sony/* src/trained_model/.\
    && python src/app.py
