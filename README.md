# NALDAM File List Utility

The script `naldam_file_list.py` reads the list of file paths in the file `file_inventory.csv`, which was produced by doing the following on the TrueNAS server:

```
find  /mnt/data-pool/data/files/Masters -type f -printf '"%p","%f","%e","%s","%TY-%Tm-%Td %TH:%TM:%TS"\n' >> file_inventory.csv
```

That should be run again whenever files are added or deleted from the `Masters` directory, and the resulting file should be copied to this directory as `file_inventory.csv`.

The script reads that file and converts it into a Pandas Dataframe. It then performs some operations on the `full_path` column to make it possible to filter the list by collection.

The script takes one argument: `--collection`. The value for that argument should be the three-letter abbreviation of the collection in which the desired files are housed.

## Usage

The script requires the the Pandas library. You can install an environment with everything you need by doing the following from the command line inside the script's directory:

```bash
conda create -n file_names --file environment.yml
```

Then:

```bash
conda activate file_names
```

Alternatively, you can just install Pandas in your own environment by doing `conda install pandas`.

Run the script from its home directory by entering the following on the command line:

```bash
python naldam_file_list.py --collection <collection_abbreviation>
```

For example, to get the names of the files in the CAR collection, do `python naldam_file_list.py --collection CAR`. 

The output will be a CSV file with two columns: `filename` and `full_path`. The file will be named with this pattern: `<collection_abbr>_file_list.csv`. For CAR, that would be `CAR_file_list.csv`.

