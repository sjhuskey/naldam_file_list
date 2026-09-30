# NALDAM File List Utility

The script `naldam_file_list.py` reads the list of file paths in the file `file_inventory.csv`, which was produced by doing the following on the TrueNAS server:

```
find  /mnt/data-pool/data/files/Masters -type f -printf '"%p","%f","%e","%s","%TY-%Tm-%Td %TH:%TM:%TS"\n' >> file_inventory.csv
```

That should be run again if any files are added or deleted from the `Masters` directory, and the resulting file should replace the `file_inventory.csv` file in this directory.

