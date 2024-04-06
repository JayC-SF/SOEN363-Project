# Concordia's Best Hits (SOEN 363 - Final Project)

## Description

Concordia's Best Hits is a comprehensive MySQL database containing hundreds of thousands of records encompassing various aspects of music, including tracks, artists, albums, playlists, genres, and even audiobooks. The data has been meticulously gathered using Python scripts leveraging the Spotify API and MusicBrainz API for scraping.

## Getting Started

To set up the project and populate the MySQL database, follow these steps:

1. Clone the Repository: Clone the Concordia's Best Hits repository to your local machine.

```bash
git clone https://github.com/JayC-SF/SOEN363-Project.git
```

2. Install Dependencies: Make sure you have Python installed on your system. Install the required Python dependencies by running:

```bash
pip install -r requirements.txt
```

3. Create a connection to your local MySQL server to be able to run the DML and DDL code. You can perform this by setting up your own database in MySQL using Visual Studio Code.

Alternatively, you can also connect to our database that is hosted on our personal server which will contain a database named `project` that already has all the data required.
The credentials to connect are the following:

```
URL: jdbc:mysql://walidoow.com:3306/project

USER: mysql
PASSWORD: fLkuJLPgt*9kB5

Info already included in the URL:
HOST: walidoow.com
PORT: 3306
DATABASE: project
```

4. Run the `SOEN363_FinalProject_DDL.sql` to create all the tables required for the database. You can select all the queries and run them.
One problem is that the file is too large for submission so to access it, please download it from the following link and place it at the root folder:

```
https://drive.google.com/file/d/1hNQ1UypdFCoF5RwHfwFfyHmfP0yahKGa/view?usp=sharing
```

To execute it, install MySQL on your terminal and run the following command in a Linux terminal:

```
source ./SOEN363_FinalProject_DML.sql
```

6. With the database populated, run each query inside `SOEN363_FinalProject_Queries.sql` to verify if the queries are working as intended.

## Contributors

- Juan-Carlos Sreng-Flores (40101813)
- Walid Achlaf (40210355)
- Daniel Lam (40248073)

## License

This project is licensed under the MIT License. 