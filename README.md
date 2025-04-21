# Genomic Sequence Server

A server that provides genomic data, including gene sequences, chromosome lengths, and more, for various species using the Ensembl API.

## Description

**Genomic Sequence Server** is a web-based service that allows users to retrieve genomic data, including gene sequences, chromosome lengths, and other biological information, for different species. It connects to the Ensembl REST API and processes the data to provide users with an easy-to-understand output.

## Features

- Retrieve gene sequences by gene name or species
- Get chromosome lengths for specific species
- Retrieve karyotype data (chromosome names) for various species
- Perform simple genomic calculations (e.g., sequence lengths)
- Error handling for incorrect inputs

## Installation

### Prerequisites:

- Python 3.x
- `pip` (Python package manager)

Once the server is running, you can access the web application by navigating to `http://localhost:8080` in your browser.

## Usage

### Endpoints

- **Get Gene Sequence for a Gene in Homo sapiens:**
/geneSeq?gene=frat1


- **Get Chromosome Length for Homo sapiens Chromosome 1:**
/chromosomeLength?specie=human&min_len=1


- **Get Karyotype Data for a Specie:**
/karyotype?specie=human


### Example Query:
To get the gene sequence for **frat1** in **Homo sapiens**, visit the following URL:

http://localhost:8080/geneSeq?gene=frat1


## Contributing

If you'd like to contribute to this project, please fork the repository and submit a pull request with your changes. Here's how to do it:

1. Fork the repository.
2. Create a new branch for your feature: `git checkout -b feature-branch`.
3. Make your changes and commit them: `git commit -m 'Add feature'`.
4. Push to your forked repository: `git push origin feature-branch`.
5. Open a pull request.
