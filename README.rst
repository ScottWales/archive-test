An archive system

Supports metadata and versions

Create a dataset
    archive dataset "My Dataset"

    # Enter dataset metadata manually

Put a file into the archive
    archive put $file --dataset "My Dataset"

Get a file from the archive
    archive get $file

Find a dataset
    archive find --title "Sample title" --variable "tas" --all-versions

    ab123.nc "Title" "Summary"
        v20180301T1200 [sha256]
    cd456.nc "Title 2" "Summary"
        v20180301T1200 [sha256]
        v20150301T1205 [sha256]


Internal storage is by file content hash for large files

    mdss ls archive/objects/ab/cdefi123456

or in a tarball for small files

    mdss ls archive/datasets/My\ Dataset/0000.tar

The dataset directory contains a sqlite database index.db
describing the contents

This gets downloaded into a cache directory when performing operations

Database Schema

File
id  sha256    location    put_date    get_date    get_count

FileMetadata
id  filename    title   summary keywords time_start time_end

VariableMetadata
id  file_id name    standard_name   units   dimensions


* Handle storing data fresh from a model run

   archive put --dataset ${RUNID} ${FILES}

* Get stats

   archive usage
        Show usage by dataset
        Including old files

* Web interface to search through catalouge?

MVP:

    archive init --dataset ${ID}
    archive put --dataset ${ID} ${FILE}
    archive get --dataset ${ID} ${FILE}
    archive list
