import subprocess as sp
import pandas as pd
from Bio import PDB
import os
import shlex
import time


def main():
    """
    Load entries.idx from pdb, parse it, load all pdb files contains 'RNA' in header.
    Perform base pair annotation of all rna pdb files in rna_ids file via rnaview
    :return:
    """
    # Loading
    # Initialize loading class
    load_struct = PDB.PDBList()

    # Parse command to load pdb index file
    command = shlex.split('wget ftp://ftp.wwpdb.org/pub/pdb/derived_data/index/entries.idx')
    # Run command
    sp.check_output(command, universal_newlines=True)

    # Delete junk --lines in file, make header tab-separated as whole other file
    with open('entries.idx', 'r') as source, open('pdb_index', 'w') as target:
        for ind, line in enumerate(source):
            if ind == 0:
                line = line.replace(', ', '\t')
            if not line.startswith('-'):
                target.write(line)


    # Create dataframe from full file with pdb index
    with open('pdb_index', 'r') as source:
        data = pd.read_csv(source, sep='\t')

    print(data.shape, data.columns)


    # Checking data
    print(data.isnull().any(), data.shape)

    # Drop files with empty header
    data.dropna(subset=['HEADER'], inplace=True)
    print(data.shape)

    # Filter subset of data with RNA in header
    mask = data['HEADER'].str.contains('RNA')
    rna = data[mask]

    # Create list with PDB ids of files with RNA
    rna_ids = rna['IDCODE'].unique().tolist()
    rna_length = len(rna_ids)
    rna_length, rna.head(), rna_ids


    with open('rna_ids', 'w') as file:
        for entry in rna_ids:
            file.write('{}\n'.format(entry))


    # Load 1 pdb file from RNA list, wait 30 seconds
    for ind, file in enumerate(rna_ids, 1):
        load_struct.retrieve_pdb_file(file, file_format='pdb',pdir='/home/arleg/PycharmProjects/Bioinformatics/RNA/pdb')
        print("{} is loaded, {} from {}".format(file, ind, rna_length))
        time.sleep(30)




    # Base pair annotation of all rna pdb files in rna_ids file
    # Add rnaview environment variable to environment in this script (it should be done despite the record of path to
    # tool and environment variable in .bashrc)
    envir = os.environ
    envir['RNAVIEW'] = '/home/arleg/RNATools/RNAVIEW'

    # Call rnaview on all files listed in rna_ids
    # There is an option in rnaview to read all pdbs in one call to tool, yet it didn`t work in my script
    with open('rna_ids', 'r') as file:
        for line in file:
            line = line.strip().lower()
            # Parse command to terminal
            command = shlex.split('/home/arleg/RNATools/RNAVIEW/bin/rnaview pdb/pdb{}.ent'.format(line))
            # Run it
            sp.check_output(command, env=envir, universal_newlines=True)


if __name__ == '__main__':
    main()

